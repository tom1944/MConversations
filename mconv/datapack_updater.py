import os
from typing import Iterator, List

from mconv.conversation.conversation_context import ConversationContext
from mconv.create_functions import create_functions
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import DATAPACK_DATA_DIR, DATAPACK_FUNCTIONS_DIR
from mconv.parse_conversation import parse_conversation

YAML_EXTENSION = '.yaml'


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


class ConversationFileLocator:
    def __init__(self, datapack_path: str):
        self._datapack_path = datapack_path

    def locate_conversations_in_datapack(self) -> List[ConversationContext]:
        datapack_path = self._datapack_path

        if not os.path.isdir(datapack_path):
            raise DatapackException(f"{datapack_path} is not a directory")

        return list(self._locate_conversations_in_datapack())

    def _locate_conversations_in_datapack(self) -> Iterator[ConversationContext]:
        datapack_path = self._datapack_path
        path_to_data_dir = os.path.join(datapack_path, DATAPACK_DATA_DIR)

        if not os.path.isdir(path_to_data_dir):
            raise DatapackException(f"{datapack_path} has no '{DATAPACK_DATA_DIR}' subdirectory")

        for namespace in subdirs(path_to_data_dir):
            path_to_functions_dir = os.path.join(path_to_data_dir, namespace, DATAPACK_FUNCTIONS_DIR)
            yield from self._locate_conversations_in_functions_dir(namespace, path_to_functions_dir)

    @staticmethod
    def _locate_conversations_in_functions_dir(namespace: str, path_to_functions_dir: str)\
            -> Iterator[ConversationContext]:

        if os.path.isdir(path_to_functions_dir):  # Check if the functions dir exists
            for root, _, files in os.walk(path_to_functions_dir):
                for file in files:
                    if file.endswith(YAML_EXTENSION):
                        conversation_name = file.removesuffix(YAML_EXTENSION)

                        path_in_functions_dir = root.removeprefix(path_to_functions_dir).strip(os.sep)

                        yield ConversationContext(
                            namespace,
                            path_in_functions_dir,
                            conversation_name
                        )


def subdirs(dirname: str) -> Iterator[str]:
    with os.scandir(dirname) as it:
        for entry in it:
            entry: os.DirEntry
            if entry.is_dir():
                yield entry.name


class DatapackException(Exception):
    pass
