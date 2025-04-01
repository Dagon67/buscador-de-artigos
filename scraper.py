import os
import requests
import logging
import random
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlparse, urlencode
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PaperScraper:
    def __init__(self):
        """Initialize the scraper with session and logging."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Configure retry settings
        self.max_retries = 3
        self.retry_delay = 5
        self.timeout = 30

    def _is_potential_pdf_url(self, url):
        """Check if a URL is potentially a PDF link."""
        if not url:
            return False

        url_lower = url.lower()
        indicators = [
            '.pdf',
            '/pdf',
            'pdf?',
            'download=pdf',
            'download=true',
            'getpdf',
            'download-pdf',
            'pdf/download',
            'pdf_file',
            'fulltext.pdf'
        ]
        return any(indicator in url_lower for indicator in indicators)

    def _make_request(self, url, stream=False):
        """Make a request with retries and error handling"""
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Request attempt {attempt + 1}/{self.max_retries} for {url}")
                response = self.session.get(url, stream=stream, timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (attempt + 1)
                    logger.info(f"Waiting {delay} seconds before retry...")
                    time.sleep(delay)
                else:
                    raise

    def _extract_pdf_urls(self, html_content, url):
        """Extract PDF URLs from HTML content."""
        self.logger.info(f"Parsing HTML content from {url}")
        soup = BeautifulSoup(html_content, 'html.parser')
        pdf_urls = []
        domain = urlparse(url).netloc
        
        self.logger.info(f"Checking patterns for domain: {domain}")
        
        # PLOS ONE
        if 'journals.plos.org' in domain:
            self.logger.info("Found matching publisher: plos")
            meta_tags = soup.find_all('meta', attrs={'name': 'citation_pdf_url'})
            self.logger.info(f"Found {len(meta_tags)} elements matching meta with attrs {{'name': 'citation_pdf_url'}}")
            for meta in meta_tags:
                pdf_url = meta.get('content')
                if pdf_url:
                    if not pdf_url.startswith('http'):
                        pdf_url = urljoin(url, pdf_url)
                    pdf_urls.append(pdf_url)
                    self.logger.info(f"Found potential PDF URL: {pdf_url}")

        elif 'www.mdpi.com' in domain:
            self.logger.info("Found matching publisher: mdpi")
            # Check meta tag
            meta_pdf = soup.find('meta', attrs={'name': 'citation_pdf_url'})
            if meta_pdf:
                self.logger.info("Found 1 elements matching meta with attrs {'name': 'citation_pdf_url'}")
                pdf_url = meta_pdf.get('content')
                if self._is_potential_pdf_url(pdf_url):
                    self.logger.info(f"Found potential PDF URL: {pdf_url}")
                    pdf_urls.append(pdf_url)

        elif 'frontiersin.org' in domain:
            self.logger.info("Found matching publisher: frontiers")
            # Try multiple patterns
            pdf_link = soup.find('a', attrs={'class': 'download-files-pdf'})
            if pdf_link:
                pdf_url = pdf_link.get('href')
                if self._is_potential_pdf_url(pdf_url):
                    pdf_urls.append(pdf_url)
            else:
                # Try alternative pattern
                pdf_url = url.replace('/full', '/pdf')
                if self._is_potential_pdf_url(pdf_url):
                    pdf_urls.append(pdf_url)

        elif 'biomedcentral.com' in domain:
            self.logger.info("Found matching publisher: bmc")
            # Check meta tag
            meta_pdf = soup.find('meta', attrs={'name': 'citation_pdf_url'})
            if meta_pdf:
                self.logger.info("Found 1 elements matching meta with attrs {'name': 'citation_pdf_url'}")
                pdf_url = meta_pdf.get('content')
                if self._is_potential_pdf_url(pdf_url):
                    self.logger.info(f"Found potential PDF URL: {pdf_url}")
                    pdf_urls.append(pdf_url)

        elif 'nature.com' in domain:
            self.logger.info("Found matching publisher: nature")
            # Check meta tag
            meta_pdf = soup.find('meta', attrs={'name': 'citation_pdf_url'})
            if meta_pdf:
                self.logger.info("Found 1 elements matching meta with attrs {'name': 'citation_pdf_url'}")
                pdf_url = meta_pdf.get('content')
                if self._is_potential_pdf_url(pdf_url):
                    self.logger.info(f"Found potential PDF URL: {pdf_url}")
                    pdf_urls.append(pdf_url)

        elif 'ncbi.nlm.nih.gov' in domain:
            self.logger.info("Found matching publisher: pmc")
            # Look for PDF links in PMC articles
            pdf_links = soup.find_all('a', href=True)
            for link in pdf_links:
                if 'pdf' in link.text.lower() and '/pmc/articles/' in link['href']:
                    pdf_url = 'https://www.ncbi.nlm.nih.gov' + link['href']
                    if self._is_potential_pdf_url(pdf_url):
                        pdf_urls.append(pdf_url)
                    break

        # Generic patterns for other publishers
        if not pdf_urls:
            # Try common patterns
            self.logger.info("Trying generic patterns")
            # Check meta tags
            meta_pdf = soup.find('meta', attrs={'name': 'citation_pdf_url'})
            if meta_pdf:
                pdf_url = meta_pdf.get('content')
                if self._is_potential_pdf_url(pdf_url):
                    pdf_urls.append(pdf_url)

            # Check for PDF download links
            pdf_links = soup.find_all('a', href=True)
            for link in pdf_links:
                href = link['href']
                if self._is_potential_pdf_url(href):
                    # Make URL absolute if it's relative
                    pdf_url = urljoin(url, href)
                    pdf_urls.append(pdf_url)

        # Log results
        self.logger.info(f"Found {len(pdf_urls)} total PDF URLs")
        return pdf_urls

    def _try_direct_download(self, url, save_path):
        """Try to download PDF directly from URL."""
        try:
            self.logger.info(f"Attempting direct download from: {url}")
            response = self._make_request(url, stream=True)
            
            # Check if response is a PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' in content_type or url.lower().endswith('.pdf'):
                self.logger.info(f"Response content type: {content_type}")
                self.logger.info(f"Saving PDF to: {save_path}")
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify file size
                file_size = os.path.getsize(save_path)
                self.logger.info(f"Successfully saved PDF ({file_size} bytes)")
                return True
            else:
                self.logger.warning(f"Response is not a PDF (content-type: {content_type})")
                return False
                
        except Exception as e:
            self.logger.error(f"Direct download failed: {str(e)}")
            self.logger.error(traceback.format_exc())
            return False

    def _try_alternative_urls(self, url, doi):
        """Generate alternative URLs to try"""
        alt_urls = set()
        
        # Parse the original URL
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        
        # Add DOI-based URLs if available
        if doi:
            alt_urls.add(f"https://doi.org/{doi}")
            
            # Try common PDF URL patterns
            if 'frontiers' in domain:
                alt_urls.add(f"https://www.frontiersin.org/articles/{doi}/pdf")
            elif 'nature' in domain:
                alt_urls.add(f"https://www.nature.com/articles/{doi}.pdf")
            elif 'mdpi' in domain:
                article_id = path.split('/')[-1]
                alt_urls.add(f"https://www.mdpi.com/article/{article_id}/pdf")
            elif 'biomedcentral' in domain:
                alt_urls.add(f"https://bmcmedinformdecismak.biomedcentral.com/track/pdf/{doi}.pdf")
        
        # Add variations of the original URL
        if 'article' in path:
            pdf_path = path.replace('article', 'pdf')
            alt_urls.add(urljoin(url, pdf_path))
        
        if 'full' in path:
            pdf_path = path.replace('full', 'pdf')
            alt_urls.add(urljoin(url, pdf_path))
        
        return list(alt_urls)

    def get_pdf_url(self, page_url):
        """Extract PDF URL from article page"""
        try:
            response = self._make_request(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Handle different publishers
            domain = urlparse(page_url).netloc
            pdf_url = None
            
            if 'frontiersin.org' in domain:
                pdf_link = soup.find('a', {'class': 'download-files-pdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
            
            elif 'mdpi.com' in domain:
                pdf_link = soup.find('a', {'class': 'download-pdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
            
            elif 'nature.com' in domain:
                pdf_link = soup.find('a', {'data-track-action': 'download pdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
                    
            elif 'plos.org' in domain:
                pdf_link = soup.find('a', {'class': 'download-pdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
                    
            elif 'biomedcentral.com' in domain:
                pdf_link = soup.find('a', {'data-track-action': 'download pdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
                    
            elif 'hindawi.com' in domain:
                pdf_link = soup.find('a', {'class': 'pdf-download'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
                    
            elif 'scielo.org' in domain:
                pdf_link = soup.find('a', {'class': 'pdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
                    
            elif 'tandfonline.com' in domain:
                pdf_link = soup.find('a', {'class': 'downloadPdf'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
                    
            elif 'sagepub.com' in domain:
                pdf_link = soup.find('a', {'class': 'pdf-download'})
                if pdf_link:
                    pdf_url = urljoin(page_url, pdf_link['href'])
            
            # Generic PDF link search if no specific match
            if not pdf_url:
                pdf_links = soup.find_all('a', href=lambda x: x and x.endswith('.pdf'))
                if pdf_links:
                    pdf_url = urljoin(page_url, pdf_links[0]['href'])
            
            if pdf_url:
                logger.debug(f"Found PDF URL: {pdf_url}")
            else:
                logger.warning(f"No PDF URL found for {page_url}")
                
            return pdf_url
            
        except Exception as e:
            logger.error(f"Error extracting PDF URL from {page_url}: {str(e)}")
            logger.debug(traceback.format_exc())
            return None

    def get_search_results(self, search_url):
        """Get article URLs from search results"""
        try:
            response = self._make_request(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            domain = urlparse(search_url).netloc
            article_urls = []
            
            # Handle different publishers
            if 'frontiersin.org' in domain:
                articles = soup.find_all('a', {'class': 'article-link'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'mdpi.com' in domain:
                articles = soup.find_all('a', {'class': 'title-link'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'nature.com' in domain:
                articles = soup.find_all('a', {'data-track-action': 'view article'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'plos.org' in domain:
                articles = soup.find_all('a', {'class': 'article-title'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'biomedcentral.com' in domain:
                articles = soup.find_all('a', {'data-test': 'title-link'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'hindawi.com' in domain:
                articles = soup.find_all('a', {'class': 'article-title'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'scielo.org' in domain:
                articles = soup.find_all('a', {'class': 'article-title'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'tandfonline.com' in domain:
                articles = soup.find_all('a', {'class': 'ref'})
                article_urls = [a['href'] for a in articles if a.get('href')]
                
            elif 'sagepub.com' in domain:
                articles = soup.find_all('a', {'class': 'article-link'})
                article_urls = [a['href'] for a in articles if a.get('href')]
            
            article_urls = [urljoin(search_url, url) for url in article_urls]
            logger.debug(f"Found {len(article_urls)} articles on {search_url}")
            return article_urls
            
        except Exception as e:
            logger.error(f"Error getting search results from {search_url}: {str(e)}")
            logger.debug(traceback.format_exc())
            return []

    def get_pdf(self, url, save_path):
        """Download PDF from article URL"""
        try:
            # Get article URLs from search
            article_urls = self.get_search_results(url)
            if not article_urls:
                logger.warning(f"No articles found at {url}")
                return False
            
            # Try each article URL
            for article_url in article_urls[:5]:  # Limit to first 5 results
                try:
                    # Get PDF URL
                    pdf_url = self.get_pdf_url(article_url)
                    if not pdf_url:
                        continue
                    
                    # Download PDF
                    response = self._make_request(pdf_url, stream=True)
                    
                    # Verify content type
                    content_type = response.headers.get('Content-Type', '').lower()
                    if 'pdf' not in content_type and not pdf_url.lower().endswith('.pdf'):
                        logger.warning(f"Response may not be a PDF. Content-Type: {content_type}")
                        continue
                    
                    # Save PDF
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # Verify file size
                    file_size = os.path.getsize(save_path)
                    if file_size == 0:
                        logger.warning("Downloaded file is empty")
                        os.remove(save_path)
                        continue
                    
                    logger.debug(f"Successfully downloaded PDF ({file_size} bytes)")
                    
                    # Random delay
                    time.sleep(random.uniform(1, 3))
                    return True
                    
                except Exception as e:
                    logger.error(f"Error downloading PDF from {article_url}: {str(e)}")
                    logger.debug(traceback.format_exc())
                    if os.path.exists(save_path):
                        os.remove(save_path)
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"Error in get_pdf for {url}: {str(e)}")
            logger.debug(traceback.format_exc())
            if os.path.exists(save_path):
                os.remove(save_path)
            return False

def download_paper(paper_info, save_path):
    """Helper function to create scraper and download paper"""
    scraper = PaperScraper()
    return scraper.get_pdf(paper_info, save_path)

if __name__ == "__main__":
    # Example usage
    paper_info = {
        'title': 'Example paper title',
        'doi': '10.1234/example.doi',
        'url': 'https://example.com/paper',
        'authors': ['Author 1', 'Author 2'],
        'abstract': 'Example abstract',
        'journal': 'Example Journal'
    }
    
    success = download_paper(paper_info, 'example_paper.pdf')
    print(f"Download {'successful' if success else 'failed'}") 