# MConversations
A tool to generate NPC conversations in minecraft.

This tool uses minecraft data packs (see [this minecraft wiki page](https://minecraft.gamepedia.com/Data_Pack)).

## Features
- Define your conversations in yaml files:
```yaml
speaker-name: Erik
default-speak-time-sec: 2
conversation:
  - say: Hello!
  - say: This is a very long text that requires 3 seconds of reading time
    speak-time-sec: 3
  - say: This is the end...
```
- Automatic detection and translation of all conversations for a data pack
- Support for text formatting using JSON text:
```yaml
speaker-name: {"text": "Erik", "color": "red"}
default-speak-time-sec: 2
conversation:
  - say: {"text": "Hello!", "color": "blue"}
```
- Support for executing functions within a conversation:
```yaml
speaker-name: "John"
default-speak-time-sec: 2
conversation:
  - say: You earned a reward!
  - function: mynamespace:rewarding-function
```

See the [example-datapack](./example-datapack) directory for an example data pack.

## Installation
- Install [Python 3.9.2](https://www.python.org/downloads/release/python-392/)
- Install StrictYAML:
`pip install strictyaml==1.3.2`

## How to use
- Create your conversation file `conv.yaml`:
- Place this file under the data pack functions folder
  e.g. as `mydatapack/data/mynamespace/functions/conv.yaml`
- Run `python mconv.py path/to/mydatapack` to create a set of .mcfunction files in the data pack.
- Run the command `/reload` from your minecraft world to reload your data pack
- Run the command `/function mynamespace:conv` to play the conversation to all players

You can use the [example-datapack](./example-datapack) to bootstrap your datapack.

