import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_map(map_path):
    """Loads and processes the given map by converting green pixels to white."""
    map_img = cv2.imread(map_path)  # Load the map image
    
    if map_img is None:
        raise FileNotFoundError(f"Could not open or find the image at {map_path}")

    # Convert to HSV and replace green with white
    hsv = cv2.cvtColor(map_img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    map_img[mask > 0] = [255, 255, 255]  # Replace green pixels with white
    
    # Convert to grayscale
    gray_map = cv2.cvtColor(map_img, cv2.COLOR_BGR2GRAY)

    return gray_map

# def load_lidar_data(lidar_file):
#     """Loads the LiDAR scan dataset."""
#     return np.loadtxt(lidar_file)  # Assumes LiDAR data is in a text file format

# def load_lidar_data(lidar_file):
#     """Loads the LiDAR scan dataset, filtering out non-numeric lines."""
#     valid_lines = []
    
#     with open(lidar_file, "r") as file:
#         for line in file:
#             try:
#                 values = list(map(float, line.split()))  # Convert to float
#                 valid_lines.append(values)
#             except ValueError:
#                 continue  # Skip non-numeric lines
    
#     lidar_data = np.array(valid_lines)  # Convert to NumPy array

#     if lidar_data.size == 0:
#         raise ValueError(f"Error: No valid LiDAR data found in {lidar_file}")

#     print(f"Loaded LiDAR data shape: {lidar_data.shape}")  # Debugging output
#     return lidar_data

# def load_lidar_data(lidar_file):
#     """Loads LiDAR scan data, filtering out headers and non-relevant lines."""
#     valid_lines = []
    
#     with open(lidar_file, "r") as file:
#         for line in file:
#             line = line.strip()  # Remove leading/trailing spaces
            
#             # Skip comments and metadata lines
#             if line.startswith("#") or line.startswith("PARAM") or line.startswith("SYNC") or line.startswith("ODOM"):
#                 continue

#             # Process LiDAR readings (FLASER or RLASER)
#             parts = line.split()
#             if parts[0] in ["FLASER", "RLASER"]:
#                 try:
#                     num_readings = int(parts[1])  # First value is number of readings
#                     ranges = list(map(float, parts[2:num_readings+2]))  # Extract LiDAR readings
                    
#                     # Extract (x, y) position of LiDAR scanner
#                     x, y = float(parts[num_readings+2]), float(parts[num_readings+3])
                    
#                     valid_lines.append([x, y])
#                 except ValueError:
#                     print(f"Skipping invalid LiDAR line: {line}")  # Debugging message
#                     continue  # Skip if parsing fails

#     lidar_data = np.array(valid_lines)  # Convert to NumPy array

#     if lidar_data.size == 0:
#         raise ValueError(f"Error: No valid LiDAR data found in {lidar_file}")

#     print(f"Loaded LiDAR data shape: {lidar_data.shape}")  # Debugging output
#     return lidar_data

def load_lidar_data(lidar_file):
    """Loads LiDAR scan data, extracting (x, y) positions while skipping metadata."""
    valid_points = []

    with open(lidar_file, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith(("#", "PARAM", "SYNC", "ODOM")):
                continue

            parts = line.split()
            if parts[0] in {"FLASER", "RLASER"}:
                try:
                    num_readings = int(parts[1])
                    x, y = map(float, parts[num_readings+2:num_readings+4])
                    valid_points.append([x, y])
                except (ValueError, IndexError):
                    print(f"Skipping invalid LiDAR line: {line}")

    if not valid_points:
        raise ValueError(f"Error: No valid LiDAR data found in {lidar_file}")

    lidar_data = np.array(valid_points)
    print(f"Loaded LiDAR data shape: {lidar_data.shape}")
    return lidar_data



def correlative_scan_matching(map_img, lidar_scan, search_range=10):
    """Performs Correlative Scan Matching (CSM) to estimate position."""
    if lidar_scan.ndim == 1:
        lidar_scan = lidar_scan.reshape(-1, 2)  # Ensure shape is (N,2)

    best_match = None
    best_score = -np.inf
    best_x, best_y = 0, 0
    
    for dx in range(-search_range, search_range):
        for dy in range(-search_range, search_range):
            transformed_scan = lidar_scan + np.array([dx, dy])  # Use NumPy array
            score = compute_match_score(map_img, transformed_scan)
            
            if score > best_score:
                best_score = score
                best_match = transformed_scan
                best_x, best_y = dx, dy
    
    return best_x, best_y, best_match



def compute_match_score(map_img, transformed_scan):
    """Computes how well the transformed LiDAR scan matches the map."""
    score = 0
    for point in transformed_scan:
        x, y = int(point[0]), int(point[1])
        if 0 <= x < map_img.shape[1] and 0 <= y < map_img.shape[0]:
            score += 255 - map_img[y, x]  # Higher intensity means better match
    print(score)
    return score

def main():
    map_path = "map.png"  # Replace with actual path
    lidar_path = "aces.clf.txt"  # Replace with actual path
    
    # Load and preprocess map
    try:
        processed_map = preprocess_map(map_path)
        
        # Display the processed image
        plt.imshow(processed_map, cmap="gray")
        plt.axis("off")
        plt.show()

        # Save the processed image
        cv2.imwrite("processed_map.png", processed_map)
        print("Processed map saved as 'processed_map.png'.")

    except FileNotFoundError as e:
        print(e)
    
    # Load LiDAR scan data
    try:
        lidar_scan = load_lidar_data(lidar_path)
    except ValueError as e:
        print(e)
        return
    print (lidar_scan)
    # Perform Correlative Scan Matching
    estimated_x, estimated_y, matched_scan = correlative_scan_matching(processed_map, lidar_scan)
    
    print(f"Estimated Position: X={estimated_x}, Y={estimated_y}")
    
    # Visualize results
    plt.imshow(processed_map, cmap='gray')
    plt.scatter(matched_scan[:, 0], matched_scan[:, 1], c='red', marker='o', label='Matched LiDAR')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
