import os
from onshape_client.client import Client

DID = '460766ee1fd3b3b2a615b94a'
WID = '979042f4d058b6f5579afa14'
EID = '1dbb2720f9be98854d69ba84'

def download_custom_stl(dynamic_length_mm):
    """Requests a custom-sized, metric STL from Onshape."""
    client = Client(configuration={
        "base_url": "https://cad-usw2.onshape.com", 
        "access_key": "on_KGHB3Hg5gDl4hPffcpuCd",
        "secret_key": "he1iDT28dxOsLz7Ww5TAVXgcj1PopbihMT50NKyMcmacO0pc"
    })

    api_url = f"https://cad-usw2.onshape.com/api/partstudios/d/{DID}/w/{WID}/e/{EID}/stl"
    
    response = client.api_client.request(
        method='GET',
        url=api_url,
        query_params=[('units', 'millimeter'), ('mode', 'text'), ('configuration', f'L={dynamic_length_mm} mm')]
    )

    if response.status == 200:
        base_dir = "/home/rpl/workspaces/rpl_dev/prusa_mk4s_module/output_files"
        os.makedirs(base_dir, exist_ok=True)
        
        output_file = os.path.join(base_dir, f"fluidtest_{dynamic_length_mm}mm.stl")
        with open(output_file, 'w') as f:
            f.write(response.data)
        return output_file
    return None

if __name__ == "__main__":
    test_dimension = 300
    download_custom_stl(test_dimension)
