import cv2
import mediapipe as mp
import pickle
import numpy as np

class PlayerController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.player = None  # Set to the player using this controller
        self.on_skill = None  # Set from play screen to update players stats

        with open('models/right_hand_sign_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
            self.labels = self.model.classes_
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.frame = None
        self.capture = None
        self.rgb_frame = None
        self.sign_collection = []
        self.prev_sign = "UNKNOWN"
        self.skill_used = ""
        self.list_of_skills = {
            "Rat" : {"skill_name": "Fireball", "mana_cost": 2, "damage": 220}, # was: Boar, Monkey, Rat, Dog, changed for quick test
            "Ox, Dragon, Tiger" : {"skill_name": "Ice Spike", "mana_cost": 3, "damage": 25},
            "Hare, Snake" : {"skill_name": "Thunder Strike", "mana_cost": 4, "damage": 30},
            "Horse, Goat" : {"skill_name": "Earthquake", "mana_cost": 5, "damage": 35},
            "Bird, Boar, Rat, Ox" : {"skill_name": "Wind Slash", "mana_cost": 3, "damage": 20}
        }

    def load_skills(self, skills_dict):
        self.list_of_skills = skills_dict

    def execute_skill(self, skill_name):
        self.skill = ','.join(self.sign_collection)
        if self.skill in self.list_of_skills.keys():       
            return self.list_of_skills[self.skill]
        # If no skill matched, return default no skill, None was an issue
        return {"skill_name": "Fail", "mana_cost": 0, "damage": 0}
    
    def normalize_data(self, landmarks):
        landmarks = np.array(landmarks).reshape(-1,3)
        wrist = landmarks[0]
        normalized = landmarks - wrist
        return normalized.flatten()
        
    def start_capture(self):
        self.capture = cv2.VideoCapture(0)
        pass
    
    def stop_capture(self):
        if self.capture is not None and self.capture.isOpened():
            self.capture.release()
        self.capture = None
        
    def get_current_frame(self):
        if self.capture is None or not self.capture.isOpened():
            return None
        capture_successful, frame = self.capture.read()
        if not capture_successful:
            return None
        frame = cv2.flip(frame, 1)
        self.rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame = frame
        return frame
    
    def control_loop(self):
        self.get_current_frame()
        results = self.hands.process(self.rgb_frame)

        if results.multi_hand_landmarks and results.multi_handedness:
            for i, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
                hand_label = handedness.classification[0].label
                hand_confidence = handedness.classification[0].score
                if hand_label == "Right":
                    landmarks = []
                    for land in hand_landmarks.landmark:
                        landmarks.append(land.x)
                        landmarks.append(land.y)
                        landmarks.append(land.z)
                    normalized = self.normalize_data(landmarks)
                    prob = self.model.predict_proba([normalized])[0]
                    highest_prob_index = np.argmax(prob)

                    if prob[highest_prob_index] > 0.6:
                        current_sign = self.labels[highest_prob_index]
                        if len(self.sign_collection) == 0 and current_sign != "UNKNOWN" and current_sign != "DEFAULT" and current_sign != "Charge":
                            if self.prev_sign == current_sign:
                                self.sign_collection.append(current_sign)
                        elif len(self.sign_collection) > 0 and self.sign_collection[-1] != current_sign and current_sign != "UNKNOWN" and current_sign != "DEFAULT" and current_sign != "Charge":
                            if self.prev_sign == current_sign:
                                self.sign_collection.append(current_sign)
                        # Skill execution
                        if len(self.sign_collection) > 0 and current_sign == "DEFAULT":
                            # Execute stored sequence, then clear collection
                            self.skill_used = self.execute_skill(self.sign_collection)
                            self.sign_collection = []
                            # Check if enough mana, if not fail
                            if self.player is not None:
                                if self.on_skill is not None:
                                    self.on_skill(self.player, self.skill_used)
                                # Play animation based on skill success or fail
                                self.player.play_animation('stomping' if self.skill_used['skill_name'] == "Fail" else 'attack')
                                
                        if current_sign == "Charge":
                            print("CHARGING MANA")
                        self.prev_sign = current_sign
                    else:
                        current_sign = "UNKNOWN"

                h,w, _ = self.frame.shape
                cx = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * w)
                cy = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * h) - 50

                cv2.putText(self.frame, f'Sign Collected: {self.sign_collection}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(self.frame, f'Skill Used: {self.skill_used}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        return self.frame
