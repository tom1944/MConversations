class Line:
    def __init__(self, text: str, speak_time: int):
        self.text = text
        self.speak_time = speak_time

    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        return self.text == other.text and self.speak_time == other.speak_time
