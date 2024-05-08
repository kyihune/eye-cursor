import cv2
import dlib
import pyautogui
import os
from gaze_tracking import GazeTracking

def main():
    # Initialize the webcam
    webcam = cv2.VideoCapture(0)

    # Initialize the face detector and landmark predictor
    detector = dlib.get_frontal_face_detector()
    cwd = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.abspath(os.path.join(cwd, "gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat"))
    predictor = dlib.shape_predictor(model_path)

    # Initialize the gaze tracker
    gaze_tracker = GazeTracking()

    # Initialize variables for cursor movement
    move_cursor = True
    prev_face_pos = None
    move_direction = (0, 0)  # Initial movement direction

    while True:
        # Get a new frame from the webcam
        _, frame = webcam.read()

        if frame is None:
            print("Cannot capture frame from camera")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = detector(gray)

        # Process each detected face
        for face in faces:
            # Get the facial landmarks
            landmarks = predictor(gray, face)

            # Calculate the center point of the face
            center_x = (landmarks.part(27).x + landmarks.part(8).x) // 2
            center_y = (landmarks.part(27).y + landmarks.part(8).y) // 2
            face_pos = (center_x, center_y)

            # Draw a circle at the face center
            cv2.circle(frame, face_pos, 5, (0, 255, 0), -1)

            # Calculate the relative movement of the face
            if prev_face_pos is not None:
                delta_x = face_pos[0] - prev_face_pos[0]
                delta_y = face_pos[1] - prev_face_pos[1]
                move_direction = (delta_x, delta_y)  # Update movement direction

            # Update the previous face position
            prev_face_pos = face_pos

        # Move the cursor based on the movement direction
        if move_cursor:
            pyautogui.moveRel(move_direction[0], move_direction[1])

        # Send the frame to GazeTracking to analyze it
        gaze_tracker.refresh(frame)

        # Get the annotated frame from GazeTracking
        annotated_frame = gaze_tracker.annotated_frame()

        # Check if the eye is blinking or not
        text = ""
        if gaze_tracker.is_blinking():
            text = "Blinking"
        elif gaze_tracker.is_right():
            text = "Looking right"
        elif gaze_tracker.is_left():
            text = "Looking left"
        elif gaze_tracker.is_center():
            text = "Looking center"

        # Display the prediction
        cv2.putText(annotated_frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # Display the pupil coordinates
        left_pupil = gaze_tracker.pupil_left_coords()
        right_pupil = gaze_tracker.pupil_right_coords()
        cv2.putText(annotated_frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(annotated_frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        # Display the resulting frame
        cv2.imshow("EyeCursor", annotated_frame)

        # Check for key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            move_cursor = not move_cursor

    # Release the webcam and close the windows
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()