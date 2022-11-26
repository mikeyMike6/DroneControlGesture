from djitellopy import Tello
from Enums.Move import Move

class Drone:
    def __init__(self, tello: Tello):
        self.in_air = False
        self.tello = tello
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0
        self.speed = 30

    def start(self, *args, **kwargs):
        print('start')
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0
        self.tello.takeoff()
        self.in_air = True

    def land(self, *args, **kwargs):
        print('land')
        self.in_air = False
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0
        self.tello.land()

    def forward(self):
        self.forw_back_velocity = self.speed

    def stop(self):
        self.forw_back_velocity = 0
        self.up_down_velocity = 0
        self.left_right_velocity = 0
        self.yaw_velocity = 0

    def back(self):
        self.forw_back_velocity = -self.speed

    def left(self):
        self.left_right_velocity = self.speed

    def right(self):
        self.left_right_velocity = -self.speed

    def up(self):
        self.up_down_velocity = self.speed

    def down(self):
        self.up_down_velocity = -self.speed

    def left_turn(self):
        self.yaw_velocity = self.speed

    def right_turn(self):
        self.yaw_velocity = -self.speed

    def movement(self, move: Move):
        if move != Move.NONE:
            print('movement is ' + str(move))
        if move != move.NONE:
            if self.in_air:
                if move == Move.STOP:
                    self.stop()
                elif move == Move.UP:
                    self.up()
                elif move == Move.DOWN:
                    self.down()
                elif move == Move.TURN_LEFT:
                    self.left_turn()
                elif move == Move.TURN_RIGHT:
                    self.right_turn()
                elif move == Move.LEFT:
                    self.left()
                elif move == Move.RIGHT:
                    self.right()
                elif move == Move.FORWARD:
                    self.forward()
                elif move == Move.BACKWARD:
                    self.back()
                else:
                    self.stop()
        else:
            self.stop()
        self.tello.send_rc_control(self.left_right_velocity, self.forw_back_velocity,
                                   self.up_down_velocity, self.yaw_velocity)

