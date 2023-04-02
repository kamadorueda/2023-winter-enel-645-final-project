import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import (
    keras,
)
import time

class_names = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "del",
    "nothing",
    "space",
]

# Recreate the exact same model, including its weights and the optimizer
asl_model = tf.keras.models.load_model("training_classifier_asl.h5")

# Show the model architecture
asl_model.summary()


mp_drawing_util = mp.solutions.drawing_utils
mediapipe_hands = mp.solutions.hands
hands_model = mediapipe_hands.Hands()

video_capture = cv2.VideoCapture(0)
read_successful, frame = video_capture.read()
height, width, channels = frame.shape

analysisframe = ""
predicted_class = "None"
hand_counter = 0
probability = 0.0

while True:
    read_successful, frame = video_capture.read()

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands_model.process(framergb)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        hand_counter += 1
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = width
            y_min = height
            for lm in handLMs.landmark:
                x, y = int(lm.x * width), int(lm.y * height)
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)

            y_min = max(0, y_min - 20)
            y_max = min(height, y_max + 20)
            x_min = max(0, x_min - 20)
            x_max = min(width, x_max + 20)
            
            cv2.rectangle(
                frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2
            )
            mp_drawing_util.draw_landmarks(
                frame, handLMs, mediapipe_hands.HAND_CONNECTIONS
            )

            # Define the label text and its position
            label_text = f"Last Prediction: {predicted_class} with probability {round(probability, 2)*100}"
            label_pos = (
                x_min,
                y_min - 10,
            )  # Place the label above the rectangle

            # Draw the rectangle and the label on the image
            cv2.rectangle(
                frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2
            )
            cv2.putText(
                frame,
                label_text,
                label_pos,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    key_press = cv2.waitKey(1)
    if key_press % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    elif hand_counter >= 10:
        # SPACE pressed
        print(x_min, x_max, y_min, y_max)
        # analysisframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        analysisframe = framergb[y_min:y_max, x_min:x_max]
        print(f"framergb shape is {analysisframe.shape}")
        analysisframe = cv2.resize(analysisframe, (224, 224))
        print(f"framergb type is {type(analysisframe)}")
        rows, cols, channels = framergb.shape
        analysisframe = cv2.cvtColor(analysisframe, cv2.COLOR_RGB2BGR)
        cv2.imshow("image", analysisframe)
        image_batch_size_1 = np.expand_dims(analysisframe, axis=0)
        print(
            f"before passing to model, analysisframe shape is {image_batch_size_1.shape}"
        )

        prediction_array = asl_model.predict(image_batch_size_1)[0]

        predicted_class = class_names[np.argmax(prediction_array)]
        probability = prediction_array[np.argmax(prediction_array)]

        print(
            f"prediction is {predicted_class} with probability {probability}"
        )
        hand_counter = 0

    cv2.imshow("Video", frame)
    cv2.imwrite("image.png", frame)

# video_capture.release()
# cv2.destroyAllWindows()
