## CSM Localization

## Problem Statement

## Task
Implement Correlative Scan Matching (CSM) for 2D LiDAR-based robot localization by studying and reproducing the method described in the paper:

“A 2D-LiDAR-based localization method for indoor mobile robots using correlative scan matching”  
Song Du, Tao Chen, Zhonghui Lou, Yijie Wu  
https://www.cambridge.org/core/journals/robotica/article/abs/2dlidarbased-localization-method-for-indoor-mobile-robots-using-correlative-scan-matching/291583763D866B1739AEF58ADC34D659

The localization algorithm is implemented and evaluated on the following dataset:  
http://ais.informatik.uni-freiburg.de/slamevaluation/datasets/aces.clf

## Subtasks

## Subtask 1: Localization Using CSM
- Use the provided LiDAR dataset to localize the robot on a given map.
- Add noise to the robot motion or sensor readings (noise parameters are chosen empirically).
- Preprocess the map using OpenCV, including replacing green pixels with white pixels.

## Subtask 2: Noise Parameter Estimation
- Use the localization results from Subtask 1 to refine and estimate better noise parameters.
- Provide a clear rationale for why the chosen noise parameters improve localization accuracy.

## Solution Overview

The solution for this task is implemented in:

TASK_5/mainCode.py

This script performs robot localization using Correlative Scan Matching (CSM) with 2D LiDAR data and a known map.

## Key Features

## Map Preprocessing
- Loads map.png
- Replaces green pixels with white pixels using OpenCV
- Converts the map to grayscale
- Applies thresholding to generate a binary occupancy map
- Saves the processed map as processed_map.png

## LiDAR Data Processing
- Loads LiDAR scan data from aces.clf.txt
- Each line represents a single LiDAR scan consisting of range measurements

## Correlative Scan Matching
- Transforms LiDAR scans into the map frame
- Evaluates scan-to-map correlation scores over a search space of (x, y, θ)
- Selects the pose with the highest correlation score as the estimated robot pose

## Localization Output
- Estimates and prints the robot’s position (x, y) and orientation (θ) to the console

## Inputs

Map file:  
TASK_5/map.png

LiDAR data file:  
TASK_5/aces.clf.txt

## Outputs

Processed map image:  
TASK_5/processed_map.png

Console output:
- Estimated robot position (x, y)
- Estimated orientation (θ)

## How to Run

1. Ensure Python is installed.
2. Install dependencies:
   pip install numpy opencv-python
3. Navigate to the repository root.
4. Run:
   python TASK_5/mainCode.py
