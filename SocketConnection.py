


import mediapipe as mp
import cv2
import socket
import threading
from Speech_Recognition import speak
def connect():
    # Create a VideoCapture object (cap) to access the webcam.
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # Function to handle a connected client
    def handle_client(client_socket):
        flag=1
        while True:

            # Capture a frame from the webcam
            success, image = cap.read()
            imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the frame to detect hand landmarks
            results = hands.process(imageRGB)

            left_hand_landmarks = None
            right_hand_landmarks = None

            # Check if any hand landmarks are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Determine if it's a left or right hand
                    if hand_landmarks.landmark[0].x < hand_landmarks.landmark[9].x:
                        left_hand_landmarks = hand_landmarks
                    else:
                        right_hand_landmarks = hand_landmarks

            if left_hand_landmarks:
                # Extract and draw landmarks for the left hand
                left_hand_coordinates = extract_landmarks(left_hand_landmarks, image)
                draw_and_print_landmarks(image, left_hand_landmarks, left_hand_coordinates, 'Right Hand', (0, 255, 0))
            if right_hand_landmarks:
                # Extract and draw landmarks for the right hand
                right_hand_coordinates = extract_landmarks(right_hand_landmarks, image)
                draw_and_print_landmarks(image, right_hand_landmarks, right_hand_coordinates, 'Left Hand', (0, 0, 255))
            if left_hand_landmarks and right_hand_landmarks:
                # Send both sets of coordinates to the connected client
                send_coordinates(client_socket, left_hand_coordinates, right_hand_coordinates)
                # Inside the handle_client function or any appropriate location

            # Show the frame with landmarks
            cv2.imshow("Output", image)

            # Check for a key press to exit
            key = cv2.waitKey(1)
            if key == ord('x'):
                break

        client_socket.close()

    # Function to extract landmarks and return their coordinates
    def extract_landmarks(hand_landmarks, image):
        coordinates = []
        for lm in hand_landmarks.landmark:
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            coordinates.extend([cx, cy])
        return coordinates

    # Function to draw landmarks and print their coordinates
    def draw_and_print_landmarks(image, landmarks, coordinates, text, color):
        mpDraw.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.putText(image, text, (coordinates[0], coordinates[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # print(f"{text} Landmarks:", coordinates)

    # Function to send coordinates to the client
    def send_coordinates(client_socket, left_hand_coordinates, right_hand_coordinates):
        coordinates_str = ','.join(map(str, left_hand_coordinates)) + '\n' + ','.join(map(str, right_hand_coordinates))
        client_socket.send(coordinates_str.encode())

    # Function to send a single text message to the client
    # Function to send text messages to the client
    def send_text(client_socket):
        listen=speak()
        while True:
            try:
                # Send a text message to the client
                message = "TEXT:"+listen
                client_socket.send(message.encode())

            except Exception as e:
                print(f"Error sending text: {e}")
                break

    # Create a socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('172.20.10.12', 5000)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Waiting for connections...")

    while True:
        try:
            client, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            # Create a new thread for each connected client to handle data transfer
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()

            # Start a new thread to send text
            client_handler2 = threading.Thread(target=send_text, args=(client,))
            client_handler2.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")
