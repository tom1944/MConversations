from mconv.minecraft_lang.json_text import JSONText


class Line:
    pass


class TextLine(Line):
    def __init__(self, text: JSONText, speak_time: int):
        self.text = text
        self.speak_time = speak_time

    def __eq__(self, other):
        if not isinstance(other, TextLine):
            return False
        return self.text == other.text and self.speak_time == other.speak_time


class FunctionLine(Line):
    def __init__(self, qualified_function_name: str):
        self.qualified_function_name = qualified_function_name

    def __eq__(self, other):
        if not isinstance(other, FunctionLine):
            return False
        return self.qualified_function_name == other.qualified_function_name
