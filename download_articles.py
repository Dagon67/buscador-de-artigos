import requests
import json
import os
from datetime import datetime
import urllib.parse
import re
from bs4 import BeautifulSoup
import time
from scraper import download_paper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_valid_filename(title):
    # Remove invalid characters and limit length
    valid_name = re.sub(r'[<>:"/\\|?*]', '', title)
    valid_name = valid_name.replace('\n', ' ').strip()
    if len(valid_name) > 100:
        valid_name = valid_name[:97] + '...'
    return valid_name + '.pdf'

def download_articles_from_json(json_file):
    logger.info(f"Starting to process {json_file}")
    
    try:
        # Create downloads directory
        base_dir = "artiguinhos/downloads"
        os.makedirs(base_dir, exist_ok=True)
        logger.info(f"Created/verified base directory: {base_dir}")
        
        # Load JSON data
        logger.info(f"Loading JSON file: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get category from filename
        category = os.path.basename(json_file).split('_')[0]
        category_dir = os.path.join(base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        logger.info(f"Created/verified category directory: {category_dir}")
        
        downloaded = 0
        
        # Handle both list and single object formats
        if isinstance(data, list):
            sources_data = data
        else:
            sources_data = [data]
        
        for source_data in sources_data:
            if isinstance(source_data, str):
                logger.warning(f"Skipping string data: {source_data}")
                continue
                
            source = source_data.get('source', '')
            results = source_data.get('results', [])
            
            logger.info(f"\nProcessing {source} articles ({len(results)} articles found)...")
            
            for article in results:
                if not article.get('url'):
                    logger.warning(f"Skipping article without URL: {article.get('title', 'No title')}")
                    continue
                    
                filename = create_valid_filename(article['title'])
                save_path = os.path.join(category_dir, filename)
                
                if os.path.exists(save_path):
                    logger.info(f"Already downloaded: {filename}")
                    downloaded += 1
                    continue
                
                logger.info(f"Attempting to download: {filename}")
                logger.info(f"URL: {article['url']}")
                
                # Extract DOI if available
                doi = None
                if source == 'CrossRef' and article['url'].startswith('https://doi.org/'):
                    doi = article['url'].replace('https://doi.org/', '')
                elif 'doi' in article:
                    doi = article['doi']
                
                if doi:
                    logger.info(f"Found DOI: {doi}")
                
                # Prepare paper info
                paper_info = {
                    'title': article['title'],
                    'url': article['url'],
                    'doi': doi,
                    'authors': article.get('authors', []),
                    'abstract': article.get('abstract', ''),
                    'journal': article.get('journal', '')
                }
                
                success = download_paper(paper_info, save_path)
                
                if success:
                    logger.info(f"Successfully downloaded: {filename}")
                    downloaded += 1
                else:
                    logger.error(f"Failed to download: {filename}")
                    if os.path.exists(save_path):
                        os.remove(save_path)
                
                # Add delay between downloads
                time.sleep(1)
        
        return downloaded
        
    except Exception as e:
        logger.error(f"Error in download_articles_from_json: {e}", exc_info=True)
        return 0

def main():
    try:
        # Process all JSON files in artiguinhos directory
        json_files = [f for f in os.listdir('artiguinhos') if f.endswith('.json')]
        logger.info(f"Found JSON files: {json_files}")
        
        total_downloaded = 0
        
        for json_file in json_files:
            logger.info(f"\nProcessing category from {json_file}...")
            downloaded = download_articles_from_json(os.path.join('artiguinhos', json_file))
            total_downloaded += downloaded
            logger.info(f"Downloaded {downloaded} articles from {json_file}")
        
        logger.info(f"\nTotal articles downloaded: {total_downloaded}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main() 