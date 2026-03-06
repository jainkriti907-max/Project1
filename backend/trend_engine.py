"""
Mosaic Trends Radar — Trend Analysis Engine
Orchestrates data collection and scoring pipeline.
"""
import logging
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

from data_ingestion.google_trends import fetch_trends_data
from data_ingestion.reddit_signals import fetch_reddit_signals
from data_ingestion.pubmed_signals import fetch_pubmed_signals
from analysis.scorer import score_trend, COMPETITION_SCORES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_TRENDS = [
    'Shilajit',
    "Lion's Mane Mushroom",
    'Magnesium Glycinate',
    'Berberine',
    'Cycle Syncing',
    'Collagen Peptides',
    'Cold Plunge Therapy',
    'NAD+ Longevity',
    'Beef Liver Supplements',
    'Ashwagandha',
    'Creatine for Women',
    'Red Light Therapy',
]

KEYWORD_TO_TREND = {
    'shilajit': 'Shilajit',
    "lion's mane": "Lion's Mane Mushroom",
    "lion's mane mushroom": "Lion's Mane Mushroom",
    'magnesium glycinate': 'Magnesium Glycinate',
    'berberine': 'Berberine',
    'cycle syncing': 'Cycle Syncing',
    'collagen': 'Collagen Peptides',
    'collagen peptides': 'Collagen Peptides',
    'cold plunge': 'Cold Plunge Therapy',
    'nad+': 'NAD+ Longevity',
    'beef liver': 'Beef Liver Supplements',
    'ashwagandha': 'Ashwagandha',
    'creatine women': 'Creatine for Women',
    'red light': 'Red Light Therapy',
}


def run_pipeline() -> List[Dict]:
    """
    Main trend analysis pipeline.
    Runs all data sources concurrently, aggregates signals, and scores trends.
    """
    logger.info("🚀 Starting Mosaic Trends Radar pipeline...")
    
    # Run data sources concurrently with timeout
    google_data, reddit_data, pubmed_data = {}, {}, {}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(fetch_trends_data): 'google',
            executor.submit(fetch_reddit_signals): 'reddit',
            executor.submit(fetch_pubmed_signals): 'pubmed',
        }
        for future in as_completed(futures, timeout=30):
            source = futures[future]
            try:
                result = future.result()
                if source == 'google':
                    for item in result:
                        kw = item['keyword'].lower()
                        trend = KEYWORD_TO_TREND.get(kw) or _fuzzy_match(kw)
                        if trend:
                            google_data[trend] = item['velocity_score']
                elif source == 'reddit':
                    for item in result:
                        kw = item['keyword'].lower()
                        trend = KEYWORD_TO_TREND.get(kw) or _fuzzy_match(kw)
                        if trend:
                            reddit_data[trend] = item['buzz_score']
                elif source == 'pubmed':
                    for item in result:
                        pubmed_data[item['trend_name']] = item['science_score']
                logger.info(f"✅ {source.capitalize()} data fetched: {len(result)} items")
            except (TimeoutError, Exception) as e:
                logger.warning(f"⚠️ {source} data source failed: {e}")
    
    # Score all target trends
    scored_trends = []
    for trend_name in TARGET_TRENDS:
        velocity = google_data.get(trend_name, _default_velocity(trend_name))
        buzz = reddit_data.get(trend_name, _default_buzz(trend_name))
        science = pubmed_data.get(trend_name, _default_science(trend_name))
        competition = COMPETITION_SCORES.get(trend_name, 50)
        
        scored = score_trend(trend_name, velocity, buzz, science, competition)
        scored_trends.append(scored)
        logger.info(f"📊 {trend_name}: score={scored['score']}, class={scored['classification']}")
    
    # Sort by score descending, return top 10
    scored_trends.sort(key=lambda x: x['score'], reverse=True)
    return scored_trends[:10]


def _fuzzy_match(keyword: str) -> str:
    """Attempt fuzzy keyword to trend mapping."""
    for kw, trend in KEYWORD_TO_TREND.items():
        if kw in keyword or keyword in kw:
            return trend
    return None


def _default_velocity(trend_name: str) -> int:
    defaults = {
        'Shilajit': 88, "Lion's Mane Mushroom": 82, 'Magnesium Glycinate': 80,
        'Berberine': 76, 'Cycle Syncing': 74, 'Collagen Peptides': 70,
        'Cold Plunge Therapy': 66, 'NAD+ Longevity': 63, 'Beef Liver Supplements': 59,
        'Ashwagandha': 72, 'Creatine for Women': 68, 'Red Light Therapy': 65,
    }
    return defaults.get(trend_name, 55)


def _default_buzz(trend_name: str) -> int:
    defaults = {
        'Shilajit': 84, "Lion's Mane Mushroom": 80, 'Magnesium Glycinate': 77,
        'Berberine': 74, 'Cycle Syncing': 70, 'Collagen Peptides': 67,
        'Cold Plunge Therapy': 72, 'NAD+ Longevity': 62, 'Beef Liver Supplements': 57,
        'Ashwagandha': 76, 'Creatine for Women': 68, 'Red Light Therapy': 65,
    }
    return defaults.get(trend_name, 50)


def _default_science(trend_name: str) -> int:
    defaults = {
        'Ashwagandha': 90, 'Magnesium Glycinate': 86, 'Collagen Peptides': 82,
        'Berberine': 84, 'NAD+ Longevity': 80, "Lion's Mane Mushroom": 74,
        'Cold Plunge Therapy': 70, 'Creatine for Women': 77, 'Shilajit': 64,
        'Red Light Therapy': 67, 'Beef Liver Supplements': 60, 'Cycle Syncing': 57,
    }
    return defaults.get(trend_name, 52)


if __name__ == '__main__':
    trends = run_pipeline()
    print(f"\n🌿 Mosaic Trends Radar — {len(trends)} Opportunities Found\n")
    for t in trends:
        print(f"  [{t['score']:3d}] {t['classification']:12s} | {t['name']}")
