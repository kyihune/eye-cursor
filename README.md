<<<<<<< HEAD



=======
# Eye Cursor Project
# Spring 2024 Computer Vision Project
by Mahel Napo and Kariam Yihune

to create a smooth eye tracking program in order to replace mouse navigation 
with simply looking around using gaze tracking with Python and OpenCV. It utilizes the [GazeTracking repository](https://github.com/antoinelame/GazeTracking) to track the user's gaze direction and control the cursor accordingly.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
git clone https://github.com/kyihune/eye-cursor.git
Copy code
2. Navigate to the project directory:
cd eye-cursor
Copy code
3. (Optional) Create a virtual environment:
python -m venv myenv
Copy code
Activate the virtual environment:
- On Windows:
  ```
  myenv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source myenv/bin/activate
  ```

4. Install the required dependencies:
- Using `requirements.txt` file:
  ```
  pip install -r requirements.txt
  ```

- Alternatively, you can install the dependencies separately:
  ```
  pip install numpy opencv-python dlib pyautogui
  ```

## Running the Example

1. Make sure you have a webcam connected to your device.

2. Run the `example.py` script:
python example.py
Copy code
3. The script will open a window showing the webcam feed with gaze tracking information overlaid on the frame.

4. Press 'q' to quit the application.

## Running the Eye Cursor
1. Make sure you have a webcam connected to your device.

2. Run the `eyeCursor.py` script:
python eyeCursor.py
Copy code
3. The script will open a window showing the webcam feed with gaze tracking, and face tracking for cursor movement.

4. The blinking of the user will be used for couple different comment(they are not set in stone yet), and the face direction will be used to control the cursor movement on the screen.

5. Press 'q' to quit the application or 'p' to pause the face tracking to reset the position of your face.

## Gaze Tracking

This project utilizes the [GazeTracking repository](https://github.com/antoinelame/GazeTracking) to perform gaze tracking. The GazeTracking module provides the necessary functionality to detect the user's gaze direction and extract information about the position of the eyes and pupils.

The GazeTracking module is integrated into the eye-cursor project to enable the eye-controlled cursor functionality.

## Troubleshooting

- If you encounter any issues with the `dlib` library, you can try installing it separately using a pre-built wheel from the unofficial Python Wheels website: [Python Wheels - dlib](https://www.lfd.uci.edu/~gohlke/pythonlibs/#dlib)

- If you have any other questions or run into any problems, please open an issue on the GitHub repository.

## License

This project is licensed under the 
>>>>>>> master
