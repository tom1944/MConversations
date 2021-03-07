import os

FUNCTION_FILE_EXTENSION = '.mcfunction'
DATAPACK_DATA_DIR = 'data'
DATAPACK_FUNCTIONS_DIR = 'functions'


class FunctionContext:
    def __init__(self, namespace: str, path_in_functions_dir: str, function_name: str):
        self.namespace = namespace
        self.function_name = function_name
        self.path_in_functions_dir = path_in_functions_dir.strip(os.sep)

    def as_qualified_function_name(self) -> str:
        if self.path_in_functions_dir == '':
            return f'{self.namespace}:{self.function_name}'
        else:
            return f'{self.namespace}:{self.path_in_functions_dir}/{self.function_name}'

    def as_filepath_in_datapack(self) -> str:
        filename = self.function_name + FUNCTION_FILE_EXTENSION

        return os.path.join(
            DATAPACK_DATA_DIR,
            self.namespace,
            DATAPACK_FUNCTIONS_DIR,
            self.path_in_functions_dir,
            filename,
        )

    def function_prefix(self) -> str:  # TODO remove
        if self.path_in_functions_dir == '':
            return f'{self.namespace}:'
        else:
            return f'{self.namespace}:{self.path_in_functions_dir}/'

    def __eq__(self, other):
        if not isinstance(other, FunctionContext):
            return False
        return self.namespace == other.namespace \
            and self.path_in_functions_dir == other.path_in_functions_dir\
            and self.function_name == other.function_name

    def __repr__(self):
        return f'FunctionContext({self.namespace}, {self.path_in_functions_dir}, {self.function_name})'
