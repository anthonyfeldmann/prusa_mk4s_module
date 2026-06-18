"""Slices STL files using PrusaSlicer on Linux."""

import subprocess
from pathlib import Path

def slice_mesh(stl_path: str) -> str | None:
    """Slices an STL and returns the .bgcode path."""
    
    stl_path_obj = Path(stl_path)
    
    print("\n--- Slicer Started ---")
    if not stl_path_obj.exists():
        print(f"Could not find STL file: {stl_path}")
        return None

    slicer_exe = "prusa-slicer" 
    
    # Update this to your absolute path on the Linux server
    config_file = Path("/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/configs/RPL_Printer_Config.ini")
    
    # Generate output path
    bgcode_path = stl_path_obj.with_suffix(".bgcode")
    
    print(f"Slicing: {stl_path_obj.name}...")

    try:
        subprocess.run([
            slicer_exe,
            "--load", str(config_file),
            "--center", "125,105",
            "--export-bgcode",
            "--output", str(bgcode_path),
            str(stl_path_obj)
        ], check=True)
        
        print(f"Slicing Complete: {bgcode_path.name}")
        return str(bgcode_path)
        
    except subprocess.CalledProcessError as e:
        print(f"PrusaSlicer failed: {e}")
        return None

if __name__ == "__main__":
    test_stl = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.stl"
    slice_mesh(test_stl)
