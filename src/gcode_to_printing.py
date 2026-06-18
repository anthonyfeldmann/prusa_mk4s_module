"""Handles uploading .bgcode to Prusa MK4S via PrusaLink API."""

import requests
from pathlib import Path
import time

PRINTER_IP = 146.137.240.52
PRUSALINK_KEY = "YOUR_VERIFIED_API_KEY"  # <-- Ensure your correct key is here!

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        print(f"DEBUG: File not found at {file_path}")
        return False

    # 1. The MK4S uses the /usb/ endpoint for PrusaLink file storage
    url = f"http://{ip}/api/v1/files/usb/{file_path_obj.name}"
    
    # 2. Tell the printer to start the job immediately after the upload stream finishes
    headers = {
        "X-Api-Key": api_key, 
        "Print-After-Upload": "true"
    }

    try:
        time.sleep(1) 
        with file_path_obj.open("rb") as f:
            # 3. CRITICAL FIX: The PrusaLink API requires PUT for binary file uploads, not POST!
            response = requests.put(
                url, 
                headers=headers, 
                data=f, 
                timeout=120
            )
            
        if response.status_code in [200, 201, 204]:
            print("Success: File uploaded and print started!")
            return True
        else:
            print(f"DEBUG: Upload failed. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"DEBUG: Connection error: {e}")
        return False
if __name__ == "__main__":
    # Test path updated to .gcode
    TEST_BGCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
