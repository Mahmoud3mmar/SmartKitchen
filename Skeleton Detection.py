import cv2
import mediapipe as mp

# Initialize Mediapipe
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# Function to process and display skeleton tracking
def track_skeleton():
    cap = cv2.VideoCapture(0)  # Use the default camera (you can specify a video file path if needed)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert the frame to RGB for Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for holistic (skeleton) tracking
        results = holistic.process(frame_rgb)

        if results.pose_landmarks:
            # Draw skeleton landmarks on the frame
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # Display the frame with the skeleton
        cv2.imshow('Skeleton Tracking', frame)

        # Check for keypress
        key = cv2.waitKey(1)

        # Press 'X' to exit
        if key == ord('x') or key == ord('X'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_skeleton()
