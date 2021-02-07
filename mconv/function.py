from typing import List

FUNCTION_FILE_EXTENSION = 'mcfunction'


class Function:
    def __init__(self, name: str, prefix: str, commands: List[str]):
        self.name = name
        self.prefix = prefix
        self.commands = commands

    def export_to_file(self):
        file_name = f'{self.name}.{FUNCTION_FILE_EXTENSION}'

        with open(file_name, 'w') as outfile:
            outfile.writelines(self.commands)

    def get_function_identifier(self) -> str:
        return self.prefix + self.name

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.name == other.name\
            and self.prefix == other.prefix\
            and self.commands == other.commands
