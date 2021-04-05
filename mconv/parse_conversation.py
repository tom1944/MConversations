from strictyaml import dirty_load, YAML, Map, Int, Seq, Optional, Any, Str, MapPattern

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.conversation.line import Line, TextLine, FunctionLine

KEYWORD_SPEAKER_NAME = 'speaker-name'
KEYWORD_DEFAULT_SPEAK_TIME_SEC = 'default-speak-time-sec'
KEYWORD_CONVERSATION = 'conversation'
KEYWORD_SAY = 'say'
KEYWORD_SPEAK_TIME_SEC = 'speak-time-sec'
KEYWORD_FUNCTION = 'function'


def parse_conversation(conv_ctx: ConversationContext, yaml_conversation: str) -> Conversation:
    yaml = YamlReader(yaml_conversation, conv_ctx).read_yaml()
    return YamlConversationParser(yaml, conv_ctx).parse_conversation()


class YamlReader:
    def __init__(self, yaml: str, conv_ctx: ConversationContext):
        self._yaml_str = yaml
        self._conv_ctx = conv_ctx

    def read_yaml(self):
        yaml = dirty_load(
            self._yaml_str,
            schema=self._make_schema(),
            allow_flow_style=True,
            label=self._conv_ctx.as_path_in_datapack()
        )

        for conversation_item in yaml[KEYWORD_CONVERSATION]:
            self._revalidate_conversation_item(conversation_item)

        return yaml.data

    @staticmethod
    def _make_schema():
        return Map({
            KEYWORD_SPEAKER_NAME: Any(),
            KEYWORD_DEFAULT_SPEAK_TIME_SEC: Int(),
            KEYWORD_CONVERSATION: Seq(
                MapPattern(Str(), Any())  # Conversation items validated in revalidation as it is not possible
            )                             # to Or together 2 Map validators
        })

    def _revalidate_conversation_item(self, conversation_item: YAML):
        if KEYWORD_SAY in conversation_item.keys():
            conversation_item.revalidate(
                Map({
                    KEYWORD_SAY: Any(),
                    Optional(KEYWORD_SPEAK_TIME_SEC): Int()
                })
            )

        elif KEYWORD_FUNCTION in conversation_item.keys():
            conversation_item.revalidate(
                Map({
                    KEYWORD_FUNCTION: Str()
                })
            )

        else:
            msg = '\n'.join([
                f'Error in {self._conv_ctx.as_path_in_datapack()} while validating conversation item:',
                str(conversation_item),
            ])
            raise Exception(msg)


class YamlConversationParser:
    def __init__(self, yaml, conversation_context: ConversationContext):
        self.conv_ctx = conversation_context
        self.yaml = yaml
        self.default_speak_time_sec = yaml[KEYWORD_DEFAULT_SPEAK_TIME_SEC]

    def parse_conversation(self) -> Conversation:
        speaker_name = self.yaml[KEYWORD_SPEAKER_NAME]
        yaml_lines = self.yaml[KEYWORD_CONVERSATION]
        lines = [self._read_line(yaml_line) for yaml_line in yaml_lines]

        return Conversation(self.conv_ctx, speaker_name, lines)

    def _read_line(self, yaml_line) -> Line:
        if KEYWORD_SAY in yaml_line.keys():
            return self._read_text_line(yaml_line)
        elif KEYWORD_FUNCTION in yaml_line.keys():
            return self._read_function_line(yaml_line)
        else:
            msg = '\n'.join([
                f'Error in {self.conv_ctx.as_path_in_datapack()} while validating conversation item:',
                str(yaml_line),
                'Incorrectly validated.'
            ])
            raise Exception(msg)

    def _read_text_line(self, yaml_line) -> TextLine:
        text = yaml_line[KEYWORD_SAY]

        if KEYWORD_SPEAK_TIME_SEC in yaml_line:
            speak_time = yaml_line[KEYWORD_SPEAK_TIME_SEC]
        else:
            speak_time = self.default_speak_time_sec

        return TextLine(text, speak_time)

    @staticmethod
    def _read_function_line(yaml_line) -> FunctionLine:
        function_to_call = yaml_line[KEYWORD_FUNCTION]
        return FunctionLine(function_to_call)
