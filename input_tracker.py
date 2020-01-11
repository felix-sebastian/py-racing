class InputTracker:
    _keys_pressed = set()

    @staticmethod
    def handle_key_down(key):
        InputTracker._keys_pressed.add(key)

    @staticmethod
    def handle_key_up(key):
        InputTracker._keys_pressed.remove(key)

    @staticmethod
    def key_pressed(key):
        return key in InputTracker._keys_pressed
