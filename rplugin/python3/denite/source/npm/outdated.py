# pylint: disable=E0401,C0411
import os
from os.path import expanduser
import re
from ..base import Base
from ...kind.npm import Kind as BaseKind

splitRe = re.compile(r"\s+")

def _find_root(path):
    while True:
        if path == '/' or os.path.ismount(path):
            return None
        p = os.path.join(path, 'package.json')
        if os.access(p, os.R_OK):
            return path
        path = os.path.dirname(path)

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = 'npm/outdated'
        self.kind = Kind(vim)
        self.sorters = []

    def on_init(self, context):
        cwd = self.vim.call('getcwd')
        context['__root'] = _find_root(cwd)

    def highlight(self):
        self.vim.command('highlight default link deniteSource__NpmName Title')
        self.vim.command('highlight default link deniteSource__NpmCurrent Comment')
        self.vim.command('highlight default link deniteSource__NpmWanted GruvboxGreen')
        self.vim.command('highlight default link deniteSource__NpmLatest WarningMsg')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource__Npm /^.*$/ ' +
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource__NpmHeader /^.*$/ contained '
                         r'contained containedin=deniteSource__Npm')
        self.vim.command(r'syntax match deniteSource__NpmName /^.*\%29c/ contained '
                         r'contained containedin=deniteSource__NpmHeader')
        self.vim.command(r'syntax match deniteSource__NpmCurrent /\%30c.\+\%39c/ contained '
                         r'contained containedin=deniteSource__NpmHeader')
        self.vim.command(r'syntax match deniteSource__NpmWanted /\%40c.\+\%49c/ contained '
                         r'contained containedin=deniteSource__NpmHeader')
        self.vim.command(r'syntax match deniteSource__NpmLatest /\%50c.*$/ contained '
                         r'contained containedin=deniteSource__NpmHeader')

    def gather_candidates(self, context):
        root = context['__root']
        candidates = []
        tmp = expanduser(context['args'][0])

        with open(tmp) as fp:
            for line in fp:
                result = self.parse_line(line)
                if result:
                    candidates.append(_candidate(result, root))
        return candidates

    def parse_line(self, line):
        # name current wanted latest
        if line.startswith('Package'):
            return None
        parts = splitRe.split(line)
        if len(parts) < 4:
            return None
        if parts[1] == parts[3]:
            return None
        return {
            'name': parts[0],
            'current': parts[1],
            'wanted': '' if parts[1] == parts[2] else parts[2],
            'latest': '' if parts[1] == parts[3] or parts[2] == parts[3] else parts[3],
            }

def _candidate(x, root):
    return {
        'word': x['name'],
        'abbr': '%-28s %-9s %-9s %-9s' % (x['name'], x['current'], x['wanted'], x['latest']),
        'source__name': x['name'],
        'action__path': os.path.join(root, 'node_modules', x['name']),
        }

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'npm/oudated'

    def action_update(self, context):
        args = ' '.join(map(lambda x: x['source__name'], context['targets']))
        cmd = 'npm update %s' % args
        self.vim.call('npm#run_command', cmd)

    def action_upgrade(self, context):
        args = ' '.join(map(lambda x: x['source__name'] + '@latest', context['targets']))
        cmd = 'npm install %s' % args
        self.vim.call('npm#run_command', cmd)
