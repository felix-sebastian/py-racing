import arcade
from constants import Constants
from car import Car
from input_tracker import InputTracker


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.set_update_rate(1 / 30)
        arcade.set_background_color(arcade.color.WHITE)
        self.pressed_keys = set()
        self.car = Car(50, 50, 0)

    def on_draw(self):
        arcade.start_render()
        self.car.draw()

    def on_update(self, delta_time):
        self.car.update()

    def on_key_press(self, key, modifiers):
        InputTracker.handle_key_down(key)

    def on_key_release(self, key, modifiers):
        InputTracker.handle_key_up(key)


MyGame(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Racer")
arcade.run()
