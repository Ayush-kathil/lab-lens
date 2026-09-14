import urllib.request
import urllib.parse
import json
import hashlib
import os
import time

SEARCH_TERMS = [
    "chemistry laboratory experiment setup",
    "titration setup laboratory",
    "distillation apparatus laboratory",
    "laboratory glassware setup",
    "chemistry practical apparatus"
]

HIGH_KEYWORDS = ["setup", "apparatus", "distillation", "titration", "experiment", "bench", "arrangement"]

def fetch_search_images(term, limit=10):
    url = (f"https://commons.wikimedia.org/w/api.php"
           f"?action=query&generator=search&gsrsearch={urllib.parse.quote(term)}"
           f"&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata"
           f"&format=json&gsrlimit={limit}")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'LabLens-Bot/2.0'})
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
        
        license_short = ext.get("LicenseShortName", {}).get("value", "").upper()
        if "CC" not in license_short and "PUBLIC DOMAIN" not in license_short and "PD" not in license_short:
            continue
            
        title = page_data.get("title", "").lower()
        desc = ext.get("ImageDescription", {}).get("value", "").lower()
        
        spatial_val = "MEDIUM"
        for kw in HIGH_KEYWORDS:
            if kw in title or kw in desc:
                spatial_val = "HIGH"
                break
                
        results.append({
            "title": page_data.get("title", ""),
            "url": info.get("url", ""),
            "descriptionurl": info.get("descriptionurl", ""),
            "artist": ext.get("Artist", {}).get("value", "Unknown"),
            "license": ext.get("LicenseShortName", {}).get("value", "Unknown"),
            "license_url": ext.get("LicenseUrl", {}).get("value", ""),
            "spatial_value": spatial_val
        })
    return results

def main():
    out_img_dir = "Dataset/SpatialComplianceReal/images"
    out_ann_dir = "Dataset/SpatialComplianceReal/annotations"
    manifest_path = "Dataset/SpatialComplianceReal/metadata/source_manifest.json"
    attrib_path = "Dataset/SpatialComplianceReal/metadata/ATTRIBUTION.md"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    existing_hashes = {m["original_sha256"] for m in manifest}
    sample_idx = len(manifest) + 1
    
    new_downloads = 0
    
    for term in SEARCH_TERMS:
        print(f"Fetching from search: {term}...")
        images = fetch_search_images(term, limit=10)
        for img in images:
            if new_downloads >= 15:
                break
                
            img_url = img["url"].split('?')[0]
            if not (img_url.lower().endswith(".jpg") or img_url.lower().endswith(".png") or img_url.lower().endswith(".jpeg")):
                continue
                
            sample_id = f"rw_{sample_idx:03d}"
            local_ext = img_url.split('.')[-1]
            local_filename = f"{sample_id}.{local_ext}"
            local_path = os.path.join(out_img_dir, local_filename)
            
            req = urllib.request.Request(img_url, headers={'User-Agent': 'LabLens-Bot/2.0'})
            try:
                with urllib.request.urlopen(req) as response:
                    img_data = response.read()
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
                continue
                
            sha256 = hashlib.sha256(img_data).hexdigest()
            if sha256 in existing_hashes:
                print(f"Duplicate hash skipped: {sha256}")
                continue
                
            with open(local_path, "wb") as f:
                f.write(img_data)
                
            existing_hashes.add(sha256)
            
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
                "spatial_value": img["spatial_value"],
                "modifications": []
            })
            
            with open(attrib_path, "a", encoding="utf-8") as f:
                f.write(f"## {sample_id}\n- **Title**: {img['title']}\n- **Creator**: {img['artist']}\n- **License**: [{img['license']}]({img['license_url']})\n- **Source**: {img['descriptionurl']}\n- **Spatial Value**: {img['spatial_value']}\n\n")
            
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
            with open(os.path.join(out_ann_dir, f"{sample_id}.json"), "w", encoding="utf-8") as f:
                json.dump(ann, f, indent=2)
                
            sample_idx += 1
            new_downloads += 1
            time.sleep(1.0)
            
        if new_downloads >= 15:
            break

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Successfully processed {new_downloads} new images.")

if __name__ == '__main__':
    main()
