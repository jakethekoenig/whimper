# Whimper

Want to talk to neovim? Now you can! This repository is sort of a work in progress so not many affordances for picking your mic, model size, language, and hardware are provided. The UX around typing TYPE/CODE in insert mode will likely change as well. Feel free to open an issue or make a pull request.

# Installation

```bash
git clone https://github.com/jakethekoenig/whimper.git ~/.vim/pack/misc/start/
cd ~/.vim/pack/misc/start/whimper
pip install -r requirements.txt
export OPENAI_API_KEY=<YOUR API KEY> # If not already set
```

# Usage

In insert mode type `TALK` and neovim will start listening to your microphone and insert the transcription. If you type `CODE` lines above and the transcription will be given to ChatGPT which will attempt to rewrite your spoken word as code.
