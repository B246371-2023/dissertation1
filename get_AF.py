import requests

def download_cif(protein_id, directory="downloads"):
    url = f'https://alphafold.ebi.ac.uk/files/AF-{protein_id}-F1-model_v4.pdb'
    local_filename = f"{directory}/{protein_id}.pdb"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {local_filename}")
    else:
        print(f"Failed to download {protein_id}. HTTP Status Code: {response.status_code}")

def process_proteins(file_path, directory="downloads"):
    with open(file_path, 'r') as file:
        for line in file:
            protein_id = line.strip()
            download_cif(protein_id, directory)

if __name__ == "__main__":
    import os

    proteins_file_path = '/home/s2530615/dissertation/ruddii_proteome.txt'  # UniProt ID list name
    download_directory = 'downloads' 

    # Ensure file exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    process_proteins(proteins_file_path, download_directory)
