" ============================================================================
" Description: provide npm command for vim
" Author: Qiming Zhao <chemzqm@gmail.com>
" Licence: MIT licence
" Version: 0.1
" Last Modified:  March 16, 2018
" ============================================================================
if exists('did_npm_nvim_loaded') || v:version < 800
  finish
endif
let did_npm_nvim_loaded = 1

let g:npm_view_fields = get(g:, 'npm_view_fields',
      \['author','repository.url','version','description','homepage','license'])
let g:npm_project_folders = get(g:, 'npm_project_folders', [])
let g:npm_parsefunc_command = get(g:, 'npm_parsefunc_command',
      \expand('<sfile>:p:h:h').'/node_modules/.bin/parsefunc')

function! s:encodeURIComponent(str)
  let s = ''
  for i in range(strlen(a:str))
    let c = a:str[i]
    if c =~# "[A-Za-z0-9-_.!~*'()]"
      let s .= c
    else
      let s .= printf('%%%02X', char2nr(a:str[i]))
    endif
  endfor
  return s
endfunction

function! s:NpmInstall(...)
  let cmd = 'npm install '.join(a:000, ' ')
  function! Callback(cmd, succeed)
    if a:succeed
      echohl MoreMsg | echon a:cmd . ' succeed' | echohl None
    endif
  endfunction
  let cwd = fnamemodify(findfile('package.json', '.;'), ':p:h')
  call npm#run(cmd, cwd, function('Callback', [cmd]), v:true)
endfunction

function! s:YarnAdd(...)
  let cmd = 'yarn add '.join(a:000, ' ')
  function! Callback(cmd, succeed)
    if a:succeed
      echohl MoreMsg | echon a:cmd . ' succeed' | echohl None
    endif
  endfunction
  let cwd = fnamemodify(findfile('package.json', '.;'), ':p:h')
  call npm#run(cmd, cwd, function('Callback', [cmd]), v:true)
endfunction

function! s:NpmRun(name)
  if empty(a:name)
    let keys = keys(NpmScripts())
    for str in ['start', 'dev', 'watch']
      if index(keys, str) >= 0
        let name = str
        break
      endif
    endfor
  else
    let name = a:name
  endif
  if empty(name)
    echoerr 'No script node'
    return
  endif
  let cmd = 'npm run '.name
  let cwd = fnamemodify(findfile('package.json', '.;'), ':p:h')
  function! Callback(cmd, succeed)
  endfunction
  call npm#run(cmd, cwd, function('Callback', [cmd]), v:true)
endfunction

function! s:NpmSearch(args)
  call denite#util#open('https://www.npmjs.com/search?q='.s:encodeURIComponent(a:args))
endfunction

function! s:ListScripts(A, L, P)
  let obj = NpmScripts()
  return join(keys(obj), "\n")
endfunction

function! s:NpmOutdated()
  let cwd = fnamemodify(findfile('package.json', '.;'), ':p:h')
  let file = tempname()
  let g:command_running = 1
  call jobstart('npm outdated > '.file, {
        \ 'on_exit': function('s:onOutdatedExit'),
        \ 'buffer_nr': bufnr('%'),
        \ 'cwd': cwd,
        \ 'file': file,
        \})
endfunction

function! s:onOutdatedExit(job_id, status, event) dict
  let g:command_running = 0
  execute 'silent! bd! '.self.buffer_nr
  execute 'Denite -mode=normal npm/outdated:'.self.file
endfunction

command! -nargs=? -complete=custom,s:ListScripts NpmRun :call s:NpmRun(<q-args>)
command! -nargs=0 NpmDev :Denite npm/dev
command! -nargs=* YarnAdd :call s:YarnAdd(<f-args>)
command! -nargs=0 NpmOutdated :call s:NpmOutdated()
command! -nargs=* NpmInstall :call s:NpmInstall(<f-args>)
command! -nargs=1 NpmSearch :call s:NpmSearch(<q-args>)
