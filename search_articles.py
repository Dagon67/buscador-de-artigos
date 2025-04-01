import requests
import json
import os
from datetime import datetime

def search_articles(query, max_results=10):
    url = f"http://localhost:8000/latest"
    params = {
        "query": query,
        "max_results": max_results
    }
    
    response = requests.get(url, params=params)
    return response.json()

def save_articles(articles, category):
    # Create directory if it doesn't exist
    os.makedirs("artiguinhos", exist_ok=True)
    
    # Create a file for this category
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"artiguinhos/{category}_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    return filename

# Categories and their search queries
categories = {
    "giftedness": "superintelligence gifted brain extreme cognition divergent thinking high IQ creativity prodigy neurodiversity",
    "learning_approaches": "differentiated learning accelerated learning multimodal instruction personalized strategies adaptive learning",
    "historical_figures": "historical polymaths visionary innovators nonconventional geniuses eccentric prodigies legacy of genius",
    "brain_topology": "neural connectivity cerebral lateralization brain morphology white matter integrity functional mapping",
    "intelligence_types": "multiple intelligences spatial musical mathematical linguistic kinesthetic intrapersonal interpersonal",
    "learning_methods": "intelligence-tailored pedagogy multimodal curriculum sensory-based gamification spatial musical mnemonics",
    "interdisciplinary": "neuroscience pedagogy cognitive psychology gifted educational neuroscience neuroeducation theories",
    "technology": "AI tutoring gifted machine learning education data mining cognition neuroinformatics VR learning",
    "cultural": "cultural giftedness social construct intelligence evolution of genius societal prodigies educational equity",
    "metacognition": "metacognitive strategies self-regulated learning creativity dynamics cognitive load management"
}

# Search and save articles for each category
results = {}
for category, query in categories.items():
    print(f"Searching for {category}...")
    articles = search_articles(query)
    filename = save_articles(articles, category)
    print(f"Saved to {filename}")
    results[category] = articles

# Print summary
print("\nSearch completed! Summary of findings:")
for category, articles in results.items():
    total_articles = sum(len(response["results"]) for response in articles)
    print(f"\n{category.replace('_', ' ').title()}:")
    print(f"Total articles found: {total_articles}")
    
    # Print some article titles as examples
    for response in articles:
        if response["results"]:
            print(f"\nFrom {response['source']}:")
            for article in response["results"][:3]:  # Show up to 3 articles per source
                print(f"- {article['title']}") 