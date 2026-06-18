import requests
import os
#From RPL Printer, CHANGE IF USING DIFFERENT PRINTER
PRINTER_IP = "146.137.240.52" 
PRUSALINK_KEY = "3ow4yo9CDB3kkzx" #Labeled as secret key on printer
#merge with other code
GCODE_FILE = r"C:\Users\Anthony Feldmann\Downloads\fluidtest_export.bgcode"  #gcode file path input


def upload_and_start_print(file_path, ip, api_key):
    """Uploads G-code to the printer and immediately starts the print."""
    
    if not os.path.exists(file_path):
        print(f"Error: no G-code at {file_path}")
        return

    # We target the main local storage endpoint for uploading
    filename = os.path.basename(file_path)
    url = f"http://{ip}/api/v1/files/usb/{filename}"

    headers = { "X-Api-Key": api_key, "Print-After_Upload": "?1"}

    print(f"Uploading '{os.path.basename(file_path)}' to the printer...")

    try:
        with open(file_path, 'rb') as f:
            # 1. Package the file for upload
            
            # 2. Add the commands to select the file and start the print
            # Notice this is a standard dictionary passed to 'data', not 'json'
            payload = {
                'select': 'true',
                'print': 'true'
            }

            # 3. Send the file and the commands at the exact same time
            response = requests.post(
                url,
                headers=headers,
                data=f,
                proxies={"http": None, "https": None},
                timeout=60                      # Gives the MK4S time to unpack the .bgcode
            )
        # HTTP 201 = file created successfully on printer USB drive
        if response.status_code in [200, 204, 201]:
            print("File uploaded and printer heating")
        # HTTP 409 = usually means the file uploaded, but the printer is busy printing something else
        elif response.status_code == 409:
            print("File uploaded, but printer busy and can't start.")
        else:
            print(f"Upload failed. HTTP {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to printer at {ip}")

# --- 2. EXECUTE ---
if __name__ == "__main__":
    upload_and_start_print(GCODE_FILE, PRINTER_IP, PRUSALINK_KEY)
