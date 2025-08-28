import cv2
import mediapipe as mp
import pickle
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def normalize_data(landmarks):
    landmarks = np.array(landmarks).reshape(-1,3)
    wrist = landmarks[0]
    normalized = landmarks - wrist
    return normalized.flatten()


with open('models/right_hand_sign_model.pkl', 'rb') as f:
    model = pickle.load(f)
    labels = model.classes_
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
print("Camera is open:", cap.isOpened())

list_of_skills = {
    "Rat,Dog": "Fireball",
    "Ox,Dragon": "Ice Spike",
    "Tiger,Hare,Snake": "Thunder Strike",
    "Horse,Goat,Monkey": "Earthquake",
    "Bird,Boar,Rat,Ox": "Wind Slash",
    "Dragon,Snake,Dog,Boar,Tiger": "Shadow Burst",
    "Hare,Rat": "Quick Jab",
    "Monkey,Bird": "Sky Cutter",
    "Goat,Boar": "Stone Skin",
    "Horse,Dog": "Guardian Leap",
    "Snake,Ox": "Venom Fang",
    "Dragon,Tiger": "Dragon's Roar",
    "Bird,Hare,Goat": "Healing Breeze",
    "Monkey,Ox,Dog": "Beast Rally",
    "Boar,Tiger,Rat": "Blood Rush",
    "Horse,Snake,Dragon": "Serpent Coil",
    "Ox,Goat,Monkey,Bird": "Spirit Link",
    "Dog,Boar,Bird,Hare": "Lunar Veil",
    "Rat,Ox,Tiger,Hare,Dragon": "Meteor Shower",
    "Snake,Horse,Goat,Monkey,Boar": "Nature's Grasp",
    "Bird,Dog,Tiger": "Lightning Chain",
    "Ox,Snake,Boar": "Iron Wall",
    "Hare,Goat,Dog": "Pack Tactics",
    "Rat,Monkey,Dragon": "Phantom Step",
    "Horse,Boar,Bird": "Tidal Wave",
    "Tiger,Goat,Ox": "Frostbite",
    "Snake,Dog,Rat": "Poison Cloud",
    "Dragon,Bird,Ox": "Solar Flare",
    "Hare,Monkey,Boar": "Mirage Dance",
    "Horse,Goat,Dog,Bird": "Stormcall",
    "Rat,Ox,Dragon": "Inferno",
    "Tiger,Snake,Horse": "Tempest Kick",
    "Goat,Monkey,Bird,Boar": "Seismic Ring",
    "Dog,Boar,Dragon": "Void Pulse",
    "Ox,Hare,Snake,Goat": "Glacier Guard",
    "Rat,Tiger,Monkey,Bird": "Starfall",
    "Horse,Ox,Dog": "War Stomp",
    "Dragon,Goat,Bird": "Phoenix Dive",
    "Snake,Boar,Hare": "Sandstorm",
    "Rat,Dog,Bird,Ox,Tiger": "Arcane Aegis",
}

sign_collection = []
prev_sign = "UNKNOWN"
skill_used = ""

def execute_skill(sign_collection):
    skill = ','.join(sign_collection)
    if skill in list_of_skills.keys():
        return list_of_skills[skill]
        

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    frame = cv2.flip(frame,1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_sign = "UNKNOWN"

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
                normalized = normalize_data(landmarks)
                prob = model.predict_proba([normalized])[0]
                highest_prob_index = np.argmax(prob)

                if prob[highest_prob_index] > 0.6:
                    current_sign = labels[highest_prob_index]
                    if len(sign_collection) == 0 and current_sign != "UNKNOWN" and current_sign != "DEFAULT" and current_sign != "Charge":
                        if prev_sign == current_sign:
                            sign_collection.append(current_sign)
                    elif len(sign_collection) > 0 and sign_collection[-1] != current_sign and current_sign != "UNKNOWN" and current_sign != "DEFAULT" and current_sign != "Charge":
                        if prev_sign == current_sign:
                            sign_collection.append(current_sign)
                    if len(sign_collection) > 0 and current_sign == "DEFAULT":
                        skill_used = execute_skill(sign_collection)                        
                        sign_collection = []
                    if current_sign == "Charge":
                        print("CHARGING MANA")
                    prev_sign = current_sign
                else:
                    current_sign = "UNKNOWN"

            h,w, _ = frame.shape
            cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * w)
            cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * h) - 50

            cv2.putText(frame, f'Sign Collected: {sign_collection}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Skill Used: {skill_used}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()