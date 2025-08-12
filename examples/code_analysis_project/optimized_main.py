import asyncio
import aiohttp
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_data(self, endpoint: str) -> Optional[List[Dict]]:
        """Fetch data from API with proper error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            async with self.session.get(url, timeout=self.timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Successfully fetched {len(data)} items from {endpoint}")
                    return data
                else:
                    logger.error(f"API request failed: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def process_data(self, data: Optional[List[Dict]]) -> List[Dict]:
        """Process data with validation and error handling"""
        if not data:
            logger.warning("No data to process")
            return []
        
        results = []
        for item in data:
            try:
                processed = {
                    'id': item.get('id'),
                    'name': item.get('name', 'Unknown'),
                    'status': item.get('status', 'unknown'),
                    'processed_at': datetime.now().isoformat()
                }
                
                # Validate required fields
                if processed['id'] is None:
                    logger.warning(f"Skipping item without ID: {item}")
                    continue
                
                results.append(processed)
            except Exception as e:
                logger.error(f"Error processing item {item}: {e}")
        
        logger.info(f"Processed {len(results)} items successfully")
        return results

async def main():
    """Main function with proper async handling"""
    config = {
        'base_url': os.getenv('API_BASE_URL', 'https://api.example.com'),
        'timeout': int(os.getenv('API_TIMEOUT', '10'))
    }
    
    async with DataProcessor(config['base_url'], config['timeout']) as processor:
        data = await processor.fetch_data('data')
        results = processor.process_data(data)
        
        for result in results:
            print(f"ID: {result['id']}, Name: {result['name']}, Status: {result['status']}")
        
        return results

if __name__ == "__main__":
    asyncio.run(main())