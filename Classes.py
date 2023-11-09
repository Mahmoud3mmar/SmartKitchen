
import mediapipe as mp  # Import mediapipe
import cv2  # Import opencv
from dollarpy import Recognizer, Template, Point
# import csv
import os
import numpy as np
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

templates = []  # list of templates for $1 training


def getPoints(videoURL, label):
    cap = cv2.VideoCapture(videoURL)  # web cam =0 , else enter filename
    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        # List to hold Coordinates
        points = []
        left_shoulder = []
        right_shoulder = []
        left_elbos = []
        right_elbos = []
        left_wirst = []
        right_wrist = []
        left_pinky = []
        right_pinky = []
        left_index = []
        right_index = []
        left_hip = []
        right_hip = []

        # List to Plot
        m_left_shoulder = []
        m_right_shoulder = []
        m_left_elbos = []
        m_right_elbos = []
        m_left_wirst = []
        m_right_wrist = []
        m_left_pinky = []
        m_right_pinky = []
        m_left_index = []
        m_right_index = []
        m_left_hip = []
        m_right_hip = []

        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor Feed
            if ret == True:

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make Detections
                results = holistic.process(image)
                # print(results.face_landmarks)

                # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

                # Recolor image back to BGR for rendering
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 2. Right hand
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                          )

                # 3. Left Hand
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                          )

                # 4. Pose Detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                # Export coordinates
                try:
                    # Extract Pose landmarks
                    pose = results.pose_landmarks.landmark
                    index = 0
                    newlist = []
                    for lnd in pose:
                        if (index in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24]):
                            newlist.append(lnd)
                        index += 1

                    # add points of wrist , elbow and shoulder
                    left_shoulder.append(Point(newlist[0].x, newlist[0].y, 1))
                    right_shoulder.append(Point(newlist[1].x, newlist[1].y, 2))
                    left_elbos.append(Point(newlist[2].x, newlist[2].y, 3))
                    right_elbos.append(Point(newlist[3].x, newlist[3].y, 4))
                    left_wirst.append(Point(newlist[4].x, newlist[4].y, 5))
                    right_wrist.append(Point(newlist[5].x, newlist[5].y, 6))
                    left_pinky.append(Point(newlist[6].x, newlist[6].y, 7))
                    right_pinky.append(Point(newlist[7].x, newlist[7].y, 8))
                    left_index.append(Point(newlist[8].x, newlist[8].y, 9))
                    right_index.append(Point(newlist[9].x, newlist[9].y, 10))
                    left_hip.append(Point(newlist[10].x, newlist[10].y, 11))
                    right_hip.append(Point(newlist[11].x, newlist[11].y, 12))

                    m_left_shoulder.append((newlist[0].x, newlist[0].y))
                    m_right_shoulder.append((newlist[1].x, newlist[1].y))
                    m_left_elbos.append((newlist[2].x, newlist[2].y))
                    m_right_elbos.append((newlist[3].x, newlist[3].y))
                    m_left_wirst.append((newlist[4].x, newlist[4].y))
                    m_right_wrist.append((newlist[5].x, newlist[5].y))
                    m_left_pinky.append((newlist[6].x, newlist[6].y))
                    m_right_pinky.append((newlist[7].x, newlist[7].y))
                    m_left_index.append((newlist[8].x, newlist[8].y))
                    m_right_index.append((newlist[9].x, newlist[9].y))
                    m_left_hip.append((newlist[10].x, newlist[10].y))
                    m_right_hip.append((newlist[11].x, newlist[11].y))
                    # Pose Landmarks
                    # pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in newlist]).flatten())

                    # Extract Face landmarks
                    # face = results.face_landmarks.landmark

                    # Concate rows
                    # row = pose_row




                except:
                    pass

                cv2.imshow(label, image)

            if cv2.waitKey(10) & 0xFF == ord('x'):
                break

    cap.release()
    cv2.destroyAllWindows()
    points = left_shoulder + right_shoulder + left_elbos + right_elbos + left_wirst + right_wrist + left_pinky + right_pinky + left_index + right_index + left_hip + right_hip
    print(label)
    xs, ys = zip(*m_left_shoulder)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_right_shoulder)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_left_elbos)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')

    xs, ys = zip(*m_right_elbos)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_left_wirst)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_right_wrist)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')

    xs, ys = zip(*m_left_pinky)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_right_pinky)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_left_index)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')

    xs, ys = zip(*m_right_index)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_left_hip)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')
    xs, ys = zip(*m_right_hip)
    plt.plot(xs, ys, 'o')
    plt.plot(xs, ys, '-')

    plt.gca().invert_yaxis()

    plt.show()

    return points




# Load video and record "Hello" gesture
vid_say_hello = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_14_31_12_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello = getPoints(vid_say_hello, "Hello")
tmpl_hello = Template('Hello', points_hello)
templates.append(tmpl_hello)

# Load video and record "Hello" gesture
vid_say_hello1 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_14_31_15_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello1 = getPoints(vid_say_hello1, "Hello")
tmpl_hello1 = Template('Hello', points_hello1)
templates.append(tmpl_hello1)

# Load video and record "Hello" gesture
vid_say_hello2 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_14_31_21_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello2 = getPoints(vid_say_hello2, "Hello")
tmpl_hello2= Template('Hello', points_hello2)
templates.append(tmpl_hello2)

# Load video and record "Hello" gesture
vid_say_hello3 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_14_31_26_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello3 = getPoints(vid_say_hello3, "Hello")
tmpl_hello3 = Template('Hello', points_hello3)
templates.append(tmpl_hello3)

# Load video and record "Hello" gesture
vid_say_hello4 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_14_31_29_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello4 = getPoints(vid_say_hello4, "Hello")
tmpl_hello4 = Template('Hello', points_hello4)
templates.append(tmpl_hello4)

# Load video and record "Hello" gesture
vid_say_hello5 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_14_31_31_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello5 = getPoints(vid_say_hello5, "Hello")
tmpl_hello5 = Template('Hello', points_hello5)
templates.append(tmpl_hello5)




# Load video and record "Hello" gesture
vid_say_hello6 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_14_40_Pro.mp4" # Replace with the path to the video where you say "Hello"
points_hello6 = getPoints(vid_say_hello6, "Hello")
tmpl_hello6 = Template('Hello', points_hello6)
templates.append(tmpl_hello6)



# Load video and record "Hello" gesture
vid_say_hello7 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_14_43_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello7 = getPoints(vid_say_hello7, "Hello")
tmpl_hello7 = Template('Hello', points_hello7)
templates.append(tmpl_hello7)



# Load video and record "Hello" gesture
vid_say_hello8 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_14_45_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello8 = getPoints(vid_say_hello8, "Hello")
tmpl_hello8 = Template('Hello', points_hello8)
templates.append(tmpl_hello8)


# Load video and record "Hello" gesture
vid_say_hello9 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_14_53_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello9 = getPoints(vid_say_hello9, "Hello")
tmpl_hello9 = Template('Hello', points_hello9)
templates.append(tmpl_hello9)



# Load video and record "Hello" gesture
vid_say_hello10 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_14_56_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello10 = getPoints(vid_say_hello10, "Hello")
tmpl_hello10 = Template('Hello', points_hello10)
templates.append(tmpl_hello10)


# Load video and record "Hello" gesture
vid_say_hello11 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_15_42_Pro.mp4" # Replace with the path to the video where you say "Hello"
points_hello11 = getPoints(vid_say_hello11, "Hello")
tmpl_hello11 = Template('Hello', points_hello11)
templates.append(tmpl_hello11)


# Load video and record "Hello" gesture
vid_say_hello12 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_15_48_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello12 = getPoints(vid_say_hello12, "Hello")
tmpl_hello12 = Template('Hello', points_hello12)
templates.append(tmpl_hello12)

# Load video and record "Hello" gesture
vid_say_hello13= r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_15_53_Pro.mp4"  # Replace with the path to the video where you say "Hello"
points_hello13 = getPoints(vid_say_hello13, "Hello")
tmpl_hello13 = Template('Hello', points_hello13)
templates.append(tmpl_hello13)

# Load video and record "Hello" gesture
vid_say_hello14 = r"C:\Users\mahmo\OneDrive\Pictures\Camera Roll\WIN_20231106_19_15_57_Pro.mp4" # Replace with the path to the video where you say "Hello"
points_hello14 = getPoints(vid_say_hello14, "Hello")
tmpl_hello14 = Template('Hello', points_hello14)
templates.append(tmpl_hello14)



import pickle

# Save the templates array to a file
with open('templates.pkl', 'wb') as file:
    pickle.dump(templates, file)