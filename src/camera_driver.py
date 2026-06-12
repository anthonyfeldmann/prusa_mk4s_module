import time

import cv2
import numpy as np


def get_single_measurement(target_bucket=2, total_buckets=3, pixels_per_mm=2.0):

    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Couldn't connect to cam")
        return None

    for _ in range(30):
        cap.read()  # stall for black frames
        time.sleep(0.03)

    # --- 2. TAKE THE OFFICIAL FRAME ---
    ret, frame = cap.read()
    cap.release()  # Immediately release the hardware so it doesn't overheat

    if not ret:
        print("Could not Capture Image")
        return None
    frame = frame[215:240, 350:450]
    # --- 3. ISOLATE THE TARGET BUCKET ---
    height, width = frame.shape[:2]  # Bucket Geometry and Isolating
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred, 50, 150)
    target_index = target_bucket - 1
    roi_width = width // total_buckets

    x_start = target_index * roi_width
    x_end = (target_index + 1) * roi_width

    margin = int(roi_width * 0.50)  # safety margin for walls
    roi_edges = edges[:, x_start + margin : x_end - margin]

    # height calculations
    y_coords, x_coords = np.where(roi_edges == 255)

    if len(y_coords) > 0:
        y_meniscus = int(np.percentile(y_coords, 5))
        pixel_height = height - y_meniscus
        physical_height_mm = round(pixel_height / pixels_per_mm, 2)
    else:
        physical_height_mm = 0.0

    return physical_height_mm


# --- EXECUTION ENGINE ---
if __name__ == "__main__":
    # Configure your physical setup here
    TARGET = 3  # The specific bucket you want to measure
    TOTAL = 5  # total number of buckets
    CALIBRATION = 3.2  # Your pixels-to-mm ratio

    print(f"Targeting Bucket {TARGET} of {TOTAL}...")

    # Run the measurement
    final_height = get_single_measurement(
        target_bucket=TARGET, total_buckets=TOTAL, pixels_per_mm=CALIBRATION
    )

    if final_height is not None:
        # --- 5. STORE THE DATA ---
        # Write the data to a simple text file that other scripts can easily read
        with open("latest_measurement.txt", "w") as file:
            file.write(str(final_height))

        # --- 6. OUTPUT TO TERMINAL ---
        # Print a clean output so your Master Script can capture it via subprocess
        print(f"RESULT:{final_height}")
