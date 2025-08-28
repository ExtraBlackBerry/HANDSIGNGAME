import numpy as np
import os
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def normalize_data(landmarks):
    landmarks = np.array(landmarks).reshape(-1,3)
    wrist = landmarks[0]
    normalized = landmarks - wrist
    return normalized.flatten()

def load_samples_into_df(dir_path):
    X = []
    y = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):
            label = filename.split('.')[0]
            file_path = os.path.join(dir_path, filename)
            count = 0
            with open(file_path, 'r') as f:
                for line in f:
                    landmarks = list(map(float, line.strip().split(',')))
                    normalized = normalize_data(landmarks)
                    X.append(normalized)
                    y.append(label)
                    count += 1
    
    return np.array(X), np.array(y)

dir_path = 'dataset/right'
X, y = load_samples_into_df(dir_path)

print(f"Loaded {len(y)} samples from {dir_path}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0, stratify=y)

model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

os.makedirs('models', exist_ok=True)
with open('models/right_hand_sign_model.pkl', 'wb') as f:
    pickle.dump(model, f)