import requests
from pathlib import Path
import time

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "3ow4yo9CDB3kkzx"

def upload_and_start_print(file_path: str, ip: str, api_key: str) -> bool:
    file_path_obj = Path(file_path)
    if not file_path_obj.exists(): return False

    url = f"http://{ip}/api/v1/files/usb/{file_path_obj.name}"
    headers = {"X-Api-Key": api_key, "Print-After-Upload": "true"}

    try:
        time.sleep(1)
        with file_path_obj.open("rb") as f:
            response = requests.post(
                url, headers=headers, data=f, 
                proxies={"http": None, "https": None}, timeout=60
            )
        return response.status_code in [200, 201, 204]
    except requests.exceptions.RequestException:
        return False

if __name__ == "__main__":
    TEST_GCODE = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.bgcode"
    upload_and_start_print(TEST_GCODE, PRINTER_IP, PRUSALINK_KEY)
