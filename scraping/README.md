# Academic Paper Scraper

A robust Python scraper designed to download academic papers from various publishers and repositories. This tool supports multiple academic publishers and includes fallback mechanisms to ensure successful paper retrieval.

## Features

- Supports multiple academic publishers:
  - PLOS ONE
  - MDPI
  - Frontiers
  - BioMed Central
  - Nature
  - PubMed Central
  - And more through generic patterns
- Smart PDF detection and download
- Automatic retry mechanism with exponential backoff
- Comprehensive logging
- Multiple download strategies:
  - Direct PDF download
  - Meta tag extraction
  - Alternative URL patterns
  - DOI-based retrieval
- Search results parsing from:
  - Google Scholar
  - PubMed
  - Generic academic search pages

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dagon67/scraping.git
cd scraping
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from scraper import PaperScraper, download_paper

# Example 1: Download a paper directly
paper_info = {
    'url': 'https://journal.com/article/12345'
}
success = download_paper(paper_info, 'paper.pdf')

# Example 2: Using the scraper class
scraper = PaperScraper()

# Get search results
results = scraper.get_search_results('https://scholar.google.com/scholar?q=machine+learning')

# Download first result
if results:
    scraper.get_pdf(results[0]['url'], 'paper.pdf')
```

## Project Structure

```
scraping/
├── scraper.py        # Main scraper implementation
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Features in Detail

### Publisher Support
The scraper includes specialized handlers for major academic publishers and falls back to generic patterns for others. It can extract PDFs from:
- Journal websites
- Digital libraries
- Academic repositories
- Pre-print servers

### Download Strategies
1. Direct PDF Detection
   - Checks URL patterns
   - Verifies content types
   - Handles redirects

2. Smart Extraction
   - Parses meta tags
   - Analyzes page structure
   - Follows download links

3. Fallback Mechanisms
   - Alternative URL patterns
   - DOI-based retrieval
   - Multiple mirror attempts

## Error Handling

- Automatic retry on failure
- Exponential backoff
- Comprehensive logging
- Exception tracking
- Connection timeout handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/Dagon67/scraping](https://github.com/Dagon67/scraping) 