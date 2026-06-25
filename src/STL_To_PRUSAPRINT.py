"""Slices STL files using PrusaSlicer (Flatpak) on Linux."""

import subprocess
import time
from pathlib import Path

def slice_mesh(stl_path: str) -> str | None:
    """Slices an STL to .bgcode using the latest Flatpak version."""
    
    stl_path_obj = Path(stl_path)
    if not stl_path_obj.exists(): return None

    flatpak_exe = "/usr/bin/flatpak"
    app_id = "com.prusa3d.PrusaSlicer"
    config_file = Path("/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/configs/RPL_Printer_Config.ini")
    
    # adds time to bgcode name for uniqueness
    unique_id = int(time.time())
    bgcode_path = stl_path_obj.with_name(f"{stl_path_obj.stem}_{unique_id}.bgcode")
    # -------------------------------
    
    try:
        subprocess.run([
            flatpak_exe, "run", app_id,
            "--load", str(config_file),
            "--center", "110,105",
            "--slice",
            "--output", str(bgcode_path),
            str(stl_path_obj)
        ], check=True)
        
        return str(bgcode_path)
    except subprocess.CalledProcessError as e:
        print(f"PrusaSlicer failed: {e}")
        return None

if __name__ == "__main__":
    test_stl = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.stl"
    slice_mesh(test_stl)
