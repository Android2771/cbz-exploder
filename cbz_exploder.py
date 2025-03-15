import os
import re
import zipfile
import shutil

# Get inputs from user
directory = input("Insert directory on where to extract cbz files: ")
title = input("Insert title of series: ")
    
# Define paths
output_dir_path = f"{directory}/output"
tmp_dir_path = f"{directory}/tmp"

# Clean output directory if exists and make anew
if os.path.exists(output_dir_path):
    shutil.rmtree(output_dir_path)
os.makedirs(output_dir_path)

# Function which extracts important information from filename
def extract_numbers_from_file(filename):
    reg = re.search(r"[Vv].*?(\d+).*?[Cc]?.*?(\d+)\.?(\d*)", filename)
    vol_no = reg.group(1)
    chap_no = reg.group(2)
    chap_minor_part = reg.group(3)
    return [vol_no, chap_no, chap_minor_part]
    
for file in os.listdir(directory):
    if file.endswith(".cbz"): 
        print(f"PROCESSING {file}")
        [vol_no, chap_no, chap_minor_part] = extract_numbers_from_file(file)
        print(f"""EXPLODED {title} Volume {vol_no} Chapter {chap_no if chap_no.isalnum() else "0"}.{chap_minor_part if chap_minor_part.isalnum() else "0"}""")
        
        with zipfile.ZipFile(os.path.join(directory, file), 'r') as zip_ref:            
            if not os.path.exists(tmp_dir_path):
                os.makedirs(tmp_dir_path)
                
            # For every cbz, extract all to temp directory
            zip_ref.extractall(tmp_dir_path)
            
            for root, subdirs, files in os.walk(tmp_dir_path):               
                for file in files:
                            
                    # Create directory inside output dir for each volume to organise all pages
                    if not os.path.exists(f"{output_dir_path}/{title} Volume {vol_no}"):
                        os.makedirs(f"{output_dir_path}/{title} Volume {vol_no}")
                        
                    os.rename(os.path.join(root, file), os.path.join(output_dir_path, f"{title} Volume {vol_no}/C{chap_no}_{chap_minor_part}_{file}"))
                
            shutil.rmtree(tmp_dir_path)
