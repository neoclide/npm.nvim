# ============================================================================
# FILE: npm.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
import json
from .base import Base
from denite import util
from operator import itemgetter
from ..kind.npm import Kind as BaseKind

def _find_json(path):
    while True:
        if path == '/' or os.path.ismount(path):
            return None
        p = os.path.join(path, 'package.json')
        if os.access(p, os.R_OK):
            return p
        path = os.path.dirname(path)

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'npm'
        self.kind = Kind(vim)

    def on_init(self, context):
        cwd = self.vim.call('getcwd')
        context['__package'] = _find_json(cwd)

    def highlight(self):
        self.vim.command('highlight default link deniteNodeName Title')
        self.vim.command('highlight default link deniteNodeVersion Statement')
        self.vim.command('highlight default link deniteNodeDev Comment')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteNode /^.*$/ ' +
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteNodeName /^\s\?\S\+/ ' +
                         r'contained containedin=deniteNode')
        self.vim.command(r'syntax match deniteNodeVersion /(.\{-})/ ' +
                         r'contained containedin=deniteNode')
        self.vim.command(r'syntax match deniteNodeDev /\v\[D\]/ ' +
                         r'contained containedin=deniteNode')

    def gather_candidates(self, context):
        package = context['__package']
        if not package:
            util.error(self.vim, 'package.json not found')
            return []

        root = os.path.dirname(package)
        items = []
        with open(package) as fp:
            try:
                obj = json.loads(fp.read())
                deps = obj.get('dependencies')
                devDeps = obj.get('devDependencies')
                if deps:
                    items += [{'name': x, 'dev': False}
                              for x in deps]
                if devDeps:
                    items += [{'name': x, 'dev': True}
                              for x in devDeps]
            except json.JSONDecodeError:
                util.error(self.vim, 'Decode error for %s' % package)
                return []

        candidates = []
        for item in items:
            jsonpath = os.path.join(root, 'node_modules', item['name'], 'package.json')
            if not os.access(jsonpath, os.R_OK):
                continue
            stat = os.stat(jsonpath)
            with open(jsonpath) as fp:
                try:
                    obj = json.loads(fp.read())
                    mtime = stat.st_mtime
                    version = obj.get('version', 'unknown')
                    name = item['name']
                    candidates.append({
                        'word': name,
                        'abbr': '%s (%s) %s' % (name, version, '[D]' if item['dev'] else ''),
                        'action__path': os.path.dirname(jsonpath),
                        'source__prod': not item['dev'],
                        'source__mtime': mtime,
                        'source__root': root,
                        'source__name': name,
                        })
                except json.JSONDecodeError:
                    util.error(self.vim, 'Decode error for %s' % jsonpath)
                    continue

        return sorted(candidates, key=itemgetter('source__prod', 'source__mtime'),
                      reverse=True)

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.persist_actions += ['delete', 'update'] #pylint: disable=E1101
        self.redraw_actions += ['delete', 'update'] #pylint: disable=E1101
        self.default_action = 'open'
        self.name = 'npm'

    def action_update(self, context):
        arg = ' '.join(map(lambda x: x['word'], context['targets']))
        cmd = 'npm update %s' % (arg, )
        self.vim.call('npm#run_command', cmd)

    def action_find(self, context):
        target = context['targets'][0]
        name = target['source__name']
        self.vim.command('Denite func:m:%s' % name)

    def action_delete(self, context):
        arg = ' '.join(map(lambda x: x['word'], context['targets']))
        cmd = 'npm uninstall %s' % (arg, )
        self.vim.call('npm#run_command', cmd)
