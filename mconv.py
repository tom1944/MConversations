import os
import sys

from mconv.create_functions import create_functions
from mconv.parse_conversation import parse_conversation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <conversation_file>')
        exit(-1)

    file_name = sys.argv[1]
    if not file_name.endswith('.yaml'):
        print(f'File name {file_name} should have .yaml extension')
        exit(-1)

    with open(file_name, 'r') as infile:
        yaml = infile.read()

    conversation = parse_conversation(
        conv_name=os.path.splitext(file_name)[0],
        yaml_conversation=yaml
    )

    functions = create_functions(conversation)

    for func in functions:
        func.export_to_file()