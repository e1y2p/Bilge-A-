"""
Medya oynatma — Windows için Spotify URI scheme.
"""

from __future__ import annotations

import subprocess
import urllib.parse


def _play_spotify(query: str, autoplay: bool = True) -> str:
    encoded_query = urllib.parse.quote(query.strip())
    search_url = f"spotify:search:{encoded_query}"
    try:
        subprocess.run(["start", "", search_url], shell=True, timeout=10)
    except Exception as exc:
        return f"Spotify açılamadı: {exc}"
    return f"Spotify'da '{query}' araması açıldı."


def play_media(query: str, provider: str = "auto", autoplay: bool = True) -> str:
    if not query or not query.strip():
        return "Çalınacak içerik belirtilmedi."

    normalized_provider = (provider or "auto").strip().lower()
    if normalized_provider not in {"auto", "spotify"}:
        return "Yalnızca Spotify destekleniyor. provider=spotify kullan."

    return _play_spotify(query, autoplay=autoplay)
