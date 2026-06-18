"""Handles uploading .bgcode to Prusa MK4S via PrusaLink API."""

import requests
from pathlib import Path
import time

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    """Uploads .bgcode to printer and starts the print with enhanced debugging."""
    
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        print(f"DEBUG: File not found at {file_path}")
        return False

    url = f"http://{ip}/api/v1/files/usb/{file_path_obj.name}"
    # Added 'Print-After-Upload' as a separate parameter for better compatibility
    headers = {"X-Api-Key": api_key, "Print-After-Upload": "true"}

    print(f"DEBUG: Attempting upload to {url}")

    try:
        time.sleep(2) 
        with file_path_obj.open("rb") as f:
            # We use a direct stream to ensure large binary files are handled correctly
            response = requests.post(
                url, 
                headers=headers, 
                data=f, 
                timeout=120
            )
            
        if response.status_code in [200, 201, 204]:
            print("Success: File uploaded and printer signaled.")
            return True
        else:
            # This print will appear in your MADSci logs and tell us exactly WHY it failed
            print(f"DEBUG: PrusaLink rejected upload. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"DEBUG: Connection error: {e}")
        return False
if __name__ == "__main__":
    # Test path updated to .gcode
    TEST_BGCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
