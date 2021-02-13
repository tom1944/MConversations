import os
import sys

from mconv.create_functions import create_functions
from mconv.parse_conversation import parse_conversation


def file_name_without_extension(path: str) -> str:
    base = os.path.basename(path)
    return os.path.splitext(base)[0]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <conversation_file>')
        exit(-1)

    path_name = sys.argv[1]
    if not path_name.endswith('.yaml'):
        print(f'File name {path_name} should have .yaml extension')
        exit(-1)

    with open(path_name, 'r') as infile:
        yaml = infile.read()

    conversation = parse_conversation(
        conv_name=file_name_without_extension(path_name),
        yaml_conversation=yaml
    )

    functions = create_functions(conversation)

    for func in functions:
        func.export_to_file()
