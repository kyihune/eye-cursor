import cv2
import dlib
import pyautogui
import os
import time
from gaze_tracking import GazeTracking



def left_click():
    pyautogui.click(buttom="left")

def main():
    # Initialize the webcam
    webcam = cv2.VideoCapture(0)

    # This failsafe crashes the program when the mouse is in a corner if it is true
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
    prev_eye_pos = None
    move_direction = (0, 0)  # Initial movement direction
    width, height = pyautogui.size()
    smoothing_factor = .6
    blink_threshold = 5.0
    movement_threshold = 1.5
    blink_timer_start = None
    blink_duration = None



    #max_eye_positions = estimation_calibration()

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
            center_y = (landmarks.part(1).y + landmarks.part(15).y) // 2
            face_pos = (center_x, center_y)

            # Draw a circle at the face center
            cv2.circle(frame, face_pos, 5, (0, 255, 0), -1)

            # Calculate the relative movement of the face

        #    if prev_face_pos is not None:
        #        delta_x = face_pos[0] - prev_face_pos[0]
        #        delta_y = face_pos[1] - prev_face_pos[1]
        #        move_direction = (delta_x, delta_y)  # Update movement direction

            # Update the previous face position
        #    prev_face_pos = face_pos

        left_eye_pos = gaze_tracker.pupil_left_coords()
        right_eye_pos = gaze_tracker.pupil_right_coords()


        if prev_eye_pos != None and left_eye_pos != None and right_eye_pos != None:

            eye_delta_x = prev_eye_pos[0] - (left_eye_pos[0] + right_eye_pos[0])/2
            eye_delta_y = prev_eye_pos[1] - (left_eye_pos[1] + right_eye_pos[1])/2

            move_direction = (int(eye_delta_x/15 * width * smoothing_factor), int(eye_delta_y/10 * height * (smoothing_factor * .45))) # Hard coded values of how far the eyes move in the x and y axes

            # Move the cursor based on the eye movement direction
            if move_cursor and (abs(eye_delta_x) + abs(eye_delta_y)) >= (2* movement_threshold):
                pyautogui.moveRel(move_direction[0], -1 * move_direction[1], duration= .1) # Duration is .1 to have less twitchy movement

        if left_eye_pos != None and right_eye_pos != None:
            prev_eye_pos = ((left_eye_pos[0] + right_eye_pos[0])/2, (left_eye_pos[1]+right_eye_pos[1])/2)



        # Send the frame to GazeTracking to analyze it
        gaze_tracker.refresh(frame)

        # Get the annotated frame from GazeTracking
        annotated_frame = gaze_tracker.annotated_frame()

        # Check if the eye is blinking or not
        text = ""
        if gaze_tracker.is_blinking(threshold=blink_threshold):
            text = "Blinking"
            if blink_timer_start == None:
                blink_timer_start = time.time()
            blink_duration = blink_timer_start - time.time()

            if blink_duration >= 1:
                left_click()

        else:
            blink_timer_start = None

        # Display the prediction
        cv2.putText(annotated_frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)


        # Display the resulting frame
        cv2.imshow("EyeCursor", annotated_frame)

        # Check for key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            move_cursor = not move_cursor
            pyautogui.moveTo(width/2,height/2)


    # Release the webcam and close the windows
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()