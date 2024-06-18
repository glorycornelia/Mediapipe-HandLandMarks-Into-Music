import cv2
import mediapipe as mp
import pygame

# Initialize pygame
pygame.mixer.init()

# Initialize MediaPipe Hands
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mp_hands=mp.solutions.hands

# Initialize the camera
camera=cv2.VideoCapture(0)

# Initilize key
from detecting_key_realtime import detect_key
inputKey = detect_key()

# Get sounds_mapping
from sounds_mapping import sounds
sounds_mapping = sounds(inputKey)

# Start the hand tracking process
fingerCountBefore = 0
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while camera.isOpened():
        ret, image=camera.read()
        image.flags.writeable=False
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        fingerCount=0

        # If hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                handIndex=results.multi_hand_landmarks.index(hand_landmarks)
                handLabel=results.multi_handedness[handIndex].classification[0].label
                handLandmarks=[]
                for landmarks in hand_landmarks.landmark:
                    handLandmarks.append([landmarks.x, landmarks.y])
                
                # Thumb detection logic
                if handLabel=="Left" and handLandmarks[4][0]>handLandmarks[3][0]:
                    fingerCount=fingerCount+1
                elif handLabel=="Right" and handLandmarks[4][0]<handLandmarks[3][0]:
                    fingerCount=fingerCount+1

                # Finger detection logic for other fingers
                if handLandmarks[8][1]<handLandmarks[6][1]: fingerCount+=1
                if handLandmarks[12][1]<handLandmarks[10][1]: fingerCount+=1
                if handLandmarks[16][1]<handLandmarks[14][1]: fingerCount+=1
                if handLandmarks[20][1]<handLandmarks[18][1]: fingerCount+=1

                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Play sound based on finger count
        if fingerCount == 0 or fingerCount == 9 or fingerCount == 10:
            pygame.mixer.music.stop()
        elif fingerCount == fingerCountBefore:
            continue
        else:
            if fingerCount in sounds_mapping:
                sound_file=sounds_mapping[fingerCount]
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
        
        fingerCountBefore = fingerCount  

         # Display finger count on the screen    
        cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.putText(image, 'key-'+inputKey, (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)
        cv2.imshow('MediaPipe Piano Show', image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

camera.release()
cv2.destroyAllWindows()