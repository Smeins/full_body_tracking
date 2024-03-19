# Full Body Tracking with detailed Hands
This is about a simple python-script that handels full body tracking with detailed hands.
## How to use:
To use the script you need to install mediapipe and opencv:
```bash
pip install mediapipe
```
```bash
pip install opencv-python
```
After installing you can clone the code and use it.   
## About the handtracking:
The handtracking is available in a german and english version, use the code that fits your language. The handtracking tracks the position of the hands. It was build to work if a hand faces down. So you might encounter bugs if the hand is facing up. We did it that way, so we could track if a hand was facing the Unitree Go2 EDU.
It is also possible to stream a live view into the script.
Note: You dont need a Unitree Go2 EDU to work with the script. If you stream a live view from c++ to the script, you should use subtasks.

## Important things:
- mediapipe installed
- opencv installed
- camera connected to your pc



