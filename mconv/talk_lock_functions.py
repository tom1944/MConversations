from typing import List

from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext

GLOBAL_NAMESPACE = 'zzz_mconv'
GLOBAL_OBJECTIVE = 'zzz_mconv'
TALK_LOCK_TARGET = '%talk_lock'
INIT = 'init'


def make_talk_lock_functions() -> List[Function]:
    return [
        _make_init_function(),
        _make_lock_talk_lock_function(),
        _make_free_talk_lock_function(),
    ]


def _make_init_function() -> Function:
    return Function(
        [
            f'scoreboard objectives add {GLOBAL_OBJECTIVE} dummy',
            f'scoreboard players set {TALK_LOCK_TARGET} {GLOBAL_OBJECTIVE} 0'
        ],
        _make_function_context(INIT)
    )


def _make_lock_talk_lock_function() -> Function:
    return Function(
        [
            f'scoreboard players set {TALK_LOCK_TARGET} {GLOBAL_OBJECTIVE} 0'
        ],
        _make_function_context('lock_talk_lock')
    )


def _make_free_talk_lock_function() -> Function:
    return Function(
        [
            f'scoreboard players set {TALK_LOCK_TARGET} {GLOBAL_OBJECTIVE} 1'
        ],
        _make_function_context('free_talk_lock')
    )


def _make_function_context(function_name: str) -> FunctionContext:
    return FunctionContext(GLOBAL_NAMESPACE, '', function_name)
