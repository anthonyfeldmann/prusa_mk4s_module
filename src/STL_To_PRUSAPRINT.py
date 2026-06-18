import subprocess
from pathlib import Path

def slice_mesh(stl_path: str) -> str | None:
    stl_path_obj = Path(stl_path)
    if not stl_path_obj.exists(): return None

    slicer_exe = "/usr/bin/prusa-slicer" 
    config_file = Path("/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/configs/RPL_Printer_Config.ini")
    bgcode_path = stl_path_obj.with_suffix(".bgcode")
    
    try:
        subprocess.run([
            slicer_exe, "--load", str(config_file),
            "--center", "125,105", "--export-bgcode",
            "--output", str(bgcode_path), str(stl_path_obj)
        ], check=True)
        return str(bgcode_path)
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    test_stl = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files/fluidtest_300mm.stl"
    slice_mesh(test_stl)
