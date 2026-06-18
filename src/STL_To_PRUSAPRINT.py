"""Slices STL files using PrusaSlicer (Flatpak) on Linux."""

"""Slices STL files using PrusaSlicer (Flatpak) on Linux."""

import subprocess
from pathlib import Path

def slice_mesh(stl_path: str) -> str | None:
    """Slices an STL to .bgcode using the latest Flatpak version."""
    
    stl_path_obj = Path(stl_path)
    if not stl_path_obj.exists(): return None

    flatpak_exe = "/usr/bin/flatpak"
    app_id = "com.prusa3d.PrusaSlicer"
    config_file = Path("/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/configs/RPL_Printer_Config.ini")
    
    # PrusaSlicer 2.9.5 automatically detects format from the extension
    bgcode_path = stl_path_obj.with_suffix(".bgcode")
    
    try:
        # Changed --export-bgcode to --slice to align with 2.9.5 syntax
        subprocess.run([
            flatpak_exe, "run", app_id,
            "--load", str(config_file),
            "--center", "125,105",
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
