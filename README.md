# CSM Localisation

## Problem Statement

**Task**: Correlative Scan Matching for Localization. The task involves reading and implementing the research paper titled “A 2D-LiDAR- based localization method for indoor mobile robots using correlative scan matching” by Song Du, Tao Chen, Zhonghui Lou, and Yijie Wu (https://www.cambridge.org/core/journals/robotica/article/abs/2dlidarbased-localization-method-for-indoor-mobile-robots-using-correlative-scan-matching/291583763D866B1739AEF58ADC34D659). You will have to implement the localization method using the correlative scan matching (CSM) technique on this dataset (http://ais.informatik.uni-freiburg.de/slamevaluation/datasets/aces.clf).

**SUBTASK 1**: Use the dataset above with the noise parameters of your choice to localize the agent on this map (use OpenCV to replace green pixels with white ones).

**SUBTASK 2**: Utilize this solution to estimate better noise parameters and provide your rationale for doing so.

## Solution

The solution for Task 5 is implemented in TASK_5/mainCode.py. This script performs localization of a robot using 2D LiDAR data and a map via the Correlative Scan Matching (CSM) technique.

## Key features:

Loads a map image (map.png) and preprocesses it (e.g., converting green pixels to white, converting to grayscale, and applying thresholding). The processed map is saved as processed_map.png.
Loads LiDAR scan data from aces.clf.txt. Each line in this file typically represents a series of range measurements from the LiDAR.
Implements the Correlative Scan Matching algorithm to find the best match between the LiDAR scans and the map, thereby estimating the robot's position (x, y) and orientation (theta) on the map.
Outputs the estimated position and orientation to the console.
Inputs

Map file: TASK_5/map.png
LiDAR data file: TASK_5/aces.clf.txt
Outputs

Processed map image: TASK_5/processed_map.png
Console output: Estimated position (x, y) and orientation (theta) of the robot.
## How to Run

Ensure you have Python installed along with the necessary libraries (e.g., OpenCV, NumPy).
Navigate to the repository's root directory.
Run the script using the following command:
python TASK_5/mainCode.py
