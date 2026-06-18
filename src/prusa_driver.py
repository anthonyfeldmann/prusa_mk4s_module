"""Prusa MK4S hardware driver."""

import argparse
import sys
import time
from pathlib import Path

from gcode_to_printing import upload_and_start_print
from STL_To_PRUSAPRINT import slice_mesh
from UpdateOnshape_to_STL import download_custom_stl

PRINTER_IP = "146.137.240.52"
PRUSALINK_KEY = "3ow4yo9CDB3kkzx"

def run_parametric_loop(length: float) -> bool:
    stl_path = download_custom_stl(length)
    if not stl_path or not Path(stl_path).exists():
        return False
    return run_stl_print(stl_path)

def run_stl_print(stl_path: str) -> bool:
    if not Path(stl_path).exists():
        return False

    bgcode_path = slice_mesh(stl_path)
    if not bgcode_path:
        return False

    # Wait loop: ensures the slicer has finished writing the file to disk
    max_wait = 10
    path_to_file = Path(bgcode_path)
    while not path_to_file.exists() and max_wait > 0:
        time.sleep(1)
        max_wait -= 1

    return upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)

def main() -> None:
    parser = argparse.ArgumentParser(description="Prusa MK4S Driver")
    parser.add_argument("--stl", type=str)
    parser.add_argument("--length", type=float)
    args = parser.parse_args()

    success = run_parametric_loop(args.length) if args.length else run_stl_print(args.stl)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
