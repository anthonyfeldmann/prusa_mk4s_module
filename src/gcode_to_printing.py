"""Handles uploading .bgcode to Prusa MK4S via PrusaLink API."""

import requests
from pathlib import Path
import time

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        return False

    # Switch to the 'local' storage endpoint instead of 'usb'
    url = f"http://{ip}/api/v1/files/local/{file_path_obj.name}"
    headers = {"X-Api-Key": api_key}

    try:
        time.sleep(1) 
        with file_path_obj.open("rb") as f:
            # First, upload the file
            response = requests.post(url, headers=headers, data=f, timeout=120)
            
            if response.status_code in [200, 201]:
                # If upload succeeds, send a separate command to start the print
                start_url = f"http://{ip}/api/v1/job"
                start_headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
                start_data = {"command": "start", "file": f"local/{file_path_obj.name}"}
                
                start_resp = requests.post(start_url, headers=start_headers, json=start_data)
                return start_resp.status_code == 204
            
        return False
    except Exception:
        return False
if __name__ == "__main__":
    # Test path updated to .gcode
    TEST_BGCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
