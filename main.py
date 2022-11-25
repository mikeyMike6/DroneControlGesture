import threading

import cv2
from djitellopy import Tello
from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel

from Enums.Gesture import Gesture
from Enums.Move import Move
from modules.GestureRecognition import GestureRecognition
from modules.GestureBuffer import GestureBuffer
from modules.DroneMovment import Drone


class MainBoxLayout(MDBoxLayout):
    gesture_status = StringProperty()
    battery_status = StringProperty()
    connected = BooleanProperty(False)
    tello = Tello()
    drone = Drone(tello)
    gesture_rec = None
    frame_read = None
    gesture_buffor = GestureBuffer()
    img_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        threading.Thread(target=self.load_model, args=()).start()
        super(MainBoxLayout, self).__init__(**kwargs)

    def start_drone(self, *args, **kwargs):
        if self.connected and not self.drone.in_air:
            threading.Thread(target=self.drone.start, args=()).start()

    def land_drone(self, *args, **kwargs):
        if self.connected and self.drone.in_air:
            threading.Thread(target=self.drone.land, args=()).start()

    def load_model(self):
        print('loading model')
        self.gesture_rec = GestureRecognition()
        print('model loaded')

    def dron_control(self, gesture):
        print(gesture)
        if not self.drone.in_air and gesture == Move.START:
            self.drone.start()
        if self.drone.in_air:
            self.drone.movement(gesture)

    def connect_to_the_drone(self):
        if not self.connected:
            try:
                self.tello.connect()
            except:
                label = MDLabel(text='Unable to connect with drone')
                button = MDRoundFlatButton(text="close")
                layout = MDBoxLayout()
                layout.add_widget(label)
                layout.add_widget(button)
                popup = Popup(
                    title="Error",
                    content=layout,
                    size_hint=(None, None),
                    size=(400, 400))
                button.bind(on_press=popup.dismiss)
                popup.open()
            else:
                self.tello.streamon()
                self.frame_read = self.tello.get_frame_read()
                Clock.schedule_interval(self.get_battery_status, 5)
                Clock.schedule_interval(self.load_video_from_drone, 1.0 / 30.0)
                self.connected = True

    def get_battery_status(self, *args):
        self.battery_status = str(self.tello.get_battery())

    def load_video_from_drone(self, *args):
        if self.connected:
            frame = self.frame_read.frame
            frame, gesture = self.gesture_rec.recognize_gesture_from(frame)
            self.gesture_status = str(gesture)
            buffer = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.img_texture = texture
            self.gesture_buffor.add_gesture(gesture.value)
            move = Move(self.gesture_buffor.get_gesture())
            threading.Thread(target=self.dron_control, args=(move,)).start()

class MainApp(MDApp):
    pass

MainApp().run()