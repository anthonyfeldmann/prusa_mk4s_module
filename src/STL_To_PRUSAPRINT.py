"""Slices STL files using PrusaSlicer (Flatpak) on Linux."""

import subprocess
from pathlib import Path

def slice_mesh(stl_path: str) -> str | None:
    """Slices an STL to .bgcode using the latest Flatpak version."""
    
    stl_path_obj = Path(stl_path)
    if not stl_path_obj.exists(): return None

    # Use the absolute path to the Flatpak utility and the App ID
    flatpak_exe = "/usr/bin/flatpak"
    app_id = "com.prusa3d.PrusaSlicer"
    config_file = Path("/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/configs/RPL_Printer_Config.ini")
    
    # Verify version to confirm we are using the modern slicer
    try:
        version = subprocess.check_output([flatpak_exe, "run", app_id, "--version"]).decode()
        print(f"DEBUG: PrusaSlicer version: {version.strip()}")
    except Exception as e:
        print(f"DEBUG: Could not verify version: {e}")

    bgcode_path = stl_path_obj.with_suffix(".bgcode")
    
    try:
        subprocess.run([
            flatpak_exe, "run", app_id,
            "--load", str(config_file),
            "--center", "125,105",
            "--export-bgcode",
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
