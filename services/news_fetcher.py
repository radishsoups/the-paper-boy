import os
import requests

NEWS_URL = "https://newsapi.org/v2/everything"


def fetch_news(date: str):
    """
    Fetch tech news and filter by date locally.
    This is more reliable than NewsAPI date filtering.
    """
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY environment variable not set")

    params = {
        "q": "technology OR AI OR Apple OR Google OR Microsoft",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": api_key,
    }

    res = requests.get(NEWS_URL, params=params)

    print("STATUS:", res.status_code)
    print("REQUEST URL:", res.url)

    data = res.json()
    
    # Check for API errors
    if data.get("status") == "error":
        error_message = data.get("message", "Unknown error")
        print(f"API ERROR: {error_message}")
        raise ValueError(f"NewsAPI error: {error_message}")
    
    if res.status_code != 200:
        print(f"HTTP ERROR: {res.status_code}")
        raise ValueError(f"HTTP error: {res.status_code}")
    
    articles = data.get("articles", [])
    print(f"Total articles returned from API: {len(articles)}")
    
    if articles:
        print(f"Sample article dates: {[a.get('publishedAt', '')[:10] for a in articles[:5]]}")

    target_date = date[:10]  # "2026-05-13"

    filtered = []

    for a in articles:
        published_at = a.get("publishedAt", "")[:10]  # YYYY-MM-DD

        if published_at == target_date:
            filtered.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "source": a.get("source", {}).get("name"),
                "url": a.get("url"),
                "publishedAt": published_at,
            })

    print(f"Articles matching {target_date}: {len(filtered)}")
    
    # If no exact date match, return all articles (NewsAPI has a delay)
    if not filtered and articles:
        print(f"No articles for exact date {target_date}, returning all {len(articles)} articles")
        filtered = [{
            "title": a.get("title"),
            "description": a.get("description"),
            "source": a.get("source", {}).get("name"),
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt", "")[:10],
        } for a in articles]

    return filtered
