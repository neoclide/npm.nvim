# pylint: disable=E0401,C0411
from os.path import expanduser
from ..base import Base
from ...kind.npm import Kind as BaseKind

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = 'npm/used'
        self.kind = Kind(vim)
        self.home = expanduser('~')
        self.sorters = []

    def highlight(self):
        # TODO highlight
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
        items = self.vim.call('NpmUsedModules')
        return map(lambda item: {
            'word': item['name'],
            'abbr': '%s - %s' % (item['name'], item['description']),
            'source__name': item['name'],
            }, items)

class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'npm/used'
        self.default_action = 'install'

    def action_install(self, context):
        arg = ' '.join(map(lambda x: x['source__name'], context['targets']))
        cmd = 'npm install %s' % (arg, )
        self.vim.call('npm#run_command', cmd)
