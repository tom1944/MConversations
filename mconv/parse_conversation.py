from strictyaml import dirty_load, YAML, Map, Str, Int, Seq, Optional

from mconv.conversation import Conversation
from mconv.line import Line


KEYWORD_SPEAKER_NAME = 'speaker-name'
KEYWORD_DEFAULT_SPEAK_TIME_SEC = 'default-speak-time-sec'
KEYWORD_CONVERSATION = 'conversation'
KEYWORD_SAY = 'say'
KEYWORD_SPEAK_TIME_SEC = 'speak-time-sec'


def parse_conversation(yaml_conversation: str) -> Conversation:
    yaml = string_to_yaml(yaml_conversation)
    return yaml_to_conv(yaml)


def string_to_yaml(yaml_conversation: str) -> YAML:
    schema = Map({
        KEYWORD_SPEAKER_NAME: Str(),
        KEYWORD_DEFAULT_SPEAK_TIME_SEC: Int(),
        KEYWORD_CONVERSATION: Seq(
            Map({
                KEYWORD_SAY: Str(),
                Optional(KEYWORD_SPEAK_TIME_SEC): Int()
            })
        )
    })

    return dirty_load(yaml_conversation, schema=schema, allow_flow_style=True)


def yaml_to_conv(yaml: YAML) -> Conversation:
    return YamlConversationParser(yaml).parse_conversation()


class YamlConversationParser:
    def __init__(self, yaml: YAML):
        self.yaml = yaml
        self.default_speak_time_sec = yaml[KEYWORD_DEFAULT_SPEAK_TIME_SEC].value

    def parse_conversation(self) -> Conversation:
        speaker_name = self.yaml[KEYWORD_SPEAKER_NAME].value
        yaml_lines = self.yaml[KEYWORD_CONVERSATION]

        lines = [self.read_line(yaml_line) for yaml_line in yaml_lines]

        return Conversation(speaker_name, lines)

    def read_line(self, yaml_line: YAML) -> Line:
        text = yaml_line[KEYWORD_SAY].value

        if KEYWORD_SPEAK_TIME_SEC in yaml_line:
            speak_time = yaml_line[KEYWORD_SPEAK_TIME_SEC].value
        else:
            speak_time = self.default_speak_time_sec

        return Line(text, speak_time)
