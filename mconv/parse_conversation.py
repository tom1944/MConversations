from strictyaml import dirty_load, YAML, Map, Int, Seq, Optional, Any

from mconv.conversation import Conversation
from mconv.minecraft.line import Line


KEYWORD_SPEAKER_NAME = 'speaker-name'
KEYWORD_DEFAULT_SPEAK_TIME_SEC = 'default-speak-time-sec'
KEYWORD_CONVERSATION = 'conversation'
KEYWORD_SAY = 'say'
KEYWORD_SPEAK_TIME_SEC = 'speak-time-sec'


def parse_conversation(conv_name: str, yaml_conversation: str, function_prefix: str) -> Conversation:
    yaml = string_to_yaml(yaml_conversation)
    return YamlConversationParser(conv_name, yaml, function_prefix).parse_conversation()


def string_to_yaml(yaml_conversation: str) -> YAML:
    schema = Map({
        KEYWORD_SPEAKER_NAME: Any(),
        KEYWORD_DEFAULT_SPEAK_TIME_SEC: Int(),
        KEYWORD_CONVERSATION: Seq(
            Map({
                KEYWORD_SAY: Any(),
                Optional(KEYWORD_SPEAK_TIME_SEC): Int()
            })
        )
    })

    return dirty_load(yaml_conversation, schema=schema, allow_flow_style=True)


class YamlConversationParser:
    def __init__(self, conv_name: str, yaml: YAML, function_prefix: str):
        self.conv_name = conv_name
        self.yaml_data = yaml.data
        self.function_prefix = function_prefix
        self.default_speak_time_sec = yaml[KEYWORD_DEFAULT_SPEAK_TIME_SEC].value

    def parse_conversation(self) -> Conversation:
        function_prefix = self.function_prefix
        speaker_name = self.yaml_data[KEYWORD_SPEAKER_NAME]
        yaml_lines = self.yaml_data[KEYWORD_CONVERSATION]

        lines = [self.read_line(yaml_line) for yaml_line in yaml_lines]

        return Conversation(self.conv_name, function_prefix, speaker_name, lines)

    def read_line(self, yaml_line) -> Line:
        text = yaml_line[KEYWORD_SAY]

        if KEYWORD_SPEAK_TIME_SEC in yaml_line:
            speak_time = yaml_line[KEYWORD_SPEAK_TIME_SEC]
        else:
            speak_time = self.default_speak_time_sec

        return Line(text, speak_time)
