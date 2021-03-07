from typing import NamedTuple


class ConversationContext(NamedTuple):
    namespace: str
    path_in_functions: str
    name: str

    def to_prefix(self) -> str:  # TODO remove
        if self.path_in_functions == "":
            return f'{self.namespace}:'
        else:
            return f'{self.namespace}:{self.path_in_functions}/'
