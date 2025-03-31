import requests
from typing import List, Dict, Optional


def get_top_news(
        api_key: str,
        country: Optional[str] = None,
        category: Optional[str] = None,
        sources: Optional[str] = None,
        keywords: Optional[str] = None,
        page_size: int = 20,
        page: int = 1,
        max_retries: int = 3
) -> List[Dict]:
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "category": category,
        "sources": sources,
        "q": keywords,
        "pageSize": page_size,
        "page": page
    }

    params = {k: v for k, v in params.items() if v is not None}

    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data["status"] != "ok":
                raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

            return [{
                "title": article["title"],
                "source": article["source"]["name"],
                "description": article.get("description"),
                "url": article["url"],
                "image": article.get("urlToImage"),
                "published_at": article["publishedAt"],
                "content": article.get("content", "")
            } for article in data["articles"]]

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Request failed after {max_retries} attempts: {str(e)}")
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"Invalid API response: {str(e)}")

    return []