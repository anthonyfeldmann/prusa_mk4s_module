import argparse
import os

# Python looks at your other files in the same folder and imports their specific functions
from gcode_to_printing import upload_and_start_print
from STL_To_PRUSAPRINT import slice_mesh

# These serve as fallbacks, but they will be dynamically overwritten 
# by the MADSci REST Node (prusa_rest_node.py) when run in the workcell.
PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"


def run_stl_print(stl_path):
    """
    Slices an provided STL file and uploads it directly to the Prusa MK4S.
    Returns True on success, False on failure to maintain MADSci compliance.
    """
    print(f"Starting workflow with provided STL: {stl_path}")

    # Validate the file actually exists before wasting compute time
    if not os.path.exists(stl_path):
        print(f"Error: Could not locate STL file at {stl_path}")
        return False

    # STEP 1: PRUSASLICER STL_TO_BGCODE
    print("Sending mesh to PrusaSlicer...")
    bgcode_path = slice_mesh(stl_path)

    if not bgcode_path:
        print("Fatal Error: PrusaSlicer failed to generate bgcode.")
        return False

    # STEP 2: BGCODE_TO_PRINT
    print(f"Uploading {bgcode_path} to Prusa MK4S at {PRINTER_IP}...")
    print_started = upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)

    if print_started:
        print("Success: Part is now printing!")
        return True 
    else:
        print("Fatal Error: Printer is busy, unreachable, or rejected the file.")
        return False 


def main():
    """Allows an engineer to manually test this script directly from the PowerShell terminal."""
    parser = argparse.ArgumentParser(description="Prusa MK4S STL Print Driver")

    # Replaced the --length argument with an --stl file path argument
    parser.add_argument(
        "--stl",
        type=str,
        required=True,
        help="The absolute or relative path to the .stl file you want to print.",
    )

    args = parser.parse_args()

    # Fire the engine using the user's file path
    success = run_stl_print(args.stl)

    # When run directly from the terminal, it is safe to use OS exit codes
    if success:
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
