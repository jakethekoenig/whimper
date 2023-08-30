let s:path = expand('<sfile>:p:h')
call remote#host#RegisterPlugin('python3', s:path.'/whimper.py', [
      \ {'sync': v:false, 'name': 'Whimper', 'type': 'function', 'opts': {}},
      \ {'sync': v:false, 'name': 'Transcribe', 'type': 'function', 'opts': {}},
     \ ])

inoremap TALK <Esc>:call Transcribe()<CR>
inoremap CODE <Esc>:call Whimper()<CR>
