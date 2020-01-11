import arcade
import math
from input_tracker import InputTracker


class Car:
    MOVEMENT_SPEED = 0.0001
    STEERING_RATE = 0.02
    TURNING_RATE = 9
    ACCELERATION = 0.6
    TOP_SPEED = 8
    INERTIA_HEADING_CHANGE_RATE = 0.1
    INERTIA_HEADING_CHANGE_RATE_SHIFT = 0.03
    SHOW_VECTOR = False
    VECTOR_INDICATOR_SIZE = 200
    TYRE_SPIN_CURVE = 1 / 2

    def __init__(self, position_x, position_y, heading, color=arcade.color.BLACK):
        self._x = position_x
        self._y = position_y
        self._heading = heading
        self._vector = heading
        self._color = color
        self._speed = 0
        self._steering = 0
        self._sprite = arcade.load_texture("./car.png", 0, 0, 189, 340)

    def draw(self):
        arcade.draw_texture_rectangle(self._x, self._y, 22, 40, self._sprite, self._heading * -1)

        a = 2 * math.pi * self._vector / 360
        magnitude = self.VECTOR_INDICATOR_SIZE * self._speed / self.TOP_SPEED

        if self.SHOW_VECTOR and magnitude > 0:
            arcade.draw_line(self._x, self._y,
                             self._x + math.sin(a) * magnitude,
                             self._y + math.cos(a) * magnitude,
                             arcade.color.RED)

        arcade.draw_text("speed=" + str(round(self._speed, 1)) + " heading=" +
                         str(round(self._heading, 1)) + " vector=" + str(round(self._vector, 1)), 10, 10,
                         arcade.color.DARK_GREEN)

    def _calc_speed(self):
        if InputTracker.key_pressed(arcade.key.UP) and not InputTracker.key_pressed(arcade.key.DOWN):
            throttle = 1
        elif InputTracker.key_pressed(arcade.key.DOWN) and not InputTracker.key_pressed(arcade.key.UP):
            throttle = -1
        else:
            throttle = -0.4

        tyre_spin = abs(pow(1 - (self._heading - self._vector) / 180, self.TYRE_SPIN_CURVE))
        return round(max(min(self._speed + self.ACCELERATION * throttle * tyre_spin, self.TOP_SPEED), 0), 3)

    def _calc_vector(self):
        difference = self._heading - self._vector
        speed_factor = 1 - self._speed / self.TOP_SPEED

        if InputTracker.key_pressed(arcade.key.LSHIFT):
            change_rate = self.INERTIA_HEADING_CHANGE_RATE_SHIFT
        else:
            change_rate = self.INERTIA_HEADING_CHANGE_RATE

        change_amount = round(abs(change_rate + change_rate * pow(speed_factor, 3)), 3)
        return self._vector + change_amount * difference

    def update(self):
        if InputTracker.key_pressed(arcade.key.LEFT) and not InputTracker.key_pressed(arcade.key.RIGHT):
            self._steering = max(self._steering - self.STEERING_RATE, -1)
        elif InputTracker.key_pressed(arcade.key.RIGHT) and not InputTracker.key_pressed(arcade.key.LEFT):
            self._steering = min(self._steering + self.STEERING_RATE, 1)
        else:
            self._steering = self._steering / 2

        if abs(self._steering) < 0.01:
            self._steering = 0

        self._steering = round(self._steering, 3)
        self._heading = round(self._heading + self._steering * self.TURNING_RATE, 3)
        self._x = self._x + self._speed * math.sin(2 * math.pi * self._vector / 360)
        self._y = self._y + self._speed * math.cos(2 * math.pi * self._vector / 360)
        self._vector = self._calc_vector()
        self._speed = self._calc_speed()
