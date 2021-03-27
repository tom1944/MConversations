import os
from typing import NamedTuple

from mconv.minecraft_lang.function_context import DATAPACK_DATA_DIR, DATAPACK_FUNCTIONS_DIR

YAML_EXTENSION = '.yaml'


class ConversationContext(NamedTuple):
    namespace: str
    path_in_functions_dir: str
    name: str

    def as_path_in_datapack(self) -> str:
        return os.path.join(
            DATAPACK_DATA_DIR,
            self.namespace,
            DATAPACK_FUNCTIONS_DIR,
            self.path_in_functions_dir,
            self.name + YAML_EXTENSION
        )
