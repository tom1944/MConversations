import os
from typing import List, Iterator

from mconv.constants import YAML_EXTENSION
from mconv.conversation.conversation_context import ConversationContext
from mconv.minecraft_lang.function_context import DATAPACK_DATA_DIR, DATAPACK_FUNCTIONS_DIR


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
