from typing import List

from mconv.minecraft.function_context import FunctionContext

FUNCTION_FILE_EXTENSION = 'mcfunction'


class Function:
    def __init__(self, commands: List[str], function_context: FunctionContext):
        self.name = function_context.function_name  # TODO inline?
        self.prefix = function_context.function_prefix()  # TODO Remove
        self.commands = commands
        self.context = function_context

    def export_to_file(self):
        file_name = f'{self.name}.{FUNCTION_FILE_EXTENSION}'

        with open(file_name, 'w') as outfile:
            outfile.write('\n'.join(self.commands))

    def get_identifier(self) -> str:
        return self.prefix + self.name

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.name == other.name\
            and self.prefix == other.prefix\
            and self.commands == other.commands

    def __repr__(self):
        return f'Function({self.name}, {self.prefix}, {self.commands})'
