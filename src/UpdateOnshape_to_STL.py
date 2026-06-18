import os
from onshape_client.client import Client

# --- 1. ONSHAPE DOCUMENT ADDRESS ---
DID = '460766ee1fd3b3b2a615b94a'
WID = '979042f4d058b6f5579afa14'
EID = '1dbb2720f9be98854d69ba84'

def download_custom_stl(dynamic_length_mm):
    """Requests a custom-sized, metric STL from Onshape."""
    
    # --- 2. AUTHENTICATION ---
    client = Client(configuration={
        # FIX 1: Updated to the US-West server to silence the UserWarning
        "base_url": "https://cad-usw2.onshape.com", 
        "access_key": "on_KGHB3Hg5gDl4hPffcpuCd",
        "secret_key": "he1iDT28dxOsLz7Ww5TAVXgcj1PopbihMT50NKyMcmacO0pc"
    })

    api_url = f"https://cad-usw2.onshape.com/api/partstudios/d/{DID}/w/{WID}/e/{EID}/stl"

    print(f"Requesting custom STL with Length = {dynamic_length_mm} mm...")

    # --- 4. EXECUTE THE PARAMETRIC METRIC REQUEST ---
    response = client.api_client.request(
        method='GET',
        url=api_url,
        query_params=[
            ('units', 'millimeter'),               
            # FIX 2: Changed from 'binary' to 'text' so the Onshape library can read it
            ('mode', 'text'),                    
            ('configuration', f'L={dynamic_length_mm} mm') 
        ]
    )

    # --- 5. SAVE THE RESULT ---
    if response.status == 200:
        file_name = f"fluidtest_{dynamic_length_mm}mm.stl"
        save_path = os.path.join(r"C:\Users\Anthony Feldmann\Downloads", file_name)
        
        # FIX 3: Changed 'wb' (Write Binary) to 'w' (Write Text)
        with open(save_path, 'w') as f:
            f.write(response.data)
        
        print(f"Success! Saved to: {save_path}")
        return save_path
        
    else:
        print(f"Error: Onshape API returned HTTP {response.status}")
        return None

# --- MANUAL TEST EXECUTION ---
if __name__ == "__main__":
    test_dimension = 300
    download_custom_stl(test_dimension)