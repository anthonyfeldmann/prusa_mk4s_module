import argparse
import sys

from gcode_to_printing import upload_and_start_print
from STL_To_PRUSAPRINT import slice_mesh

#
# Python looks at your other files in the same folder and imports their specific functions
from UpdateOnshape_to_STL import download_custom_stl

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"  # may need to be changed


def run_parametric_loop(length_value):
    """Passes the dimension variables"""

    print(f"starting workflow w {length_value} mm")

    # STEP 1: ONSHAPE_to_STL
    stl_path = download_custom_stl(length_value)

    if not stl_path:
        print(" Onshape API failed.")
        sys.exit(1)

    # STEP 2: PRUSASLICER STL_TO_BGCODE
    bgcode_path = slice_mesh(stl_path)

    if not bgcode_path:
        print("PrusaSlicer failed")
        sys.exit(1)

    # STEP3: BGCODE_TO_PRINT
    print_started = upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)

    if print_started:
        print(f"Part ({length_value}mm) is now printing!")
        sys.exit(0)  # Absolute Success
    else:
        print("Fail; Printer is busy or unreachable. Data point not recorded.")
        sys.exit(1)  # Fatal Failure (Tells your Optimizer to wait or try again)


def main():
    """Allows an external optimizer to trigger this script and pass a variable."""
    parser = argparse.ArgumentParser(description="Parametric Loop Controller")

    # This creates a new command-line flag specifically for your physical dimension
    parser.add_argument(
        "--length",
        type=float,  # Allows decimals like 150.5
        required=True,
        help="The physical length (in mm) to inject into the Onshape model.",
    )

    args = parser.parse_args()

    # Fire the engine using the user's variable
    run_parametric_loop(args.length)


if __name__ == "__main__":
    main()
    # python3.13 Prusa_Automation.py --length 150 to run
