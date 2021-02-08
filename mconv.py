import sys

from mconv.create_functions import create_functions
from mconv.parse_conversation import parse_conversation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <conversation_file>')
        exit(-1)

    file_name = sys.argv[1]

    with open(file_name, 'r') as infile:
        yaml = infile.read()

    conversation = parse_conversation(
        conv_name=file_name,
        yaml_conversation=yaml
    )

    functions = create_functions(conversation)

    for func in functions:
        func.export_to_file()
