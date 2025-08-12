import requests
import json
import time

def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_data(data):
    if not data:
        return []
    
    results = []
    for item in data:
        processed = {
            'id': item.get('id'),
            'name': item.get('name'),
            'status': item.get('status', 'unknown')
        }
        results.append(processed)
    
    return results

def main():
    url = "https://api.example.com/data"
    data = fetch_data(url)
    results = process_data(data)
    
    for result in results:
        print(f"ID: {result['id']}, Name: {result['name']}")
    
    return results

if __name__ == "__main__":
    main()