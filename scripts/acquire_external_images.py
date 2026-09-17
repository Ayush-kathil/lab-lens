import urllib.request
import urllib.parse
import json
import os
import time
import hashlib
from datetime import datetime
import csv
import re
from urllib.error import HTTPError

USER_AGENT = 'AyushKathilLabLensResearch/1.0 (ayush@example.com)'
BROWSER_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

def request_with_retry(url, headers, max_retries=5):
    retries = 0
    backoff = 2
    while retries < max_retries:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                return response.read()
        except HTTPError as e:
            if e.code == 429:
                retry_after = e.headers.get('Retry-After')
                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                else:
                    wait_time = backoff
                print(f"HTTP 429 Too Many Requests. Retrying in {wait_time} seconds... (Attempt {retries+1}/{max_retries})")
                time.sleep(wait_time)
                backoff *= 2
                retries += 1
            else:
                raise e
        except Exception as e:
            print(f"Network error: {e}. Retrying in {backoff} seconds...")
            time.sleep(backoff)
            backoff *= 2
            retries += 1
    raise Exception(f"Failed to fetch {url} after {max_retries} retries.")

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
    try:
        data = json.loads(request_with_retry(url, {'User-Agent': USER_AGENT}).decode('utf-8'))
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
    try:
        data = json.loads(request_with_retry(url, {'User-Agent': USER_AGENT}).decode('utf-8'))
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
    os.makedirs('Dataset/ExternalLabBench/images', exist_ok=True)
    os.makedirs('Dataset/ExternalLabBench/labels', exist_ok=True)
    manifest_path = 'outputs/external_evaluation/external_manifest.csv'
    header = ['image_id', 'filename', 'source_page_url', 'direct_image_url', 'creator', 'license', 'license_url', 'retrieval_timestamp', 'width', 'height', 'sha256', 'duplicate_status', 'duplicate_reference', 'dataset_role', 'annotation_status', 'ground_truth_status']

    # Load existing manifest to skip downloaded
    existing_urls = set()
    records = []
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_urls.add(row['direct_image_url'])
                records.append(row)
    
    # We do NOT expand the dataset yet as per the instructions, 
    # but the script is robustly implemented.
    print("Download script robustness improved (Phase 4). Expansion paused until audit clears.")

if __name__ == '__main__':
    main()
