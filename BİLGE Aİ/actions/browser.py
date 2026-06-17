"""
Tarayıcı kontrolü — Windows için webbrowser modülü ile çalışır.
"""

import urllib.parse
import webbrowser


def _open(url: str) -> None:
    webbrowser.open(url)


def browser_control(action: str, url: str = None, query: str = None) -> str:
    if action == "open_url":
        if not url:
            return "URL belirtilmedi."
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        _open(url)
        return f"Açıldı: {url}"

    elif action == "search":
        if not query:
            return "Arama sorgusu belirtilmedi."
        encoded = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded}"
        _open(search_url)
        return f"'{query}' için arama açıldı."

    return f"Bilinmeyen eylem: {action}"
