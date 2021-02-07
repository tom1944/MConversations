# MConversations
A tool to generate NPC conversations in minecraft

## Installation
- Install [Python 3.7](https://www.python.org/downloads/release/python-379/)
- Install StrictYAML:
`pip install strictyaml==1.3.2`

## How to use
See `conv-example.yaml` for an  example conversation file.

- Run ```python mconv.py conv-example.yaml```
to create a minecraft function file `conv-example.mcfunction`.

- Place this file in your datapack under `<data-pack-name>/data/<namespace>/functions`.

See [this minecraft wiki page](https://minecraft.gamepedia.com/Data_Pack) for more info about data packs.
