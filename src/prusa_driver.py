"""Prusa MK4S hardware driver."""

import argparse
import sys
import time
import requests
from pathlib import Path

from gcode_to_printing import upload_and_start_print, is_printer_ready, monitor_print_job
from STL_To_PRUSAPRINT import slice_mesh
from UpdateOnshape_to_STL import download_custom_stl

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"

# --- PRUSACONNECT CLOUD CREDENTIALS ---
PRUSA_CONNECT_UUID = "3e40403e-a4c8-41b2-b3a6-c932feff4c64"
PRUSA_CONNECT_TOKEN = "R55RXEA73e40403e"

def force_ready_via_cloud() -> bool:
    """Sends the 'Set Ready' command via PrusaConnect to dismiss the Finished screen."""
    print("Reaching out to PrusaConnect cloud to clear the UI...")
    url = f"https://connect.prusa3d.com/app/printers/{PRUSA_CONNECT_UUID}/command"
    headers = {
        "Authorization": f"Bearer {PRUSA_CONNECT_TOKEN}",
        "Content-Type": "application/json"
    }
    # Command to force the UI into the Ready state
    payload = {"command": "set_ready"} 
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code in [200, 201, 204]:
            print("Cloud command accepted! UI is clear.")
            return True
        else:
            print(f"Cloud command rejected: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Network error reaching PrusaConnect: {e}")
        return False

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

    # Upload the file and start the job
    start_success = upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)
    
    # If the print started successfully, block the script until it finishes!
    if start_success:
        print_finished = monitor_print_job(PRINTER_IP, PRUSALINK_KEY)
        
        # --- END OF CYCLE CLEANUP ---
        # If the print hit 100%, trigger the cloud reset before releasing the orchestrator
        if print_finished:
            print("Print completed successfully. Triggering cloud reset to clear UI...")
            force_ready_via_cloud()
            
            # Give the MK4 motherboard 2 seconds to physically update the screen 
            # before the script exits and hands control back to the orchestrator.
            time.sleep(2)
        # ----------------------------
        
        return print_finished
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
