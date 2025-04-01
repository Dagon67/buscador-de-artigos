import os
import logging
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scraper import PaperScraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_papers_by_topic():
    """Load papers organized by topic"""
    topics = {
        "Giftedness": [
            "superintelligence", "gifted brain", "extreme cognition", "divergent thinking",
            "high IQ creativity", "prodigy", "neurodiversity gifted", "exceptional perception"
        ],
        "Alternative Learning": [
            "differentiated learning", "accelerated learning", "multimodal instruction",
            "personalized strategies", "adaptive learning", "self-paced discovery",
            "experiential learning", "peer learning"
        ],
        "Historical Figures": [
            "historical polymaths", "visionary innovators", "nonconventional geniuses",
            "eccentric prodigies", "legacy of genius", "alternative perception history"
        ],
        "Brain Topology": [
            "neural connectivity", "cerebral lateralization", "brain morphology",
            "white matter integrity", "functional mapping", "cortical thickness",
            "hemispheric asymmetry", "brain plasticity"
        ],
        "Types of Intelligence": [
            "ontological intelligence", "heuristic intelligence", "spatial intelligence",
            "musical intelligence", "mathematical intelligence", "linguistic intelligence",
            "kinesthetic intelligence", "intrapersonal intelligence", "interpersonal intelligence",
            "naturalistic intelligence", "existential intelligence", "emotional intelligence"
        ],
        "Learning Methods": [
            "intelligence-tailored pedagogy", "multimodal curriculum", "sensory-based learning",
            "gamification education", "musical mnemonics", "problem-based learning",
            "visual-spatial instruction", "kinesthetic strategies", "collaborative inquiry",
            "creative workshops"
        ],
        "Interdisciplinary": [
            "neuroscience pedagogy", "cognitive psychology gifted", "educational neuroscience",
            "neuroeducation theories", "diversity models education", "bio-psycho-social gifted"
        ],
        "Cultural Dimensions": [
            "cultural giftedness", "social construct intelligence", "evolution of genius",
            "societal prodigies", "educational equity gifted", "gifted stereotypes",
            "diversity high abilities", "innovation culture"
        ],
        "Metacognition": [
            "metacognitive strategies", "self-regulated learning", "creativity dynamics",
            "cognitive load management", "executive functions education",
            "heuristic problem solving", "intuitive reasoning", "knowledge integration"
        ]
    }
    return topics

def load_checkpoint():
    """Load the checkpoint file if it exists"""
    checkpoint_file = os.path.join(os.path.dirname(__file__), 'downloads', 'checkpoint.json')
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return json.load(f)
    return {
        'downloaded_papers': [],
        'current_topic': '',
        'current_term': '',
        'total_downloaded': 0,
        'last_publisher': ''
    }

def save_checkpoint(checkpoint_data):
    """Save the current progress to checkpoint file"""
    checkpoint_file = os.path.join(os.path.dirname(__file__), 'downloads', 'checkpoint.json')
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint_data, f, indent=4)

def search_and_download_papers():
    """Search for and download papers for each topic with checkpointing"""
    # Initialize scraper
    scraper = PaperScraper()
    
    # Create downloads directory structure
    base_dir = os.path.join(os.path.dirname(__file__), 'downloads')
    os.makedirs(base_dir, exist_ok=True)
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    downloaded_papers = set(checkpoint['downloaded_papers'])
    total_downloaded = checkpoint['total_downloaded']
    
    # Load topics and search terms
    topics = load_papers_by_topic()
    
    # Publishers to search
    publishers = [
        "frontiersin.org",
        "mdpi.com",
        "nature.com",
        "plos.org",
        "biomedcentral.com",
        "hindawi.com",
        "scielo.org",
        "tandfonline.com",
        "sagepub.com"
    ]
    
    # Start from last checkpoint if exists
    topics_items = list(topics.items())
    if checkpoint['current_topic']:
        topic_idx = next(i for i, (t, _) in enumerate(topics_items) if t == checkpoint['current_topic'])
        topics_items = topics_items[topic_idx:]
    
    for topic, search_terms in topics_items:
        # Create topic directory
        topic_dir = os.path.join(base_dir, topic.replace(" ", "_"))
        os.makedirs(topic_dir, exist_ok=True)
        
        logger.info(f"\nProcessing topic: {topic}")
        
        # Start from last search term if exists
        if checkpoint['current_topic'] == topic and checkpoint['current_term']:
            term_idx = search_terms.index(checkpoint['current_term'])
            search_terms = search_terms[term_idx:]
        
        for search_term in search_terms:
            logger.info(f"\nSearching for papers related to: {search_term}")
            
            # Start from last publisher if exists
            pub_idx = publishers.index(checkpoint['last_publisher']) if checkpoint['last_publisher'] else 0
            for publisher in publishers[pub_idx:]:
                try:
                    # Update checkpoint
                    checkpoint.update({
                        'current_topic': topic,
                        'current_term': search_term,
                        'last_publisher': publisher
                    })
                    save_checkpoint(checkpoint)
                    
                    # Construct search URL based on publisher
                    if "frontiersin.org" in publisher:
                        search_url = f"https://www.frontiersin.org/search?q={search_term}"
                    elif "mdpi.com" in publisher:
                        search_url = f"https://www.mdpi.com/search?q={search_term}"
                    elif "nature.com" in publisher:
                        search_url = f"https://www.nature.com/search?q={search_term}"
                    else:
                        continue
                    
                    # Get paper URL and attempt download
                    try:
                        filename = f"{search_term.replace(' ', '_')}_{publisher.split('.')[0]}.pdf"
                        save_path = os.path.join(topic_dir, filename)
                        
                        if save_path not in downloaded_papers:
                            success = scraper.get_pdf(search_url, save_path)
                            if success:
                                downloaded_papers.add(save_path)
                                checkpoint['downloaded_papers'].append(save_path)
                                total_downloaded += 1
                                checkpoint['total_downloaded'] = total_downloaded
                                save_checkpoint(checkpoint)
                                
                                logger.info(f"Successfully downloaded: {filename}")
                                logger.info(f"Total papers downloaded: {total_downloaded}")
                                
                                # Pause every 100 papers
                                if total_downloaded % 100 == 0:
                                    logger.info(f"\n=== Downloaded {total_downloaded} papers ===")
                                    logger.info("Taking a 60-second break...")
                                    time.sleep(60)
                                    logger.info("Resuming downloads...\n")
                            else:
                                logger.warning(f"Failed to download from {publisher}")
                        else:
                            logger.info(f"Skipping already downloaded: {filename}")
                            
                    except Exception as e:
                        logger.error(f"Error downloading from {publisher}: {str(e)}")
                    
                    # Wait between downloads
                    time.sleep(5)
                    
                except Exception as e:
                    logger.error(f"Error processing {publisher}: {str(e)}")
                    continue
            
            # Clear last publisher after completing a search term
            checkpoint['last_publisher'] = ''
            save_checkpoint(checkpoint)
        
        # Clear current term after completing a topic
        checkpoint['current_term'] = ''
        save_checkpoint(checkpoint)
    
    logger.info(f"\n=== Download session complete ===")
    logger.info(f"Total papers downloaded: {total_downloaded}")

if __name__ == "__main__":
    search_and_download_papers() 