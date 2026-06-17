"""
Basit hava durumu ozeti — uzaktaki bir servis uzerinden calisir.
Alp Ünlü tarafından yapılmıştır — @alppunlu

Varsayilan konum:
- JARVIS_WEATHER_LOCATION env varsa onu kullanir
- yoksa Istanbul varsayilir
"""

from __future__ import annotations

import os
import sys

import requests


# Türkçe gün isimleri (ASCII-friendly)
TURKISH_DAYS = {
    "Monday": "Pazartesi",
    "Tuesday": "Sali",
    "Wednesday": "Carsamba",
    "Thursday": "Persembe",
    "Friday": "Cuma",
    "Saturday": "Cumartesi",
    "Sunday": "Pazar",
}


def get_weather_summary(location: str | None = None) -> str:
    target = (location or os.environ.get("JARVIS_WEATHER_LOCATION") or "Istanbul").strip()
    try:
        response = requests.get(
            f"https://wttr.in/{target}",
            params={"format": "j1"},
            timeout=10,
            headers={"User-Agent": "BILGE AI Windows"},
        )
        response.raise_for_status()
        response.encoding = 'utf-8'
        payload = response.json()
        current = (payload.get("current_condition") or [{}])[0]
        temp_c = current.get("temp_C")
        feels_like = current.get("FeelsLikeC")
        weather_desc = ((current.get("weatherDesc") or [{}])[0]).get("value", "")
        humidity = current.get("humidity")

        parts = []
        if temp_c:
            parts.append(f"{temp_c}°")
        if weather_desc:
            parts.append(weather_desc.lower())
        if feels_like and feels_like != temp_c:
            parts.append(f"hiss: {feels_like}°")
        if humidity:
            parts.append(f"nem %{humidity}")

        # Tahmin bilgilerini ekle
        weather_parts = []
        if parts:
            weather_parts.append(f"{target} icin hava durumu: " + " - ".join(parts) + ".")

        # 3 gunluk tahmin
        forecasts = payload.get("weather", [])[:3]
        if forecasts:
            weather_parts.append("\nTahmin:")
            for forecast in forecasts:
                date_str = forecast.get("date", "")
                max_temp = forecast.get("maxtempC", "")
                min_temp = forecast.get("mintempC", "")
                desc = ((forecast.get("hourly") or [{}])[0].get("weatherDesc") or [{}])[0].get("value", "")
                
                # Tarihten gunu cikar
                try:
                    from datetime import datetime
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    day_name = date_obj.strftime("%A")
                    day_tr = TURKISH_DAYS.get(day_name, day_name)
                    day_str = f"{day_tr}"
                except Exception:
                    day_str = date_str

                forecast_parts = []
                if max_temp:
                    forecast_parts.append(f"max {max_temp}°")
                if min_temp:
                    forecast_parts.append(f"min {min_temp}°")
                if desc:
                    forecast_parts.append(desc.lower())
                
                if forecast_parts:
                    weather_parts.append(f"  {day_str}: " + " - ".join(forecast_parts))

        if not weather_parts:
            return "Hava durumu bilgisi su anda alinamadi."

        return "\n".join(weather_parts)
    except Exception as e:
        return f"Hava durumu bilgisi su anda alinamadi. Hata: {str(e)}"
