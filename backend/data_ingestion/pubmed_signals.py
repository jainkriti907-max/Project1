"""
PubMed research signal ingestion.
Uses NCBI E-utilities API (free, no auth required).
"""
import logging
import requests
from typing import Dict, List

logger = logging.getLogger(__name__)

RESEARCH_QUERIES = {
    'Shilajit': 'shilajit fulvic acid therapeutic',
    "Lion's Mane Mushroom": 'hericium erinaceus neuroprotective cognitive',
    'Magnesium Glycinate': 'magnesium glycinate sleep anxiety supplementation',
    'Berberine': 'berberine glucose metabolism weight management',
    'Cycle Syncing': 'menstrual cycle exercise performance hormones',
    'Collagen Peptides': 'collagen peptide supplementation skin joint',
    'Cold Plunge Therapy': 'cold water immersion recovery inflammation',
    'NAD+ Longevity': 'NAD+ nicotinamide riboside longevity aging',
    'Beef Liver Supplements': 'organ meat liver nutrient density bioavailability',
    'Ashwagandha': 'ashwagandha withania somnifera adaptogen stress',
    'Creatine for Women': 'creatine supplementation women muscle cognition',
    'Red Light Therapy': 'photobiomodulation red light therapy clinical',
}

NCBI_BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

def fetch_pubmed_signals() -> List[Dict]:
    """
    Fetch research publication counts from PubMed for wellness trends.
    Returns scientific backing scores.
    """
    results = []
    
    for trend_name, query in RESEARCH_QUERIES.items():
        try:
            # Search PubMed
            search_url = f'{NCBI_BASE}/esearch.fcgi'
            params = {
                'db': 'pubmed',
                'term': query,
                'retmode': 'json',
                'datetype': 'pdat',
                'mindate': '2022',
                'maxdate': '2025',
                'retmax': 0,
            }
            res = requests.get(search_url, params=params, timeout=8)
            if res.status_code == 200:
                data = res.json()
                count = int(data.get('esearchresult', {}).get('count', 0))
                science_score = min(100, int(50 + (count / 10) * 5))
                results.append({
                    'trend_name': trend_name,
                    'paper_count': count,
                    'science_score': max(science_score, _baseline_science(trend_name)),
                })
            else:
                results.append({'trend_name': trend_name, 'paper_count': 0, 'science_score': _baseline_science(trend_name)})
        except Exception as e:
            logger.warning(f"PubMed error for {trend_name}: {e}")
            results.append({'trend_name': trend_name, 'paper_count': 0, 'science_score': _baseline_science(trend_name)})
    
    return results


def _baseline_science(trend_name: str) -> int:
    """Evidence-calibrated baseline science scores."""
    scores = {
        'Ashwagandha': 88, 'Magnesium Glycinate': 85, 'Collagen Peptides': 80,
        'NAD+ Longevity': 78, 'Berberine': 82, "Lion's Mane Mushroom": 72,
        'Cold Plunge Therapy': 68, 'Creatine for Women': 75, 'Red Light Therapy': 65,
        'Shilajit': 62, 'Beef Liver Supplements': 58, 'Cycle Syncing': 55,
    }
    return scores.get(trend_name, 50)
