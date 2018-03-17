# ============================================================================
# FILE: npm.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# CREATED: Mar 17, 2018
# ============================================================================
# pylint: disable=E0401,C0411
import os
import platform
import re
from .base import Base

isMac = platform.system() == 'Darwin'

class Kind(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'npm/base'
        self.default_action = 'open'

    def action_open(self, context):
        target = context['targets'][0]
        self.vim.command('Denite file_rec:%s' % target['action__path'])

    def action_tabopen(self, context):
        target = context['targets'][0]
        if not isMac:
            return
        self.vim.call('npm#iterm_tabopen', target['action__path'])

    def action_preview(self, context):
        target = context['targets'][0]
        fields = ' '.join(self.vim.evel('g:npm_view_fields'))
        cmd = 'npm view %s %s' % (target['source__name'], fields)
        self.vim.call('npm#run_command', cmd)

    def action_browser(self, context):
        for item in context['targets']:
            url = 'https://www.npmjs.com/package/%s' % item['source__name']
            self.vim.call('denite#util#open', url)

    def action_help(self, context):
        target = context['targets'][0]
        items = os.scandir(target['action__path'])
        pattern = re.compile(r'readme\.md', re.I) #pylint: disable=E1101
        for item in items:
            if item.is_file() and pattern.match(item.name):
                self.vim.command('keepalt edit %s' % item.path)
                self.vim.command('set readonly')
                break
