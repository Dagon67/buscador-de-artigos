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
        self.logger = logger
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
                self.logger.debug(f"Request attempt {attempt + 1}/{self.max_retries} for {url}")
                response = self.session.get(url, stream=stream, timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (attempt + 1)
                    self.logger.info(f"Waiting {delay} seconds before retry...")
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
        """Try alternative URLs for PDF download."""
        alternative_urls = []
        
        # Try DOI-based alternatives if DOI is available
        if doi:
            self.logger.info(f"Trying alternative URLs using DOI: {doi}")
            # Try Sci-Hub
            scihub_urls = [
                f"https://sci-hub.se/{doi}",
                f"https://sci-hub.st/{doi}",
                f"https://sci-hub.ru/{doi}"
            ]
            alternative_urls.extend(scihub_urls)
        
        # Try URL-based alternatives
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        
        # Common PDF URL patterns
        pdf_patterns = [
            '/pdf',
            '/download',
            '/fulltext.pdf',
            '/download/pdf',
            '/article/pdf'
        ]
        
        for pattern in pdf_patterns:
            new_url = f"{parsed_url.scheme}://{parsed_url.netloc}{pattern}"
            alternative_urls.append(new_url)
        
        return alternative_urls

    def get_pdf_url(self, page_url):
        """Get PDF download URL from article page."""
        try:
            self.logger.info(f"Fetching article page: {page_url}")
            response = self._make_request(page_url)
            html_content = response.text
            
            # Extract DOI if present
            soup = BeautifulSoup(html_content, 'html.parser')
            doi = None
            doi_meta = soup.find('meta', attrs={'name': 'citation_doi'})
            if doi_meta:
                doi = doi_meta.get('content')
            
            # Try to find PDF URL in page
            pdf_urls = self._extract_pdf_urls(html_content, page_url)
            
            if pdf_urls:
                self.logger.info(f"Found PDF URL: {pdf_urls[0]}")
                return pdf_urls[0]
            
            # Try alternative URLs
            alternative_urls = self._try_alternative_urls(page_url, doi)
            for alt_url in alternative_urls:
                try:
                    self.logger.info(f"Trying alternative URL: {alt_url}")
                    response = self._make_request(alt_url)
                    if 'pdf' in response.headers.get('content-type', '').lower():
                        self.logger.info(f"Found PDF at alternative URL: {alt_url}")
                        return alt_url
                except:
                    continue
            
            self.logger.warning("No PDF URL found")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting PDF URL: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None

    def get_search_results(self, search_url):
        """Get search results from a search page."""
        try:
            self.logger.info(f"Fetching search results from: {search_url}")
            response = self._make_request(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # Handle different search result formats
            # Google Scholar
            if 'scholar.google.com' in search_url:
                articles = soup.find_all('div', class_='gs_r')
                for article in articles:
                    title_elem = article.find('h3', class_='gs_rt')
                    if title_elem and title_elem.a:
                        title = title_elem.a.text
                        url = title_elem.a['href']
                        results.append({'title': title, 'url': url})
            
            # PubMed
            elif 'pubmed.ncbi.nlm.nih.gov' in search_url:
                articles = soup.find_all('article', class_='full-docsum')
                for article in articles:
                    title_elem = article.find('a', class_='docsum-title')
                    if title_elem:
                        title = title_elem.text.strip()
                        url = 'https://pubmed.ncbi.nlm.nih.gov' + title_elem['href']
                        results.append({'title': title, 'url': url})
            
            # Generic handler
            else:
                # Look for common article patterns
                articles = soup.find_all(['article', 'div'], class_=['article', 'result'])
                for article in articles:
                    title_elem = article.find(['h2', 'h3', 'h4'])
                    if title_elem and title_elem.a:
                        title = title_elem.a.text.strip()
                        url = urljoin(search_url, title_elem.a['href'])
                        results.append({'title': title, 'url': url})
            
            self.logger.info(f"Found {len(results)} search results")
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting search results: {str(e)}")
            self.logger.error(traceback.format_exc())
            return []

    def get_pdf(self, url, save_path):
        """Download PDF from article URL."""
        try:
            self.logger.info(f"Attempting to get PDF from: {url}")
            
            # First try direct download if URL appears to be PDF
            if self._is_potential_pdf_url(url):
                self.logger.info("URL appears to be direct PDF link")
                if self._try_direct_download(url, save_path):
                    return True
            
            # If direct download fails or URL is not PDF, try to find PDF URL
            pdf_url = self.get_pdf_url(url)
            if not pdf_url:
                self.logger.warning("Could not find PDF URL")
                return False
            
            # Try to download using found PDF URL
            if self._try_direct_download(pdf_url, save_path):
                return True
            
            self.logger.warning("All download attempts failed")
            return False
            
        except Exception as e:
            self.logger.error(f"Error downloading PDF: {str(e)}")
            self.logger.error(traceback.format_exc())
            return False

def download_paper(paper_info, save_path):
    """Download a paper given its information."""
    try:
        # Create scraper instance
        scraper = PaperScraper()
        
        # Extract URL from paper info
        url = paper_info.get('url')
        if not url:
            logger.error("No URL provided in paper info")
            return False
        
        # Create save directory if it doesn't exist
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Download PDF
        success = scraper.get_pdf(url, save_path)
        
        if success:
            logger.info(f"Successfully downloaded paper to: {save_path}")
        else:
            logger.error("Failed to download paper")
        
        return success
        
    except Exception as e:
        logger.error(f"Error in download_paper: {str(e)}")
        logger.error(traceback.format_exc())
        return False 