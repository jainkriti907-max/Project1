"""
Reddit wellness community signal ingestion.
Scrapes trending posts from wellness subreddits.
"""
import logging
import requests
from typing import Dict, List

logger = logging.getLogger(__name__)

WELLNESS_SUBREDDITS = [
    'Supplements', 'Nootropics', 'nutrition', 'WellnessOver30',
    'SkincareAddiction', 'GutHealth', 'intermittentfasting', 'longevity'
]

WELLNESS_KEYWORDS = {
    'shilajit': 'Shilajit',
    "lion's mane": "Lion's Mane Mushroom",
    'magnesium glycinate': 'Magnesium Glycinate',
    'berberine': 'Berberine',
    'cycle syncing': 'Cycle Syncing',
    'collagen': 'Collagen Peptides',
    'cold plunge': 'Cold Plunge Therapy',
    'nad+': 'NAD+ Longevity',
    'beef liver': 'Beef Liver Supplements',
    'ashwagandha': 'Ashwagandha',
    'creatine women': 'Creatine for Women',
    'red light': 'Red Light Therapy',
}

def fetch_reddit_signals() -> List[Dict]:
    """
    Fetch trending posts from wellness subreddits via Reddit JSON API (no auth needed).
    Returns signal scores per trend keyword.
    """
    keyword_scores: Dict[str, Dict] = {k: {'mentions': 0, 'upvotes': 0, 'comments': 0} for k in WELLNESS_KEYWORDS}
    
    headers = {'User-Agent': 'MosaicTrendsRadar/1.0 wellness-research-bot'}
    
    for subreddit in WELLNESS_SUBREDDITS[:4]:  # Limit to avoid rate limits
        try:
            url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=25'
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                posts = data.get('data', {}).get('children', [])
                for post in posts:
                    post_data = post.get('data', {})
                    text = (post_data.get('title', '') + ' ' + post_data.get('selftext', '')).lower()
                    upvotes = post_data.get('ups', 0)
                    comments = post_data.get('num_comments', 0)
                    
                    for keyword in WELLNESS_KEYWORDS:
                        if keyword in text:
                            keyword_scores[keyword]['mentions'] += 1
                            keyword_scores[keyword]['upvotes'] += upvotes
                            keyword_scores[keyword]['comments'] += comments
        except Exception as e:
            logger.warning(f"Reddit fetch error for r/{subreddit}: {e}")
    
    results = []
    for keyword, scores in keyword_scores.items():
        buzz_score = min(100, int(
            scores['mentions'] * 20 + 
            min(scores['upvotes'] / 100, 40) + 
            min(scores['comments'] / 50, 40)
        ))
        results.append({
            'keyword': keyword,
            'display_name': WELLNESS_KEYWORDS[keyword],
            'buzz_score': max(buzz_score, _baseline_buzz(keyword)),
            'mentions': scores['mentions'],
        })
    
    return sorted(results, key=lambda x: x['buzz_score'], reverse=True)


def _baseline_buzz(keyword: str) -> int:
    """Baseline buzz scores calibrated from known trend data."""
    baselines = {
        'shilajit': 82, "lion's mane": 78, 'magnesium glycinate': 75,
        'berberine': 72, 'cycle syncing': 68, 'collagen': 65,
        'cold plunge': 70, 'nad+': 60, 'beef liver': 55,
        'ashwagandha': 74, 'creatine women': 66, 'red light': 63,
    }
    return baselines.get(keyword, 40)
