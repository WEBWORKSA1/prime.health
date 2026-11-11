"""Field and source helpers shared by tool definitions."""


def F(id, type, label, **kw):
    d = {"id": id, "type": type, "label": label}
    d.update(kw)
    return d


def pm(q):
    """PubMed search link (stable even if an article ID changes)."""
    return "https://pubmed.ncbi.nlm.nih.gov/?term=" + q.replace(" ", "+")


SEX = F("sex", "radio", "Sex", options=[("f", "Female"), ("m", "Male")])
AGE = F("age", "num", "Age", min=18, max=100, step=1, ph="35", unit="years")
HEIGHT = F("height", "height", "Height")
WEIGHT = F("weight", "weight", "Weight")
ACTIVITY = F("activity", "select", "Activity level", default="1.375", wide=True, options=[
    ("1.2", "Sedentary: desk job, little or no exercise"),
    ("1.375", "Lightly active: exercise 1–3 days a week"),
    ("1.55", "Moderately active: exercise 3–5 days a week"),
    ("1.725", "Very active: hard exercise 6–7 days a week"),
    ("1.9", "Extremely active: physical job plus training"),
])

CDC_BMI = ("CDC: Adult BMI categories", "https://www.cdc.gov/bmi/")
WHO_PA = ("WHO guidelines on physical activity and sedentary behaviour (2020)", "https://www.who.int/publications/i/item/9789240015128")
USPSTF = ("U.S. Preventive Services Task Force: A and B recommendations", "https://www.uspreventiveservicestaskforce.org/uspstf/recommendation-topics/uspstf-a-and-b-recommendations")
AHA_BP = ("American Heart Association: Understanding blood pressure readings", "https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings")
ACC_AHA_2025 = ("2025 AHA/ACC high blood pressure guideline (Circulation)", "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001356")
MIFFLIN = ("Mifflin MD, et al. A new predictive equation for resting energy expenditure. Am J Clin Nutr, 1990", pm("Mifflin St Jeor 1990 resting energy expenditure"))
COMPENDIUM = ("Adult Compendium of Physical Activities", "https://pacompendium.com/")
NASEM_MACRO = ("National Academies: Dietary Reference Intakes for macronutrients", "https://nap.nationalacademies.org/catalog/10490")
NHLBI_METS = ("NHLBI: Metabolic syndrome", "https://www.nhlbi.nih.gov/health/metabolic-syndrome")
KODAMA = ("Kodama S, et al. Cardiorespiratory fitness and mortality: a meta-analysis. JAMA, 2009", pm("Kodama 2009 cardiorespiratory fitness meta-analysis JAMA"))
DING = ("Ding D, et al. Daily steps and health outcomes in adults. Lancet Public Health, 2025", "https://pubmed.ncbi.nlm.nih.gov/40713949/")
