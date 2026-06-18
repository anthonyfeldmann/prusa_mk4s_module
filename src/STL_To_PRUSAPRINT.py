"""Slices STL files using PrusaSlicer on Linux."""

import subprocess
from pathlib import Path

def slice_mesh(stl_path: str) -> str | None:
    """Slices an STL and returns the .gcode path."""
    
    stl_path_obj = Path(stl_path)
    
    print("\n--- Slicer Started ---")
    if not stl_path_obj.exists():
        print(f"Could not find STL file: {stl_path}")
        return None

    # Using the verified absolute path
    slicer_exe = "/usr/bin/prusa-slicer" 
    
    config_file = Path("/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/configs/RPL_Printer_Config.ini")
    
    # Generate output path with .gcode extension
    gcode_path = stl_path_obj.with_suffix(".gcode")
    
    print(f"Slicing: {stl_path_obj.name}...")

    try:
        subprocess.run([
            slicer_exe,
            "--load", str(config_file),
            "--center", "125,105",
            "--export-gcode",
            "--output", str(gcode_path),
            str(stl_path_obj)
        ], check=True)
        
        print(f"Slicing Complete: {gcode_path.name}")
        return str(gcode_path)
        
    except subprocess.CalledProcessError as e:
        print(f"PrusaSlicer failed: {e}")
        return None

if __name__ == "__main__":
    test_stl = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.stl"
    slice_mesh(test_stl)
