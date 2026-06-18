"""Prusa MK4S hardware driver."""

import argparse
import sys
from pathlib import Path

from gcode_to_printing import upload_and_start_print
from STL_To_PRUSAPRINT import slice_mesh
from UpdateOnshape_to_STL import download_custom_stl

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "3ow4yo9CDB3kkzx"

def run_parametric_loop(length: float) -> bool:
    print(f"Starting parametric CAD generation for length: {length}mm")
    try:
        stl_path = download_custom_stl(length)
    except Exception as e:
        print(f"Fatal Error: Onshape API generation failed: {e}")
        return False

    if not stl_path or not Path(stl_path).exists():
        print("Fatal Error: Onshape script did not output a valid STL file.")
        return False

    print(f"Successfully generated CAD. Pushing {stl_path} to printer...")
    return run_stl_print(stl_path)

def run_stl_print(stl_path: str) -> bool:
    print(f"Starting workflow with provided STL: {stl_path}")
    if not Path(stl_path).exists():
        print(f"Error: Could not locate STL file at {stl_path}")
        return False

    bgcode_path = slice_mesh(stl_path)
    if not bgcode_path:
        print("Fatal Error: PrusaSlicer failed to generate bgcode.")
        return False

    print(f"Uploading {bgcode_path} to Prusa MK4S at {PRINTER_IP}...")
    print_started = upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)

    if print_started:
        print("Success: Part is now printing!")
        return True 
    else:
        print("Fatal Error: Printer is busy, unreachable, or rejected the file.")
        return False 

def main() -> None:
    parser = argparse.ArgumentParser(description="Prusa MK4S STL Print Driver")
    parser.add_argument("--stl", type=str, help="Path to the .stl file.")
    parser.add_argument("--length", type=float, help="Test parametric loop (mm).")
    args = parser.parse_args()

    if args.length is not None:
        success = run_parametric_loop(args.length)
    elif args.stl is not None:
        success = run_stl_print(args.stl)
    else:
        print("Error: You must provide either --stl or --length.")
        sys.exit(1)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
