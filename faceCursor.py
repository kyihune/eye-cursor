import cv2
import dlib
import pyautogui
import os
import time
from gaze_tracking import GazeTracking

def open_browser():
    pyautogui.press('win')
    #time.sleep(1) 
    pyautogui.write('browser')
    #time.sleep(1)
    pyautogui.press('enter')

def close_browser():
    pyautogui.hotkey('ctrl', 'w')

def left_click():
    pyautogui.click(button='left')

def main():
    # Initialize the webcam
    webcam = cv2.VideoCapture(0)

    pyautogui.FAILSAFE = False
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
    smoothed_face_pos = None
    move_direction = (0, 0)  # Initial movement direction
    smoothing_factor = 0.5  # Adjust this value for smoothing (0 < smoothing_factor < 1)
    movement_threshold = 10  # Adjust this value to change the movement threshold

    # Initialize variables for eye closure detection
    both_eyes_closed_start_time = None
    eyes_closed_start_time = None
    browser_opened = False
    blinking_threshold = 5.0  # Adjust this value to change the blinking sensitivity

    while True:
        # Get a new frame from the webcam
        _, frame = webcam.read()
        frame = cv2.flip(frame, 1)
        if frame is None:
            print("Cannot capture frame from camera")
            break

        # Get the frame dimensions
        frame_height, frame_width, _ = frame.shape

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
            center_y = (landmarks.part(1).y + landmarks.part(15).y) // 2
            face_pos = (center_x, center_y)

            # Draw a circle at the face center
            cv2.circle(frame, face_pos, 5, (0, 255, 0), -1)

            # Apply smoothing to the face position
            if smoothed_face_pos is None:
                smoothed_face_pos = face_pos
            else:
                smoothed_face_pos = (
                    int(smoothing_factor * face_pos[0] + (1 - smoothing_factor) * smoothed_face_pos[0]),
                    int(smoothing_factor * face_pos[1] + (1 - smoothing_factor) * smoothed_face_pos[1])
                )

            # Calculate the movement offset based on the smoothed face position
            if prev_face_pos is not None:
                delta_x = smoothed_face_pos[0] - prev_face_pos[0]
                delta_y = smoothed_face_pos[1] - prev_face_pos[1]

                # Check if the face movement exceeds the threshold
                if abs(delta_x) > movement_threshold or abs(delta_y) > movement_threshold:
                    move_direction = (delta_x, delta_y)
                else:
                    move_direction = (0, 0)  # Stop moving the cursor

            # Update the previous face position
            prev_face_pos = smoothed_face_pos

        # Move the cursor based on the movement direction
        if move_cursor:
            pyautogui.moveRel(move_direction[0], move_direction[1])

        # Send the frame to GazeTracking to analyze it
        gaze_tracker.refresh(frame)

        # Get the annotated frame from GazeTracking
        annotated_frame = gaze_tracker.annotated_frame()

        # Initialize the eye closure text
        text = "Eyes open"

        # # Check if both eyes are closed
        if gaze_tracker.is_blinking(threshold=blinking_threshold):
            if both_eyes_closed_start_time is None:
                both_eyes_closed_start_time = time.time()
            both_eyes_closed_duration = time.time() - both_eyes_closed_start_time

            # Update the eye closure text
            text = "Both eyes closed"

            # Open the browser if both eyes are closed for 2 seconds
            if not browser_opened and both_eyes_closed_duration >= 2:
                open_browser()
                browser_opened = True

            # Close the browser if both eyes are closed for 4 seconds
            elif browser_opened and both_eyes_closed_duration >= 4:
                close_browser()
                browser_opened = False
        else:
            both_eyes_closed_start_time = None

        # Check if eyes are closed for left-click
        if gaze_tracker.is_blinking(threshold=blinking_threshold) and browser_opened:
            if eyes_closed_start_time is None:
                eyes_closed_start_time = time.time()
            eyes_closed_duration = time.time() - eyes_closed_start_time

            # Perform left-click if eyes are closed for 1 second
            if eyes_closed_duration >= 2:
                left_click()
        else:
            eyes_closed_start_time = None

        # Display the eye closure text
        cv2.putText(annotated_frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # Display the resulting frame
        cv2.imshow("FaceCursor", annotated_frame)

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