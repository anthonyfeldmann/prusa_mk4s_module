"""Prusa MK4S hardware driver."""

import argparse
import sys
import time
import requests
from pathlib import Path

# Removed upload_and_start_print since we are handling the sequence directly
from gcode_to_printing import is_printer_ready, monitor_print_job
from STL_To_PRUSAPRINT import slice_mesh
from UpdateOnshape_to_STL import download_custom_stl

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"

def run_parametric_loop(length: float) -> bool:
    stl_path = download_custom_stl(length)
    if not stl_path or not Path(stl_path).exists():
        return False
    return run_stl_print(stl_path)

def run_stl_print(stl_path: str) -> bool:
    if not Path(stl_path).exists():
        return False

    bgcode_path = slice_mesh(stl_path)
    if not bgcode_path:
        return False

    max_wait = 10
    path_to_file = Path(bgcode_path)
    while not path_to_file.exists() and max_wait > 0:
        time.sleep(1)
        max_wait -= 1

    print("Checking printer status...")
    max_status_wait = 12
    
    while max_status_wait > 0:
        if is_printer_ready(PRINTER_IP, PRUSALINK_KEY):
            print("Printer is IDLE. Proceeding with upload...")
            break
        print("Waiting for printer to become available...")
        time.sleep(5)
        max_status_wait -= 1
    else:
        print("Error: Printer did not become available.")
        return False

    # --- SPLIT UPLOAD AND START SEQUENCE ---
    filename = path_to_file.name
    headers = {"X-Api-Key": PRUSALINK_KEY}
    target_url = f"http://{PRINTER_IP}/api/files/usb/{filename}"
    
    print(f"1. Uploading {filename} to printer USB...")
    try:
        # Step 1: Passive Upload (PUT request)
        with open(path_to_file, "rb") as f:
            upload_response = requests.put(target_url, data=f, headers=headers, timeout=120)
            
        if upload_response.status_code not in [200, 201, 204]:
            print(f"Upload failed: {upload_response.status_code} - {upload_response.text}")
            return False
            
        print("2. Upload complete. Waiting 2 seconds for MK4 filesystem...")
        # Step 2: Buffer Wait
        time.sleep(2)
        
        # Step 3: Dedicated Start Command (POST request to override UI)
        print("3. Commanding MK4 to start the job...")
        payload = {"command": "select", "print": True}
        start_response = requests.post(target_url, json=payload, headers=headers, timeout=10)
        
        if start_response.status_code not in [200, 204]:
            print(f"Start command rejected: {start_response.status_code} - {start_response.text}")
            return False
            
        print("Print successfully started!")
        start_success = True
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to communicate with PrusaLink API: {e}")
        return False
    # ---------------------------------------
    
    # If the print started successfully, block the script until it finishes!
    if start_success:
        return monitor_print_job(PRINTER_IP, PRUSALINK_KEY)
    else:
        return False

def main() -> None:
    parser = argparse.ArgumentParser(description="Prusa MK4S Driver")
    parser.add_argument("--stl", type=str)
    parser.add_argument("--length", type=float)
    args = parser.parse_args()

    success = run_parametric_loop(args.length) if args.length else run_stl_print(args.stl)
    
    # The script will only reach this line once the print is 100% finished
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
