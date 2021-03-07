from typing import List

from mconv.minecraft.function_context import FunctionContext

FUNCTION_FILE_EXTENSION = 'mcfunction'


class Function:
    def __init__(self, commands: List[str], function_context: FunctionContext):
        self.commands = commands
        self.context = function_context

    def export_to_file(self):
        file_name = f'{self.context.function_name}.{FUNCTION_FILE_EXTENSION}'

        with open(file_name, 'w') as outfile:
            outfile.write('\n'.join(self.commands))

    def get_qualified_function_name(self) -> str:
        return self.context.as_qualified_function_name()

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.commands == other.commands\
            and self.context == other.context

    def __repr__(self):
        return f'Function({self.commands}, {self.context})'
