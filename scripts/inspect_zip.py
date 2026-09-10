import zipfile
import json
import os
from collections import Counter
from pathlib import Path

def analyze_zip(zip_path, output_json):
    if not os.path.exists(zip_path):
        print(f"File not found: {zip_path}")
        return
        
    print(f"Analyzing {zip_path}...")
    size = os.path.getsize(zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        info_list = z.infolist()
        total_entries = len(info_list)
        
        extensions = Counter()
        directories = 0
        metadata_files = []
        
        # We also want to record the order to see if images/labels are adjacent
        files_in_order = []
        
        for info in info_list:
            if info.is_dir():
                directories += 1
                continue
                
            path = Path(info.filename)
            ext = path.suffix.lower()
            extensions[ext] += 1
            
            files_in_order.append(info.filename)
            
            if ext in ['.json', '.yaml', '.csv', '.xml', '.txt', '.md']:
                # For txt, only record if it's not in labels dir to avoid listing all 4500 labels
                if 'labels' not in path.parts:
                    metadata_files.append(info.filename)
            elif 'readme' in path.name.lower():
                metadata_files.append(info.filename)
                
        inventory = {
            'archive_path': zip_path,
            'archive_size_bytes': size,
            'total_entries': total_entries,
            'directories': directories,
            'extensions': dict(extensions),
            'metadata_files': metadata_files,
            'files_in_order_sample': files_in_order[:20] # Just a sample to avoid huge json
        }
        
    with open(output_json, 'w') as f:
        json.dump(inventory, f, indent=2)
        
    print("Inventory saved.")
    
if __name__ == '__main__':
    zip_path = r"C:\Users\shiva\Downloads\ChemEq25 (Main paper Scientific Data journal, Titl.zip"
    analyze_zip(zip_path, "outputs/chemeq25_archive_inventory.json")
