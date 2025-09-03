import cv2
import mediapipe as mp
import numpy as np
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
os.makedirs('dataset/right', exist_ok=True)
os.makedirs('dataset/left', exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label
            
            if hand_label == "Right":
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.extend([landmark.x, landmark.y, landmark.z])

                key = cv2.waitKey(1) & 0xFF

                sign_map ={
                    #Right Hand Signs
                    ord('q') : 'Rat',
                    ord('w') : 'Ox',
                    ord('e') : 'Tiger',
                    ord('a') : 'Hare',
                    ord('s') : 'Dragon',
                    ord('d') : 'Snake',
                    ord('z') : 'Horse',
                    ord('x') : 'Goat',
                    ord('c') : 'Monkey',
                    ord('r') : 'Bird',
                    ord('t') : 'Dog',
                    ord('y') : 'Boar',
                    ord('f') : 'DEFAULT',
                    ord('g') : 'Charge',
                    # 


                }

                if key in sign_map:
                    sign_name = sign_map[key]
                    file_path = f'dataset/right/{sign_name}.txt'
                    with open(file_path, 'a') as f:
                        f.write(','.join(map(str, landmarks)) + '\n')
                    print(f'Saved {sign_name} to {file_path}')

                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, 'Right Hand', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Collecting Samples', frame)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

cap.release()
cv2.destroyAllWindows()