"""
Trend scoring and classification engine.
Aggregates multi-source signals into opportunity scores.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Market size estimates for Indian wellness market (USD)
MARKET_ESTIMATES = {
    'Shilajit': '$180M by 2027',
    "Lion's Mane Mushroom": '$340M by 2028',
    'Magnesium Glycinate': '$290M by 2027',
    'Berberine': '$420M by 2028',
    'Cycle Syncing': '$150M by 2027',
    'Collagen Peptides': '$650M by 2028',
    'Cold Plunge Therapy': '$200M by 2027',
    'NAD+ Longevity': '$520M by 2030',
    'Beef Liver Supplements': '$95M by 2027',
    'Ashwagandha': '$780M by 2028',
    'Creatine for Women': '$310M by 2027',
    'Red Light Therapy': '$280M by 2028',
}

PRODUCT_CONCEPTS = {
    'Shilajit': 'Shilajit + Ashwagandha men\'s vitality stack',
    "Lion's Mane Mushroom": 'Lion\'s Mane nootropic coffee blend',
    'Magnesium Glycinate': 'Evening magnesium + L-theanine sleep formula',
    'Berberine': 'Berberine + chromium metabolic support capsules',
    'Cycle Syncing': 'Phase-specific women\'s supplement kit (4-pack)',
    'Collagen Peptides': 'Marine collagen + vitamin C beauty drink powder',
    'Cold Plunge Therapy': 'Cold recovery mineral bath salts + guide',
    'NAD+ Longevity': 'NMN + resveratrol longevity daily capsule',
    'Beef Liver Supplements': 'Grass-fed beef liver organ meat capsules',
    'Ashwagandha': 'KSM-66 ashwagandha stress + sleep gummy',
    'Creatine for Women': 'Micronised creatine + collagen women\'s blend',
    'Red Light Therapy': 'Portable red light therapy panel + protocol book',
}

PACKAGING_FORMATS = {
    'Shilajit': 'Resin jar + dropper (40g)',
    "Lion's Mane Mushroom": 'Mushroom powder sachets (30-day supply)',
    'Magnesium Glycinate': 'Glass bottle capsules (60ct) + QR sleep guide',
    'Berberine': 'Eco-pack capsules with 90-day supply',
    'Cycle Syncing': 'Monthly subscription kit (4 labelled pouches)',
    'Collagen Peptides': 'Kraft paper stick packs in box (30ct)',
    'Cold Plunge Therapy': 'Premium tin canister + printed protocol card',
    'NAD+ Longevity': 'Dark glass bottle, minimalist luxury packaging',
    'Beef Liver Supplements': 'Matte pouch, nose-to-tail branding (180 caps)',
    'Ashwagandha': 'Kraft gummy pouch with resealable zip (60 gummies)',
    'Creatine for Women': 'Pastel canister (250g), scoop included',
    'Red Light Therapy': 'Retail box with USB device + instruction booklet',
}

LAUNCH_TIMING = {
    'Shilajit': 'Q3 2025 — peak pre-monsoon demand',
    "Lion's Mane Mushroom": 'Q4 2025 — back-to-work nootropic season',
    'Magnesium Glycinate': 'Q1 2025 — New Year wellness spike',
    'Berberine': 'Q2 2025 — summer metabolic trend',
    'Cycle Syncing': 'Q2 2025 — women\'s health awareness month',
    'Collagen Peptides': 'Q1 2025 — wedding season prep',
    'Cold Plunge Therapy': 'Q4 2025 — winter recovery trend',
    'NAD+ Longevity': 'Q3 2026 — emerging longevity wave',
    'Beef Liver Supplements': 'Q2 2025 — carnivore diet crossover',
    'Ashwagandha': 'Q3 2025 — exam stress + festive season',
    'Creatine for Women': 'Q1 2025 — new year fitness resolution',
    'Red Light Therapy': 'Q4 2025 — winter skin care season',
}

OPPORTUNITY_BRIEFS = {
    'Shilajit': 'Shilajit is experiencing a breakout moment in India driven by growing male wellness awareness and Ayurvedic ingredient revival. YouTube search volume has tripled YoY. The market lacks premium, clean-label formats — an opportunity for Mosaic to own the "modern Ayurveda" positioning with a resin + capsule combo targeting men 28–45.',
    "Lion's Mane Mushroom": 'Functional mushrooms are moving from fringe to mainstream. Lion\'s Mane is the cognitive performance ingredient of 2025, driven by TikTok wellness creators and remote-work brain fog discourse. A ready-to-mix nootropic coffee blend would capture the ₹500–900 per unit premium segment.',
    'Magnesium Glycinate': 'Sleep anxiety is the #1 wellness concern for Indian urban millennials. Magnesium glycinate is the breakout mineral of 2024-25, with Reddit and YouTube driving massive awareness. The Indian market currently offers low-quality oxide formulations — a premium glycinate evening formula with L-theanine is a clear whitespace.',
    'Berberine': 'Called "nature\'s Ozempic" online, berberine is seeing explosive search growth among consumers seeking metabolic health alternatives. Backed by 1,000+ clinical studies. High opportunity for a clean-label berberine + chromium metabolic formula targeting PCOS and pre-diabetic consumers.',
    'Cycle Syncing': 'Cycle syncing is the fastest growing women\'s wellness concept on Instagram and YouTube India. Dr. Aviva Romm and Alisa Vitti content is being remixed into Hindi. A 4-phase supplement kit personalised to menstrual cycle phases would be a category-creating product with no Indian competitors.',
    'Collagen Peptides': 'The India beauty-from-within market is accelerating. Marine collagen peptides are now the #1 growth supplement in the beauty vertical. The gap is in premium, transparent formulations (source-declared, tested). A beautifying collagen drink powder in stick-pack format targets the ₹2,000–4,000 beauty consumer.',
    'Cold Plunge Therapy': 'Cold therapy is moving from elite athletes to mainstream wellness adopters. Post-COVID recovery culture and the Andrew Huberman effect are driving the wave. While home plunges are expensive, an accessible Epsom + mineral bath salt cold recovery kit is a low-capex entry with strong repeat purchase potential.',
    'NAD+ Longevity': 'The longevity supplement category is 3–5 years from Indian mainstream but early adopters are actively purchasing from US brands at premium prices. An NMN/NR product with educational positioning could capture the longevity early adopter segment now while building brand authority.',
    'Beef Liver Supplements': 'The ancestral nutrition / carnivore wellness movement is creating genuine demand for clean beef organ supplements. Currently only US brands (Ancestral Supplements) serve this Indian demand. A grass-fed, India-sourced liver capsule would be differentiated and defensible.',
    'Ashwagandha': 'Despite being a mature trend, ashwagandha is entering a second growth phase as global clinical validation increases. The gap is in premium gummy formats — the current market is dominated by bulk capsules. A KSM-66 standardised ashwagandha gummy with sleep positioning captures a new consumption occasion.',
    'Creatine for Women': 'The narrative around creatine has shifted — women creators on Instagram are now driving creatine adoption for strength, cognition, and skin. No Indian brand owns this positioning. A women-first creatine + collagen blend in aesthetically designed packaging could own the category.',
    'Red Light Therapy': 'Red light therapy (photobiomodulation) is one of the fastest-growing biohacking categories globally. Indian consumer awareness is 18–24 months behind the US, creating a perfect early mover window. An affordable portable panel with a Mosaic-branded protocol guide could establish category leadership.',
}

COMPETITION_SCORES = {
    'Shilajit': 55, "Lion's Mane Mushroom": 35, 'Magnesium Glycinate': 65,
    'Berberine': 30, 'Cycle Syncing': 15, 'Collagen Peptides': 72,
    'Cold Plunge Therapy': 28, 'NAD+ Longevity': 20, 'Beef Liver Supplements': 18,
    'Ashwagandha': 80, 'Creatine for Women': 40, 'Red Light Therapy': 25,
}

def score_trend(
    trend_name: str,
    velocity: int,
    buzz: int,
    science: int,
    competition: int,
) -> Dict:
    """
    Compute composite opportunity score and classification.
    
    Score formula:
    - Velocity (Google Trends momentum): 30%
    - Consumer buzz (Reddit/YouTube): 25%
    - Market potential (estimated size): 20%
    - Scientific backing (PubMed): 15%
    - Competition opportunity (inverse competition): 10%
    """
    market_score = _market_score(trend_name)
    competition_opportunity = 100 - competition  # low competition = high opportunity
    
    composite = int(
        velocity * 0.30 +
        buzz * 0.25 +
        market_score * 0.20 +
        science * 0.15 +
        competition_opportunity * 0.10
    )
    
    composite = max(0, min(100, composite))
    
    if composite >= 70:
        classification = 'Strong Trend'
    elif composite >= 50:
        classification = 'Early Trend'
    else:
        classification = 'Fad'
    
    return {
        'name': trend_name,
        'score': composite,
        'classification': classification,
        'marketOpportunity': MARKET_ESTIMATES.get(trend_name, '$100M+ by 2027'),
        'productConcept': PRODUCT_CONCEPTS.get(trend_name, f'{trend_name} supplement formula'),
        'packagingFormat': PACKAGING_FORMATS.get(trend_name, 'Premium capsule bottle (60ct)'),
        'launchTiming': LAUNCH_TIMING.get(trend_name, 'Q2 2025'),
        'opportunityBrief': OPPORTUNITY_BRIEFS.get(trend_name, f'{trend_name} is an emerging wellness opportunity with strong consumer momentum.'),
        'signals': {
            'velocity': velocity,
            'marketPotential': market_score,
            'scientificBacking': science,
            'consumerBuzz': buzz,
            'competition': competition,
        }
    }


def _market_score(trend_name: str) -> int:
    """Convert market estimate string to numeric score."""
    scores = {
        'Ashwagandha': 92, 'Collagen Peptides': 88, 'NAD+ Longevity': 82,
        'Berberine': 80, "Lion's Mane Mushroom": 75, 'Creatine for Women': 73,
        'Magnesium Glycinate': 70, 'Red Light Therapy': 68, 'Shilajit': 65,
        'Cold Plunge Therapy': 60, 'Cycle Syncing': 58, 'Beef Liver Supplements': 50,
    }
    return scores.get(trend_name, 55)
