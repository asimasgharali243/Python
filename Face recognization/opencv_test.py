# import cv2
# import mediapipe as mp
# import pyautogui
# import speech_recognition as sr
# import threading
# from collections import deque

# # ------------------ Mediapipe Setup ------------------
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# cap = cv2.VideoCapture(0)

# # ------------------ Gesture Stability ------------------
# gesture_history = deque(maxlen=10)  # store last 10 gestures
# prev_x, prev_y = 0, 0  # for smooth mouse movement

# # ------------------ Voice Commands ------------------
# def voice_listener():
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()

#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("Voice control active. Say something...")

#     while True:
#         try:
#             with mic as source:
#                 audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
#                 command = recognizer.recognize_google(audio).lower()
#                 print("Voice Command:", command)

#                 if "next" in command:
#                     pyautogui.press("right")
#                 elif "previous" in command:
#                     pyautogui.press("left")
#                 elif "pause" in command or "stop" in command:
#                     pyautogui.press("space")
#                 elif "play" in command or "resume" in command:
#                     pyautogui.press("playpause")
#                 elif "volume up" in command:
#                     pyautogui.press("volumeup")
#                 elif "volume down" in command:
#                     pyautogui.press("volumedown")
#                 elif "exit" in command or "quit" in command:
#                     print("Voice: Exit Command Detected")
#                     break

#         except sr.WaitTimeoutError:
#             continue
#         except sr.UnknownValueError:
#             print("Voice not recognized, try again...")
#         except Exception as e:
#             print("Voice Error:", str(e))

# # Run voice recognition in background
# voice_thread = threading.Thread(target=voice_listener, daemon=True)
# voice_thread.start()

# # ------------------ Finger Counting ------------------
# def count_fingers(hand_landmarks, handedness):
#     finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
#     finger_pips = [6, 10, 14, 18]  # PIP joints
#     count = 0
#     threshold = 0.02  # tolerance

#     for tip, pip in zip(finger_tips, finger_pips):
#         if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y - threshold:
#             count += 1

#     # Thumb check (depends on left/right hand)
#     if handedness == "Right":
#         if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x - threshold:
#             count += 1
#     else:  # Left hand
#         if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x + threshold:
#             count += 1

#     return count

# # ------------------ Main Loop ------------------
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(rgb)

#     if results.multi_hand_landmarks:
#         for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
#             mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             handedness = results.multi_handedness[idx].classification[0].label
#             fingers = count_fingers(hand_landmarks, handedness)
#             gesture_history.append(fingers)

#             if gesture_history.count(fingers) > 7:
#                 current_gesture = fingers

#                 if current_gesture == 0:  # ✊ Fist
#                     cv2.putText(frame, "Stop / Pause", (50, 100),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#                     # pyautogui.press("space")

#                 elif current_gesture == 1:  # ☝ One finger
#                     cv2.putText(frame, "Next Slide", (50, 100),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#                     # pyautogui.press("right")

#                     index_tip = hand_landmarks.landmark[8]
#                     h, w, _ = frame.shape
#                     x, y = int(index_tip.x * w), int(index_tip.y * h)

#                     smooth_factor = 0.2
#                     prev_x = prev_x + (x - prev_x) * smooth_factor
#                     prev_y = prev_y + (y - prev_y) * smooth_factor
#                     pyautogui.moveTo(int(prev_x * 3), int(prev_y * 3))
#                     cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)

#                 elif current_gesture == 2:  # ✌ Two fingers
#                     cv2.putText(frame, "Previous Slide", (50, 100),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
#                     # pyautogui.press("left")

#                 elif current_gesture == 3:  # Three fingers
#                     cv2.putText(frame, "Volume Up", (50, 100),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#                     # pyautogui.press("volumeup")

#                 elif current_gesture == 4:  # Four fingers
#                     cv2.putText(frame, "Volume Down", (50, 100),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
#                     # pyautogui.press("volumedown")

#                 elif current_gesture == 5:  # 🖐 Palm
#                     cv2.putText(frame, "Play / Resume", (50, 100),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#                     # pyautogui.press("playpause")

#     cv2.imshow("Hand + Voice Gesture Control", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()
 

import cv2
import mediapipe as mp
import pyautogui
import threading
from collections import deque
import queue
import sounddevice as sd
import vosk
import json
import os

# ------------------ Mediapipe Setup ------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# ------------------ Gesture Stability ------------------
gesture_history = deque(maxlen=10)
prev_x, prev_y = 0, 0

# ------------------ Vosk Voice Recognition Setup ------------------
model_path = "models/vosk-model-small-en-us-0.15"  # path to vosk model
if not os.path.exists(model_path):
    raise FileNotFoundError("Vosk model not found. Please download and extract it to: " + model_path)

vosk_model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def voice_listener():
    rec = vosk.KaldiRecognizer(vosk_model, 16000)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        print("🎤 Offline Voice Control active. Speak commands...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "text" in result and result["text"] != "":
                    command = result["text"].lower()
                    print("Voice Command:", command)

                    if "next" in command:
                        pyautogui.press("right")
                    elif "previous" in command:
                        pyautogui.press("left")
                    elif "pause" in command or "stop" in command:
                        pyautogui.press("space")
                    elif "play" in command or "resume" in command:
                        pyautogui.press("playpause")
                    elif "volume up" in command:
                        pyautogui.press("volumeup")
                    elif "volume down" in command:
                        pyautogui.press("volumedown")
                    elif "exit" in command or "quit" in command:
                        print("Voice: Exit Command Detected")
                        break

# Run voice recognition in background
voice_thread = threading.Thread(target=voice_listener, daemon=True)
voice_thread.start()

# ------------------ Finger Counting ------------------
def count_fingers(hand_landmarks, handedness):
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    count = 0
    threshold = 0.02

    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y - threshold:
            count += 1

    if handedness == "Right":
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x - threshold:
            count += 1
    else:
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x + threshold:
            count += 1

    return count

# ------------------ Main Loop ------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            handedness = results.multi_handedness[idx].classification[0].label
            fingers = count_fingers(hand_landmarks, handedness)
            gesture_history.append(fingers)

            if gesture_history.count(fingers) > 7:
                current_gesture = fingers

                if current_gesture == 0:  # Fist
                    cv2.putText(frame, "Stop / Pause", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                elif current_gesture == 1:  # One finger (Mouse control + Next)
                    cv2.putText(frame, "Next Slide", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    index_tip = hand_landmarks.landmark[8]
                    h, w, _ = frame.shape
                    x, y = int(index_tip.x * w), int(index_tip.y * h)

                    smooth_factor = 0.2
                    prev_x = prev_x + (x - prev_x) * smooth_factor
                    prev_y = prev_y + (y - prev_y) * smooth_factor
                    pyautogui.moveTo(int(prev_x * 3), int(prev_y * 3))
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)

                elif current_gesture == 2:
                    cv2.putText(frame, "Previous Slide", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                elif current_gesture == 3:
                    cv2.putText(frame, "Volume Up", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                elif current_gesture == 4:
                    cv2.putText(frame, "Volume Down", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                elif current_gesture == 5:
                    cv2.putText(frame, "Play / Resume", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Hand + Voice Gesture Control (Offline)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

