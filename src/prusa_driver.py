"""Prusa MK4S hardware driver."""

import argparse
import sys


# Python looks at your other files in the same folder and imports their specific functions
from gcode_to_printing import upload_and_start_print
from STL_To_PRUSAPRINT import slice_mesh
from UpdateOnshape_to_STL import download_custom_stl

# These serve as fallbacks, but they will be dynamically overwritten 
# by the MADSci REST Node (prusa_rest_node.py) when run in the workcell.
PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "jjehZqxQ542F9pQ"


def run_parametric_loop(length: float) -> bool:
    """
    Takes a parametric length, triggers Onshape CAD generation,
    and pushes the resulting STL to the printer.
    """
    print(f"Starting parametric CAD generation for length: {length}mm")  # noqa: T201

    try:
        # 1. Generate the STL using your existing Onshape script
        # (Ensure your script returns the absolute or relative path to the new STL)
        stl_path = generate_stl(length)
        
    except Exception as e:
        print(f"Fatal Error: Onshape API generation failed: {e}")  # noqa: T201
        return False

    if not stl_path or not Path(stl_path).exists():
        print("Fatal Error: Onshape script did not output a valid STL file.")  # noqa: T201
        return False

    # 2. Hand the fresh STL directly over to our existing print workflow
    print(f"Successfully generated CAD. Pushing {stl_path} to printer...")  # noqa: T201
    return run_stl_print(stl_path)


def run_stl_print(stl_path: str) -> bool:
    """
    Slices an provided STL file and uploads it directly to the Prusa MK4S.
    Returns True on success, False on failure to maintain MADSci compliance.
    """
    print(f"Starting workflow with provided STL: {stl_path}")  # noqa: T201

    # Validate the file actually exists before wasting compute time
    if not Path(stl_path).exists():
        print(f"Error: Could not locate STL file at {stl_path}")  # noqa: T201
        return False

    # STEP 1: PRUSASLICER STL_TO_BGCODE
    print("Sending mesh to PrusaSlicer...")  # noqa: T201
    bgcode_path = slice_mesh(stl_path)

    if not bgcode_path:
        print("Fatal Error: PrusaSlicer failed to generate bgcode.")  # noqa: T201
        return False

    # STEP 2: BGCODE_TO_PRINT
    print(f"Uploading {bgcode_path} to Prusa MK4S at {PRINTER_IP}...")  # noqa: T201
    print_started = upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)

    if print_started:
        print("Success: Part is now printing!")  # noqa: T201
        return True 
    else:
        print("Fatal Error: Printer is busy, unreachable, or rejected the file.")  # noqa: T201
        return False 


def main() -> None:
    """Allows an engineer to manually test this script directly from the PowerShell terminal."""
    parser = argparse.ArgumentParser(description="Prusa MK4S STL Print Driver")

    # Allow testing either an STL file directly, or the full parametric loop
    parser.add_argument(
        "--stl",
        type=str,
        help="The absolute or relative path to the .stl file you want to print.",
    )
    parser.add_argument(
        "--length",
        type=float,
        help="Test the full Onshape parametric loop with a specific length in mm.",
    )

    args = parser.parse_args()

    # Fire the engine using the user's requested flag
    if args.length is not None:
        success = run_parametric_loop(args.length)
    elif args.stl is not None:
        success = run_stl_print(args.stl)
    else:
        print("Error: You must provide either --stl or --length to run a test.")  # noqa: T201
        sys.exit(1)

    # When run directly from the terminal, it is safe to use OS exit codes
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
