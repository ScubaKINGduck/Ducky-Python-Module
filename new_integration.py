import keyboard, ducky


class Keyboard:
    def __init__(self, fps):
        keyboard.hook(self._update_keys)
        self.pressed_keys = ['']
        self.pressed_keys_types = ['']
        self.fps = fps
        while True:
            # print(self.pressed_keys[len(self.pressed_keys)-1])
            if len(self.pressed_keys) > 50:
                temp = self.pressed_keys[-50:]
                self.pressed_keys = temp
                temp2 = self.pressed_keys_types[-50:]
                self.pressed_keys_types = temp2
            ducky.wait(1000 / self.fps)

    def _update_keys(self, event):
        self.pressed_keys.append(event.name)
        self.pressed_keys_types.append(event.event_type)

    def _is_pressed(self, key: object) -> bool:
        return keyboard.is_pressed(key)


manager = Keyboard(30)