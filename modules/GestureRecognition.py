import copy
import csv
import itertools
import os

import cv2
import mediapipe as mp
import numpy as np

from classifier.classifier import Classifier
from Enums.Gesture import Gesture


def normalize_landmarks(image, landmarks):
    width, height, _ = image.shape
    tmp_landmark = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * width), width - 1)
        landmark_y = min(int(landmark.y * height), height - 1)
        tmp_landmark.append([landmark_x, landmark_y])

    temp_landmark_list = copy.deepcopy(tmp_landmark)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # konwersja na liste jednowymiarową
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # normalizacja do wartosci od 0 do 1
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def calculate_bounding(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


class GestureRecognition:
    def __init__(self):
        self.hand, self.classifier, self.gesture_labels, = self.load_model()

    def load_model(self):
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            max_num_hands=1
        )
        classifier = Classifier()
        # load labels

        # do testów, normalnie nie używac pełnej ściezki
        # with open(os.path.join(os.getcwd(), 'gesture_labels.csv'), encoding='utf-8-sig') as file:
        with open(r'modules/gesture_labels.csv', encoding='utf-8-sig') as file:
            self.gesture_labels = csv.reader(file)
            self.gesture_labels = [
                row[0] for row in self.gesture_labels
            ]
        return hands, classifier, self.gesture_labels

    def recognize_gesture_from(self, image, draw=True):
        image = cv2.flip(image, 1)
        image_copy = copy.deepcopy(image)

        gesture = Gesture.NONE
        gesture_id = -1
        finger_landmarks_y = 0

        # detekcja
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.hand.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                normalized_landmarks = normalize_landmarks(image_copy, hand_landmarks)
                gesture_id = self.classifier(normalized_landmarks)
                finger_landmarks_y = hand_landmarks.landmark[8].x
                if draw:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image_copy,
                        hand_landmarks,
                        mp.solutions.hands.HAND_CONNECTIONS,
                        mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                        mp.solutions.drawing_styles.get_default_hand_connections_style()
                    )
                    rectangle_points = calculate_bounding(image_copy, hand_landmarks)
                    image_copy = cv2.rectangle(image_copy, (rectangle_points[0], rectangle_points[1]),
                                               (rectangle_points[2], rectangle_points[3]), (0, 0, 0), 2)
        if gesture_id == 0:
            gesture = Gesture.FINGER_UP
            if draw:
                height, weight, _ = image_copy.shape
                cv2.line(image_copy, (int(weight / 3), 0), (int(weight / 3), height), (255, 255, 255), 2)
                cv2.line(image_copy, (int(weight / 3) * 2, 0), (int(weight / 3) * 2, height), (255, 255, 255), 2)
            if finger_landmarks_y < 0.3:
                gesture = Gesture.FINGER_UP_LEFT
            elif finger_landmarks_y > 0.6:
                gesture = Gesture.FINGER_UP_RIGHT
        else:
            gesture = Gesture(gesture_id)
        return image_copy, gesture

