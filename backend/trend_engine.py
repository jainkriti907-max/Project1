import logging
from typing import List, Dict
from analysis.scorer import score_trend, COMPETITION_SCORES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_TRENDS = [
    'Shilajit', "Lion's Mane Mushroom", 'Magnesium Glycinate',
    'Berberine', 'Cycle Syncing', 'Collagen Peptides',
    'Cold Plunge Therapy', 'NAD+ Longevity', 'Beef Liver Supplements',
    'Ashwagandha', 'Creatine for Women', 'Red Light Therapy',
]

VELOCITY_DATA = {
    'Shilajit': 92, "Lion's Mane Mushroom": 85, 'Magnesium Glycinate': 83,
    'Berberine': 78, 'Cycle Syncing': 76, 'Collagen Peptides': 72,
    'Cold Plunge Therapy': 68, 'NAD+ Longevity': 65, 'Beef Liver Supplements': 61,
    'Ashwagandha': 74, 'Creatine for Women': 70, 'Red Light Therapy': 67,
}

BUZZ_DATA = {
    'Shilajit': 88, "Lion's Mane Mushroom": 82, 'Magnesium Glycinate': 79,
    'Berberine': 76, 'Cycle Syncing': 72, 'Collagen Peptides': 69,
    'Cold Plunge Therapy': 74, 'NAD+ Longevity': 64, 'Beef Liver Supplements': 59,
    'Ashwagandha': 78, 'Creatine for Women': 71, 'Red Light Therapy': 67,
}

SCIENCE_DATA = {
    'Ashwagandha': 90, 'Magnesium Glycinate': 86, 'Collagen Peptides': 82,
    'Berberine': 84, 'NAD+ Longevity': 80, "Lion's Mane Mushroom": 74,
    'Cold Plunge Therapy': 70, 'Creatine for Women': 77, 'Shilajit': 64,
    'Red Light Therapy': 67, 'Beef Liver Supplements': 60, 'Cycle Syncing': 57,
}

def run_pipeline() -> List[Dict]:
    logger.info("Starting Mosaic Trends Radar pipeline...")
    live_velocity = _try_google_trends()
    live_buzz = _try_reddit()
    live_science = _try_pubmed()

    scored_trends = []
    for trend_name in TARGET_TRENDS:
        velocity = live_velocity.get(trend_name, VELOCITY_DATA.get(trend_name, 60))
        buzz = live_buzz.get(trend_name, BUZZ_DATA.get(trend_name, 55))
        science = live_science.get(trend_name, SCIENCE_DATA.get(trend_name, 55))
        competition = COMPETITION_SCORES.get(trend_name, 50)
        scored = score_trend(trend_name, velocity, buzz, science, competition)
        scored_trends.append(scored)
        logger.info(f"{trend_name}: score={scored['score']}")

    scored_trends.sort(key=lambda x: x['score'], reverse=True)
    return scored_trends[:10]

def _try_google_trends() -> Dict:
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=330, timeout=(5, 10))
        batch = ['ashwagandha supplement', 'shilajit benefits',
                 "lion's mane mushroom", 'magnesium glycinate', 'berberine']
        pytrends.build_payload(batch, timeframe='today 3-m', geo='IN')
        interest = pytrends.interest_over_time()
        if interest.empty:
            return {}
        mapping = {
            'ashwagandha supplement': 'Ashwagandha',
            'shilajit benefits': 'Shilajit',
            "lion's mane mushroom": "Lion's Mane Mushroom",
            'magnesium glycinate': 'Magnesium Glycinate',
            'berberine': 'Berberine',
        }
        results = {}
        for kw, trend in mapping.items():
            if kw in interest.columns:
                vals = interest[kw].values
                if len(vals) >= 4:
                    results[trend] = min(100, int((vals[-4:].mean() / (vals[:4].mean() + 1)) * 50))
        return results
    except Exception as e:
        logger.warning(f"Google Trends unavailable: {e}")
        return {}

def _try_reddit() -> Dict:
    try:
        import requests
        headers = {'User-Agent': 'MosaicTrendsRadar/1.0'}
        res = requests.get('https://www.reddit.com/r/Supplements/hot.json?limit=25',
                           headers=headers, timeout=8)
        if res.status_code != 200:
            return {}
        posts = res.json().get('data', {}).get('children', [])
        keyword_map = {
            'shilajit': 'Shilajit', "lion's mane": "Lion's Mane Mushroom",
            'magnesium': 'Magnesium Glycinate', 'berberine': 'Berberine',
            'ashwagandha': 'Ashwagandha', 'collagen': 'Collagen Peptides',
            'creatine': 'Creatine for Women', 'nad': 'NAD+ Longevity',
        }
        scores = {}
        for post in posts:
            text = (post['data'].get('title', '') + ' ' + post['data'].get('selftext', '')).lower()
            ups = post['data'].get('ups', 0)
            for kw, trend in keyword_map.items():
                if kw in text:
                    scores[trend] = min(100, scores.get(trend, 50) + 10 + min(ups // 50, 30))
        return scores
    except Exception as e:
        logger.warning(f"Reddit unavailable: {e}")
        return {}

def _try_pubmed() -> Dict:
    try:
        import requests
        queries = {
            'Ashwagandha': 'ashwagandha withania somnifera',
            'Berberine': 'berberine glucose metabolism',
            'Magnesium Glycinate': 'magnesium glycinate sleep',
        }
        results = {}
        for trend, query in queries.items():
            res = requests.get(
                'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
                params={'db': 'pubmed', 'term': query, 'retmode': 'json',
                        'mindate': '2022', 'maxdate': '2025', 'retmax': 0},
                timeout=8)
            if res.status_code == 200:
                count = int(res.json().get('esearchresult', {}).get('count', 0))
                results[trend] = min(100, 50 + min(count // 5, 50))
        return results
    except Exception as e:
        logger.warning(f"PubMed unavailable: {e}")
        return {}
