"""Handles uploading .bgcode to Prusa MK4S via PrusaLink API."""

import requests
from pathlib import Path
import time

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "YOUR_VERIFIED_API_KEY" 

def is_printer_ready(ip: str, api_key: str) -> bool:
    url = f"http://{ip}/api/v1/status"
    headers = {"X-Api-Key": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            state = response.json().get("printer", {}).get("state", "").upper()
            if state in ["IDLE", "READY"]:
                return True
            else:
                print(f"DEBUG: Printer is busy. Current state: '{state}'")
                return False
        return False
    except Exception:
        return False

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        return False

    url = f"http://{ip}/api/v1/files/usb/{file_path_obj.name}"
    headers = {
        "X-Api-Key": api_key, 
        "Print-After-Upload": "true"
    }

    try:
        time.sleep(1) 
        with file_path_obj.open("rb") as f:
            response = requests.put(url, headers=headers, data=f, timeout=120)
            
        if response.status_code in [200, 201, 204]:
            print("Success: File uploaded and print started!")
            return True
        else:
            print(f"DEBUG: Upload failed. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"DEBUG: Connection error: {e}")
        return False

def monitor_print_job(ip: str, api_key: str) -> bool:
    """Blocks and monitors the printer until the job is FINISHED."""
    url = f"http://{ip}/api/v1/status"
    headers = {"X-Api-Key": api_key}
    
    print("Monitoring print progress. MADSci node will hold here until complete...")
    
    # Give the printer a few seconds to transition from IDLE to PRINTING
    time.sleep(10)
    
    last_logged_progress = -1

    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                state = data.get("printer", {}).get("state", "").upper()
                
                # Check for completion
                if state == "FINISHED":
                    print("\nPrint job complete! Part is ready for the workflow.")
                    return True
                
                # Check for fatal errors that should fail the MADSci node
                elif state in ["ERROR", "ATTENTION", "STOPPED"]:
                    print(f"\nError: Print halted unexpectedly. State: {state}")
                    return False
                
                # Log progress cleanly (every 10%)
                progress = data.get("job", {}).get("progress", 0)
                if progress is not None:
                    rounded_progress = int(progress // 10) * 10
                    if rounded_progress != last_logged_progress:
                        print(f"Print Status: {state} - {rounded_progress}% complete")
                        last_logged_progress = rounded_progress
                        
        except requests.exceptions.RequestException as e:
            # If the network blips, don't fail the whole print. Just warn and retry.
            print(f"DEBUG: Temporary connection loss during monitoring: {e}")
            
        # Poll every 30 seconds to avoid overwhelming the MK4S API
        time.sleep(30)
if __name__ == "__main__":
    # Test path updated to .gcode
    TEST_BGCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
