"""Handles uploading .bgcode to Prusa MK4S via PrusaLink API."""


import requests
from pathlib import Path
import time

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "3ow4yo9CDB3kkzx"

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        return False

    url = f"http://{ip}/api/v1/files/usb/{file_path_obj.name}"
    headers = {"X-Api-Key": api_key, "Print-After-Upload": "true"}

    try:
        # Give the system one last second to flush the file buffer
        time.sleep(1) 
        with file_path_obj.open("rb") as f:
            response = requests.post(
                url, 
                headers=headers, 
                data=f, 
                timeout=120
            )
            
        # Return success only if printer accepts the file (200-204 range)
        return response.status_code in [200, 201, 204]
    except Exception:
        return False
if __name__ == "__main__":
    # Test path updated to .gcode
    TEST_BGCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
