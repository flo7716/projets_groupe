import re

IGNORE_LIST = [
    "Latest", "AI", "Amazon", "Apps", "Biotech & Health", "Climate", "Cloud Computing", 
    "Commerce", "Crypto", "Enterprise", "EVs", "Fintech", "Fundraising", "Gadgets", 
    "Gaming", "Google", "Government & Policy", "Hardware", "Instagram", "Layoffs", 
    "Media & Entertainment", "Meta", "Microsoft", "Privacy", "Robotics", "Security", 
    "Social", "Space", "Startups", "TikTok", "Transportation", "Venture", "Events", 
    "Startup Battlefield", "StrictlyVC", "Newsletters", "Podcasts", "Videos", 
    "Partner Content", "TechCrunch Brand Studio", "Crunchboard", "Contact Us"
]

def filter_summary(text):
    ignore_pattern = r"|".join(re.escape(phrase) for phrase in IGNORE_LIST)
    text = re.sub(ignore_pattern, '', text)
    return text.strip()

if __name__ == "__main__":
    article_text = "This is a news article about AI and Google advancements..."
    filtered_text = filter_summary(article_text)
    print(f"Texte filtré : {filtered_text}")
