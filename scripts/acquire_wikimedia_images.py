import urllib.request
import urllib.parse
import json
import hashlib
import os
import time

SEARCH_TERMS = [
    "laboratory beaker",
    "laboratory flask",
    "chemistry equipment"
]

def fetch_search_images(term, limit=15):
    url = (f"https://commons.wikimedia.org/w/api.php"
           f"?action=query&generator=search&gsrsearch={urllib.parse.quote(term)}"
           f"&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata"
           f"&format=json&gsrlimit={limit}")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'LabLens-Bot/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {term}: {e}")
        return []
        
    pages = data.get("query", {}).get("pages", {})
    results = []
    
    for page_id, page_data in pages.items():
        if "imageinfo" not in page_data:
            continue
        info = page_data["imageinfo"][0]
        ext = info.get("extmetadata", {})
        
        # Check license
        license_short = ext.get("LicenseShortName", {}).get("value", "").upper()
        if "CC" not in license_short and "PUBLIC DOMAIN" not in license_short and "PD" not in license_short:
            continue
            
        results.append({
            "title": page_data.get("title", ""),
            "url": info.get("url", ""),
            "descriptionurl": info.get("descriptionurl", ""),
            "artist": ext.get("Artist", {}).get("value", "Unknown"),
            "license": ext.get("LicenseShortName", {}).get("value", "Unknown"),
            "license_url": ext.get("LicenseUrl", {}).get("value", "")
        })
    return results

def main():
    out_img_dir = "Dataset/SpatialComplianceReal/images"
    out_ann_dir = "Dataset/SpatialComplianceReal/annotations"
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_ann_dir, exist_ok=True)
    
    manifest = []
    attributions = ["# ATTRIBUTION\n\nAll images sourced from Wikimedia Commons.\n"]
    
    sample_idx = 1
    for term in SEARCH_TERMS:
        print(f"Fetching from search: {term}...")
        images = fetch_search_images(term, limit=15)
        for img in images:
            if sample_idx > 20:
                break
                
            img_url = img["url"].split("?")[0]
            if not (img_url.lower().endswith(".jpg") or img_url.lower().endswith(".png") or img_url.lower().endswith(".jpeg")):
                continue
                
            sample_id = f"rw_{sample_idx:03d}"
            local_ext = img_url.split('.')[-1]
            local_filename = f"{sample_id}.{local_ext}"
            local_path = os.path.join(out_img_dir, local_filename)
            
            # Download
            req = urllib.request.Request(img_url, headers={'User-Agent': 'LabLens-Bot/1.0'})
            try:
                with urllib.request.urlopen(req) as response:
                    img_data = response.read()
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
                continue
                
            with open(local_path, "wb") as f:
                f.write(img_data)
                
            # SHA-256
            sha256 = hashlib.sha256(img_data).hexdigest()
            
            # Add to manifest
            manifest.append({
                "sample_id": sample_id,
                "session_id": f"session_{sample_idx:03d}",
                "split": "unassigned",
                "source_platform": "Wikimedia Commons",
                "source_page_url": img["descriptionurl"],
                "title": img["title"],
                "creator": img["artist"],
                "license": img["license"],
                "license_url": img["license_url"],
                "retrieval_date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "original_filename": img["url"].split('/')[-1],
                "original_sha256": sha256,
                "local_filename": local_filename,
                "modifications": []
            })
            
            # Add to attribution
            attributions.append(f"## {sample_id}\n- **Title**: {img['title']}\n- **Creator**: {img['artist']}\n- **License**: [{img['license']}]({img['license_url']})\n- **Source**: {img['descriptionurl']}\n")
            
            # Create dummy annotation
            ann = {
                "sample_id": sample_id,
                "session_id": f"session_{sample_idx:03d}",
                "split": "unassigned",
                "annotation_status": "NEEDS_REVIEW",
                "image_metadata": {
                    "filename": local_filename,
                    "width": 1000, 
                    "height": 1000,
                    "viewpoint": "unknown"
                },
                "objects": [],
                "setup_specification": {
                    "setup_name": "unknown_setup",
                    "required_objects": {},
                    "regions": {},
                    "spatial_rules": []
                },
                "ground_truth": {
                    "compliant": False,
                    "violations": []
                }
            }
            # write annotation
            with open(os.path.join(out_ann_dir, f"{sample_id}.json"), "w", encoding="utf-8") as f:
                json.dump(ann, f, indent=2)
                
            sample_idx += 1
            time.sleep(0.5)

    with open("Dataset/SpatialComplianceReal/metadata/source_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    with open("Dataset/SpatialComplianceReal/metadata/ATTRIBUTION.md", "w", encoding="utf-8") as f:
        f.write("\n".join(attributions))
        
    print(f"Successfully processed {len(manifest)} images.")

if __name__ == '__main__':
    main()
