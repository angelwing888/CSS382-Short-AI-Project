import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

BASE_URL = "https://www.marvelrivals.com/balancepost/"
BALANCE_POSTS_API = "https://www.marvelrivals.com/api/searchbalancepost"

def fetch_all_balance_patches():
    """
    Fetch all balance patch data from Marvel Rivals
    """
    all_patches = []
    page = 1
    
    while True:
        try:
            params = {
                "pageNum": page,
                "pageSize": 10
            }
            
            response = requests.get(BALANCE_POSTS_API, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' not in data or not data['data']:
                break
            
            posts = data['data']
            
            for post in posts:
                patch_info = {
                    'title': post.get('name', ''),
                    'date': post.get('update_time', ''),
                    'url': post.get('h5_url', ''),
                    'characters': []
                }
                
                # Fetch detailed balance info from each post
                if patch_info['url']:
                    char_adjustments = parse_balance_post(patch_info['url'])
                    patch_info['characters'] = char_adjustments
                
                all_patches.append(patch_info)
                time.sleep(0.5)  # Be respectful to the server
            
            page += 1
            time.sleep(1)  # Rate limiting between pages
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        except json.JSONDecodeError:
            print(f"Error decoding JSON on page {page}")
            break
    
    return all_patches


def parse_balance_post(post_url):
    """
    Parse individual balance post to extract character adjustments
    """
    try:
        response = requests.get(post_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all sections with character names and adjustments
        characters = []
        
        # Look for common patterns in balance posts
        # This is a general parser that looks for headers and following text
        sections = soup.find_all(['h2', 'h3', 'h4'])
        
        for section in sections:
            text = section.get_text(strip=True)
            
            # Check if this looks like a character name
            if text and len(text) < 50:  # Character names are usually short
                # Get the following paragraph as adjustment details
                next_elem = section.find_next(['p', 'ul', 'div'])
                if next_elem:
                    adjustment = next_elem.get_text(strip=True)
                    if adjustment and len(adjustment) > 10:
                        characters.append({
                            'name': text,
                            'adjustment': adjustment[:200]  # Limit to first 200 chars
                        })
        
        return characters
    
    except Exception as e:
        print(f"Error parsing {post_url}: {e}")
        return []


def get_heroes_with_adjustments():
    """
    Fetch all patches and organize by character
    Returns a dict with character names as keys and list of adjustments as values
    """
    patches = fetch_all_balance_patches()
    
    heroes_dict = {}
    
    for patch in patches:
        for char in patch['characters']:
            char_name = char['name']
            
            if char_name not in heroes_dict:
                heroes_dict[char_name] = []
            
            heroes_dict[char_name].append({
                'patch': patch['title'],
                'date': patch['date'],
                'adjustment': char['adjustment']
            })
    
    return heroes_dict


def save_to_json(data, filename='balance_data.json'):
    """
    Save the scraped data to a JSON file for use by the web app
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")


if __name__ == '__main__':
    print("Fetching Marvel Rivals balance patches...")
    heroes_data = get_heroes_with_adjustments()
    save_to_json(heroes_data)
    print(f"Found {len(heroes_data)} heroes with adjustments")
