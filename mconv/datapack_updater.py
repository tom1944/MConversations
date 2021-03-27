import os
from typing import List

from mconv.conversation.conversation_context import ConversationContext
from mconv.conversion_locator import ConversationFileLocator
from mconv.create_functions import create_functions
from mconv.minecraft_lang.function import Function
from mconv.parse_conversation import parse_conversation


class DatapackUpdater:
    def __init__(self, datapack_path: str):
        self.datapack_path = datapack_path

    def update_conversations_in_datapack(self):
        datapack_path = self.datapack_path
        conversation_ctxs = ConversationFileLocator(datapack_path).locate_conversations_in_datapack()

        for ctx in conversation_ctxs:
            yaml = self._read_conversation_file(ctx)

            conversation = parse_conversation(ctx, yaml)
            functions = create_functions(conversation)

            self._write_functions(functions)

    def _read_conversation_file(self, ctx: ConversationContext) -> str:
        path_to_yaml_file = os.path.join(self.datapack_path, ctx.as_path_in_datapack())

        with open(path_to_yaml_file, 'r') as file:
            yaml = file.read()

        return yaml

    def _write_functions(self, functions: List[Function]):
        for function in functions:
            file_name = os.path.join(self.datapack_path, function.context.as_filepath_in_datapack())

            with open(file_name, 'w') as outfile:
                outfile.write('\n'.join(function.commands))
