import unittest
import cv2
from Enums.Gesture import Gesture
from modules.GestureRecognition import GestureRecognition


class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = GestureRecognition()


class TestGestureRecognitonFingerUp(TestModel):
    def runTest(self):
        self.thumbUpImg = cv2.imread(r'modules/tests/fingerup.jpg')
        _, gesture = self.model.recognize_gesture_from(self.thumbUpImg, draw=False)
        self.assertEqual(gesture, Gesture.FINGER_UP)


class TestGestureRecognitonThumbUp(TestModel):
    def runTest(self):
        self.thumbUpImg = cv2.imread(r'modules/tests/thumb_up.jpg')
        _, gesture = self.model.recognize_gesture_from(self.thumbUpImg, draw=False)
        self.assertEqual(gesture, Gesture.THUMB_UP)

