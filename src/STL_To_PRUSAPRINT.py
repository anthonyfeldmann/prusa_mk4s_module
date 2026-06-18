import subprocess
import os

def slice_mesh(stl_path):
    """
    Takes a dynamic STL file path, runs it through PrusaSlicer, 
    and returns the path of the new .bgcode file.
    """
    
    print(f"\n--- Slicer Started ---")
    if not os.path.exists(stl_path):
        print(f"Could not find STL file  {stl_path}")
        return None

    # --- 1. DEFINE YOUR LOCAL PATHS ---
    # VERIFY THESE MATCH YOUR COMPUTER!
    slicer_exe = r"C:\Program Files\Prusa3D\PrusaSlicer\prusa-slicer-console.exe"
    config_file = r"C:\Users\Anthony Feldmann\Downloads\RPL_Printer_Config.ini"
    
    # --- 2. GENERATE THE OUTPUT NAME ---
    # This automatically changes "fluidtest_300mm.stl" to "fluidtest_300mm.bgcode"
    bgcode_path = stl_path.replace(".stl", ".bgcode")
    
    print(f"Slicing: {os.path.basename(stl_path)}...")

    # --- 3. RUN PRUSASLICER ---
    try:
        subprocess.run([
            slicer_exe,
            "--load", config_file,
            "--center", "125,105",       # Apply your specific MK4S settings
            "--export-gcode",           # Tell it to generate binary G-code
            "--output", bgcode_path,     # Where to save the new file
            stl_path                     # The input STL to slice
        ], check=True)
        
        print(f"Slicing Complete: {os.path.basename(bgcode_path)}")
        
        # --- 4. HAND THE PATH BACK TO THE MASTER SCRIPT ---
        return bgcode_path
        
    except subprocess.CalledProcessError:
        print("PrusaSlicer failed to generate the G-code.")
        return None

# --- MANUAL TEST EXECUTION ---
# This block is hidden from the Master Script! 
# It only runs if you double-click THIS file directly.
if __name__ == "__main__":
    # A fake path just to test if the slicer works by itself
    test_stl = r"C:\Users\Anthony Feldmann\Downloads\fluidtest_export.stl"
    slice_mesh(test_stl)