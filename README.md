# MConversations
A tool to generate NPC conversations in minecraft

## Installation
- Install [Python 3.7](https://www.python.org/downloads/release/python-379/)
- Install StrictYAML:
`pip install strictyaml==1.3.2`

## How to use
- Create your conversation file `conv.yaml`:
```yaml
function-prefix: mynamespace:path/to/dir/
speaker-name: Erik
default-speak-time-sec: 2
conversation:
  - say: Hello!
  - say: This is a very long text that requires 3 seconds of reading time
    speak-time-sec: 3
  - say: This is the end...
```


- Run ```python mconv.py conv.yaml``` to create a set of function files.
Place these files in `mydatapack/data/mynamespace/functions/path/to/dir`.

See [this minecraft wiki page](https://minecraft.gamepedia.com/Data_Pack) for more info about data packs.
