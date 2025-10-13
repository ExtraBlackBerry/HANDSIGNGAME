# Seal Strike: Hand Sign Combat Game
This project is an exciting proof-of-concept game that combines Pygame, OpenCV, and MediaPipe to create an immersive combat experience. Players execute spells by performing real-time Naruto-style hand signs captured via their webcam.

## Features
* Real-Time Gesture Control: Utilizes MediaPipe for hand tracking and OpenCV for video processing.

* Spell Execution: Map complex hand sign sequences to in-game abilities, adding a dynamic, physical component to the gameplay.

* Networked Multiplayer: This game is a 1v1 duel using a direct connection between players.

## Getting Started
**Requirements**  
Ensure you have Python 3.7+ installed along with the following libraries, libraries also included in requirements.txt:
* `pygame-ce`
* `opencv-python`
* `mediapipe`

## Installation
1. Clone the repository:
```
git clone [github.com/ExtraBlackBerry/HANDSIGNGAME]
cd Seal-Strike
```
2. Create and activate virtual environment (Recommended):
```
python -m venv venv
.\venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
## How to Run
1. Execute the main game file:
```
python game.py
```

## Development To-Do List 🛠️
This section outlines immediate tasks and future enhancements.

[ ] Win condition
* when player hp hit 0 go to game over screen, clean up all network stuff  
* Restart button, main menu button



[ ] Make sure network is cleaned up when leaving join or host screen so it can restart nice



[ ] Make host wait for joiner player instantiation before allow start  
* send message when created, set game_ready for host when message recieved



[ ] Stop player doing 'hit' animation when enemy casts fail



[ ] Fix animations for other player in fight



[ ] Stop allowing camera controls after death



[ ] Make sequence/skill display area
* how sequence then when executed show spell name



[ ] maybe make controller None for player constructor and only assign p1 controller to speed up host player object instantiation  