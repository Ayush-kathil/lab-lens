import urllib.request
import urllib.parse
import json
import os
import time
import hashlib
from datetime import datetime
import csv
import re

USER_AGENT = 'AyushKathilLabLensResearch/1.0 (ayush@example.com)'

def search_wikimedia_titles(query, limit=30):
    params = urllib.parse.urlencode({
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'srnamespace': '6',
        'srlimit': limit
    })
    url = f'https://commons.wikimedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return [item['title'] for item in data.get('query', {}).get('search', [])]
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def get_image_info(titles):
    results = []
    params = urllib.parse.urlencode({
        'action': 'query',
        'format': 'json',
        'prop': 'imageinfo',
        'titles': '|'.join(titles),
        'iiprop': 'url|extmetadata|dimensions'
    }, safe='|')
    url = f'https://commons.wikimedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_info in pages.items():
                title = page_info.get('title', '')
                if 'imageinfo' in page_info:
                    info = page_info['imageinfo'][0]
                    ext = info.get('extmetadata', {})
                    license_name = ext.get('LicenseShortName', {}).get('value', 'Unknown')
                    license_url = ext.get('LicenseUrl', {}).get('value', 'Unknown')
                    artist = ext.get('Artist', {}).get('value', 'Unknown')
                    desc_url = info.get('descriptionurl', '')
                    img_url = info.get('url', '')
                    
                    base_url = img_url.split('?')[0]
                    if base_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                        artist_clean = re.sub(r'<[^>]+>', '', str(artist)).replace('\n', ' ')[:100]
                        # Fix encoding issues by ascii encoding and ignoring bad chars
                        artist_clean = artist_clean.encode('ascii', 'ignore').decode('ascii')
                        license_name = str(license_name).encode('ascii', 'ignore').decode('ascii')
                        
                        results.append({
                            'filename': title.replace('File:', '').replace(' ', '_').encode('ascii', 'ignore').decode('ascii'),
                            'source_page_url': desc_url,
                            'direct_image_url': base_url,
                            'creator': artist_clean,
                            'license': license_name,
                            'license_url': str(license_url).replace('\n', ' '),
                            'width': info.get('width', 0),
                            'height': info.get('height', 0)
                        })
    except Exception as e:
        print('Error in image info:', e)
    return results

def main():
    queries = ['chemistry beaker', 'erlenmeyer flask laboratory', 'test tube chemistry', 'laboratory bench', 'volumetric flask']
    all_titles = set()
    for q in queries:
        titles = search_wikimedia_titles(q, 30)
        all_titles.update(titles)
        time.sleep(1)

    all_titles = list(all_titles)[:120]
    print(f'Found {len(all_titles)} titles')

    all_images = []
    for i in range(0, len(all_titles), 20):
        batch = all_titles[i:i+20]
        all_images.extend(get_image_info(batch))
        time.sleep(2)

    print(f'Got info for {len(all_images)} images')

    os.makedirs('Dataset/ExternalLabBench/images', exist_ok=True)
    os.makedirs('Dataset/ExternalLabBench/labels', exist_ok=True)

    manifest_path = 'outputs/external_evaluation/external_manifest.csv'
    header = ['image_id', 'filename', 'source_page_url', 'direct_image_url', 'creator', 'license', 'license_url', 'retrieval_timestamp', 'width', 'height', 'sha256', 'duplicate_status', 'duplicate_reference', 'dataset_role', 'annotation_status', 'ground_truth_status']

    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        count = 0
        for idx, img in enumerate(all_images):
            if count >= 50:
                break
            try:
                browser_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                req = urllib.request.Request(img['direct_image_url'], headers={'User-Agent': browser_ua})
                with urllib.request.urlopen(req) as response:
                    img_data = response.read()
                    
                img_sha256 = hashlib.sha256(img_data).hexdigest()
                fname = f'ext_{count:03d}.jpg' if img['direct_image_url'].lower().endswith(('.jpg', '.jpeg')) else f'ext_{count:03d}.png'
                out_path = os.path.join('Dataset/ExternalLabBench/images', fname)
                
                with open(out_path, 'wb') as out_f:
                    out_f.write(img_data)
                    
                writer.writerow([
                    f'ext_{count:03d}',
                    fname,
                    img['source_page_url'],
                    img['direct_image_url'],
                    img['creator'],
                    img['license'],
                    img['license_url'],
                    datetime.utcnow().isoformat() + 'Z',
                    img['width'],
                    img['height'],
                    img_sha256,
                    'UNIQUE', 
                    '',
                    'UNASSIGNED', 
                    'HUMAN_REVIEW_REQUIRED',
                    'PENDING'
                ])
                count += 1
                if count % 10 == 0:
                    print(f'Downloaded {count}')
                time.sleep(0.5)
            except Exception as e:
                print(f'Failed to download {img["direct_image_url"]}: {e}')

    print(f'Successfully downloaded {count} images and wrote manifest.')

if __name__ == '__main__':
    main()
