from typing import NamedTuple


class ConversationContext(NamedTuple):
    namespace: str
    path_in_functions_dir: str
    name: str
