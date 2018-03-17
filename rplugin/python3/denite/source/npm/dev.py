# pylint: disable=E0401,C0411
import os
import platform
from ..base import Base
from operator import itemgetter
from ...kind.npm import Kind

isMac = platform.system() == 'Darwin'

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'npm/dev'
        self.kind = Kind(vim)

    def highlight(self):
        self.vim.command('highlight link deniteSource__NpmName Directory')
        self.vim.command('highlight link deniteSource__NpmDirectory Comment')

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource__NpmHeader /^.*$/ '
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource__NpmName /^.*\%22c/ contained '
                         r'contained containedin=deniteSource__NpmHeader')
        self.vim.command(r'syntax match deniteSource__NpmDirectory /\%25c\S\+/ contained '
                         r'contained containedin=deniteSource__NpmHeader')


    def gather_candidates(self, context):
        projects = self.vim.call('npm#projects')
        homepath = os.path.expanduser('~')

        candidates = []
        for item in projects:
            mtime = os.stat(item['directory']).st_mtime
            candidates.append({
                'word': item['name'] + item['description'],
                'abbr': '%-22s %-26s %s' % (item['name'],
                                            item['directory'].replace(homepath, '~'),
                                            item['description']),
                'source__mtime': mtime,
                'action__path': item['directory'],
                'source__name': item['name'],
                })

        return sorted(candidates, key=itemgetter('source__mtime'),
                      reverse=True)
