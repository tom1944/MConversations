import os

FUNCTION_FILE_EXTENSION = '.mcfunction'
DATAPACK_DATA_DIR = 'data'
DATAPACK_FUNCTIONS_DIR = 'functions'


class FunctionContext:
    def __init__(self, namespace: str, path_in_functions_dir: str, function_name: str):
        self.namespace = namespace
        self.path_in_functions_dir = path_in_functions_dir.strip(os.sep)
        self.function_name = function_name

    def as_qualified_function_name(self) -> str:
        if self.path_in_functions_dir == '':
            return f'{self.namespace}:{self.function_name}'
        else:
            return f'{self.namespace}:{self.path_in_functions_dir.replace(os.sep, "/")}/{self.function_name}'

    def as_path_to_function_file(self) -> str:
        path = os.path.join(
            DATAPACK_DATA_DIR,
            self.namespace,
            DATAPACK_FUNCTIONS_DIR,
            self.path_in_functions_dir,
        )

        return path.strip(os.sep)

    def as_function_file_name(self) -> str:
        return self.function_name + FUNCTION_FILE_EXTENSION

    def __eq__(self, other):
        if not isinstance(other, FunctionContext):
            return False
        return self.namespace == other.namespace \
            and self.path_in_functions_dir == other.path_in_functions_dir\
            and self.function_name == other.function_name

    def __repr__(self):
        return f'FunctionContext({self.namespace}, {self.path_in_functions_dir}, {self.function_name})'
