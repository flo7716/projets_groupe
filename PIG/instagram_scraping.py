import httpx
import json
from typing import Dict
from urllib.parse import quote

INSTAGRAM_DOCUMENT_ID = "8845758582119845" # contst id for post documents instagram.com


def scrape_post(url_or_shortcode: str) -> Dict:
    """Scrape single Instagram post data"""
    if "http" in url_or_shortcode:
        shortcode = url_or_shortcode.split("/p/")[-1].split("/")[0]
    else:
        shortcode = url_or_shortcode
    print(f"scraping instagram post: {shortcode}")

    variables = quote(json.dumps({
        'shortcode':shortcode,'fetch_tagged_user_count':None,
        'hoisted_comment_id':None,'hoisted_reply_id':None
    }, separators=(',', ':')))
    body = f"variables={variables}&doc_id={INSTAGRAM_DOCUMENT_ID}"
    url = "https://www.instagram.com/graphql/query"

    result = httpx.post(
        url=url,
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=body
    )
    data = json.loads(result.content)
    return data["data"]["xdt_shortcode_media"]

# Example usage:
posts = scrape_post("https://www.instagram.com/p/CuE2WNQs6vH/")

# save a JSON file
with open("result.json", "w",encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)


