"""deletes all files on Prusa USB"""

from argparse import ArgumentParser

import requests


def main(args):
    """main deletion"""
    # PrusaLink standard API endpoint
    base_url = f"http://{args.ip_address}/api"
    headers = {"X-Api-Key": args.api_key}

    print(f"Connecting to Prusa MK4S at {args.ip_address}...")

    # check what is currently printing
    try:
        job_resp = requests.get(f"{base_url}/job", headers=headers, timeout=10)
        job_resp.raise_for_status()

        current_job = job_resp.json()
        is_printing = current_job.get("state") == "Printing"
        active_file_path = current_job.get("job", {}).get("file", {}).get("path")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Could not reach printer to check state: {e}")

    # get files
    files_url = f"{base_url}/files/usb"
    files_resp = requests.get(files_url, headers=headers, timeout=10)

    if files_resp.status_code != 200:
        raise Exception(
            f"Failed to fetch files. Status code {files_resp.status_code}: {files_resp.text}"
        )

    file_list = files_resp.json().get("files", [])

    if not file_list:
        print("USB drive is already empty.")
        return

    # delete files
    for f in file_list:
        # Ignore folders to prevent accidental directory corruption
        if f.get("type") == "folder":
            continue

        file_path = f.get("path")

        # Safety Check: Skip the file if the nozzle is currently printing it
        if is_printing and file_path == active_file_path:
            print(f"File '{file_path}' is currently printing, skipping...")
            continue

        # Execute the HTTP DELETE command
        delete_resp = requests.delete(
            f"{files_url}/{file_path}", headers=headers, timeout=10
        )

        if delete_resp.status_code in (200, 204):
            print(f"File '{file_path}' deleted...")
        else:
            print(
                f"Could not delete '{file_path}', response: {delete_resp.status_code} - {delete_resp.text}"
            )

    print(f"All inactive files cleared from Prusa MK4S at {args.ip_address}")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Delete all inactive .gcode/.bgcode files stored on a Prusa MK4S USB drive."
    )
    parser.add_argument(
        "-ip", "--ip_address", required=True, help="Printer IP address", type=str
    )
    parser.add_argument(
        "-k", "--api_key", required=True, help="PrusaLink API Key", type=str
    )

    args = parser.parse_args()
    main(args)
