import cv2
from gaze_tracking import GazeTracking

def run_gaze_tracking():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)  # Initialize camera inside the function

    if not webcam.isOpened():
        print("Cannot open camera")
        return

    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        if frame is None:
            print("Cannot capture frame from camera")
            break

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""
        # Check if the eye is blinking or not
        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        # Display the prediction
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        # Display the resulting frame
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)

        # Check for the 'q' key to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()

# Run the gaze tracking function
run_gaze_tracking()