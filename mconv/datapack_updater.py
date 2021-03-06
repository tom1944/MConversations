import os
from typing import Iterator

from mconv.conversation.conversation_context import ConversationContext
from mconv.create_functions import create_functions
from mconv.minecraft_lang.function_context import DATAPACK_DATA_DIR, DATAPACK_FUNCTIONS_DIR
from mconv.parse_conversation import parse_conversation

YAML_EXTENSION = '.yaml'


class DatapackUpdater:
    def __init__(self, datapack_path: str):
        self.datapack_path = datapack_path

    def update_conversations_in_datapack(self):
        old_working_dir = os.getcwd()
        os.chdir(self.datapack_path)
        yaml_files = self._find_yaml_files_in_current_working_dir()

        for yaml_file in yaml_files:
            try:
                FunctionFilesCreator(yaml_file).generate_mcfunction_files_for_yaml_file()
                print(f'Successfully processed {yaml_file}')
            except Exception as e:
                print(f'Exception while processing {yaml_file}: {e}')
        os.chdir(old_working_dir)

    def _find_yaml_files_in_current_working_dir(self) -> Iterator[str]:
        if not os.path.isdir(DATAPACK_DATA_DIR):
            raise DatapackException(f"{self.datapack_path} has no '{DATAPACK_DATA_DIR}' subdirectory")

        for namespace in subdirs(DATAPACK_DATA_DIR):
            functions_dir = os.path.join(DATAPACK_DATA_DIR, namespace, DATAPACK_FUNCTIONS_DIR)
            if os.path.isdir(functions_dir):
                for root, dirs, files in os.walk(functions_dir):
                    for file in files:
                        if file.endswith(YAML_EXTENSION):
                            yield os.path.join(root, file)


def subdirs(dirname: str) -> Iterator[str]:
    with os.scandir(dirname) as it:
        for entry in it:
            if entry.is_dir():
                yield entry.name


class FunctionFilesCreator:
    def __init__(self, yaml_filepath: str):
        self.yaml_filepath = yaml_filepath.strip(os.sep)

    def generate_mcfunction_files_for_yaml_file(self):
        with open(self.yaml_filepath, 'r') as file:
            yaml = file.read()

        context = self._make_conversation_context()

        conversation = parse_conversation(context, yaml)
        functions = create_functions(conversation)

        for function in functions:
            function.export_to_file()

    def _make_conversation_context(self) -> ConversationContext:
        yaml_filepath = self.yaml_filepath
        data_dir, namespace, functions_dir, filepath_in_functions_dir = yaml_filepath.split(os.sep, maxsplit=3)
        if os.sep in filepath_in_functions_dir:
            path, filename = filepath_in_functions_dir.rsplit(os.sep)
        else:
            path = ''
            filename = filepath_in_functions_dir

        if data_dir != DATAPACK_DATA_DIR or functions_dir != DATAPACK_FUNCTIONS_DIR\
                or not filename.endswith(YAML_EXTENSION):
            raise DatapackException(
                f'{yaml_filepath} is not a path to a yaml conversation definition file inside a datapack'
            )

        return ConversationContext(
            namespace,
            path,
            filename.rstrip(YAML_EXTENSION)
        )


class DatapackException(Exception):
    pass
