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
    try:
        stl_path = download_custom_stl(length)
    except Exception:
        return False

    if not stl_path or not Path(stl_path).exists():
        return False

    return run_stl_print(stl_path)

def run_stl_print(stl_path: str) -> bool:
    if not Path(stl_path).exists():
        return False

    bgcode_path = slice_mesh(stl_path)
    if not bgcode_path:
        return False

    return upload_and_start_print(bgcode_path, PRINTER_IP, PRUSALINK_KEY)

def main() -> None:
    parser = argparse.ArgumentParser(description="Prusa MK4S STL Print Driver")
    parser.add_argument("--stl", type=str)
    parser.add_argument("--length", type=float)
    args = parser.parse_args()

    if args.length is not None:
        success = run_parametric_loop(args.length)
    elif args.stl is not None:
        success = run_stl_print(args.stl)
    else:
        sys.exit(1)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
