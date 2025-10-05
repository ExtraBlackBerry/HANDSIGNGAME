import cv2
import mediapipe as mp
import pickle
import numpy as np

class PlayerController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        with open('models/right_hand_sign_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
            self.labels = self.model.classes_
        
        self.hads = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
        self.capture = cv2.VideoCapture(0)

        self.sign_collection = []
        self.prev_sign = "UNKNOWN"
        self.skill_used = ""
        self.list_of_skills = {}

    def execute_skill(self, skill_name):
        self.skill = ','.join(self.sign_collection)
        if self.skill in self.list_of_skills.keys():
            return self.ist_of_skills[self.skill]