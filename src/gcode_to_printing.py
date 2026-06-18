"""Handles uploading .gcode to Prusa MK4S via PrusaLink API."""

"""Handles uploading .bgcode to Prusa MK4S via PrusaLink API."""

import requests
from pathlib import Path
import time

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    file_path_obj = Path(file_path)
    if not file_path_obj.exists(): return False

    url = f"http://{ip}/api/v1/files/usb/{file_path_obj.name}"
    headers = {"X-Api-Key": api_key, "Print-After-Upload": "true"}

    # Increase wait time to 3 seconds to let the printer process the file creation
    time.sleep(3) 

    try:
        with file_path_obj.open("rb") as f:
            # Added a slightly longer timeout
            response = requests.post(url, headers=headers, data=f, timeout=120)
            
        if response.status_code in [200, 201, 204]:
            return True
        else:
            print(f"DEBUG: PrusaLink rejected file with status {response.status_code}")
            return False
    except Exception as e:
        print(f"DEBUG: Connection error: {e}")
        return False

if __name__ == "__main__":
    # Test path updated to .gcode
    TEST_BGCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
