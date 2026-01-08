#!/usr/bin/env python3
"""
Kalshi NYC High Temperature Betting Strategy
Advanced analysis comparing multiple forecast sources

This script provides real-time forecast comparison for betting decisions.
"""

import requests
import json
from datetime import datetime, timedelta

# NYC Central Park coordinates
NYC_LAT = 40.7829
NYC_LON = -73.9654

def get_open_meteo_forecast():
    """Get current forecast from Open-Meteo (free)"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": NYC_LAT,
        "longitude": NYC_LON,
        "daily": "temperature_2m_max",
        "temperature_unit": "fahrenheit",
        "timezone": "America/New_York",
        "forecast_days": 7
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecasts = []
        if "daily" in data:
            for i, date in enumerate(data["daily"]["time"]):
                forecasts.append({
                    "date": date,
                    "high_temp": data["daily"]["temperature_2m_max"][i]
                })
        return forecasts
    except Exception as e:
        print(f"Error fetching Open-Meteo: {e}")
        return None

def get_nws_forecast():
    """Get forecast from National Weather Service (settlement source!)"""
    # First get the forecast grid endpoint for NYC
    points_url = f"https://api.weather.gov/points/{NYC_LAT},{NYC_LON}"

    try:
        headers = {"User-Agent": "KalshiWeatherAnalysis/1.0"}
        response = requests.get(points_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast_url = data["properties"]["forecast"]
        response = requests.get(forecast_url, headers=headers, timeout=10)
        response.raise_for_status()
        forecast_data = response.json()

        forecasts = []
        for period in forecast_data["properties"]["periods"]:
            if period["isDaytime"]:
                forecasts.append({
                    "name": period["name"],
                    "high_temp": period["temperature"],
                    "short_forecast": period["shortForecast"]
                })
        return forecasts
    except Exception as e:
        print(f"Error fetching NWS: {e}")
        return None

def display_current_forecasts():
    """Display and compare current forecasts"""
    print("=" * 60)
    print("CURRENT NYC HIGH TEMPERATURE FORECASTS")
    print("=" * 60)
    print(f"Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Get Open-Meteo forecast
    print("\n--- Open-Meteo Forecast ---")
    om_forecast = get_open_meteo_forecast()
    if om_forecast:
        for day in om_forecast[:5]:
            print(f"  {day['date']}: {day['high_temp']:.0f}°F")
    else:
        print("  Unable to fetch")

    # Get NWS forecast (settlement source)
    print("\n--- NWS Forecast (SETTLEMENT SOURCE) ---")
    nws_forecast = get_nws_forecast()
    if nws_forecast:
        for period in nws_forecast[:5]:
            print(f"  {period['name']}: {period['high_temp']}°F - {period['short_forecast']}")
    else:
        print("  Unable to fetch")

    print("\n" + "=" * 60)
    print("FORECAST COMPARISON")
    print("=" * 60)

    if om_forecast and nws_forecast:
        # Compare first day
        om_today = om_forecast[0]['high_temp']
        nws_today = nws_forecast[0]['high_temp']
        diff = abs(om_today - nws_today)

        print(f"\nToday's High Forecast Comparison:")
        print(f"  Open-Meteo: {om_today:.0f}°F")
        print(f"  NWS: {nws_today}°F")
        print(f"  Difference: {diff:.1f}°F")

        if diff <= 2:
            print("\n  ✓ Strong agreement - HIGH CONFIDENCE")
        elif diff <= 4:
            print("\n  ~ Moderate agreement - MEDIUM CONFIDENCE")
        else:
            print("\n  ⚠ Significant disagreement - LOW CONFIDENCE")

    print("\n" + "=" * 60)
    print("BETTING GUIDANCE")
    print("=" * 60)

    print("""
For Kalshi NYC High Temp bets, always check:

1. NWS (weather.gov) - This is the SETTLEMENT SOURCE
   - Kalshi uses NWS Daily Climate Report for Central Park
   - URL: weather.gov/okx

2. AccuWeather (accuweather.com)
   - Historically most accurate predictor
   - Compare their forecast to NWS

3. Weather Channel (weather.com)
   - Second most accurate commercial source

BETTING STRATEGY:
- If all 3 sources agree within 2°F: BET CONFIDENTLY
- If sources differ by 3-4°F: BET CAUTIOUSLY
- If sources differ by 5+°F: CONSIDER AVOIDING OR BET ON RANGE

TIMING TIP:
- Check forecasts multiple times per day
- Models update at 00Z, 06Z, 12Z, 18Z (UTC)
- Later updates are more accurate
""")

def show_accuracy_summary():
    """Display compiled accuracy rankings"""
    print("\n" + "=" * 60)
    print("FORECAST PROVIDER ACCURACY RANKINGS (NYC 2024)")
    print("=" * 60)
    print("Source: ForecastAdvisor.com + Independent Studies\n")

    # Combined ranking based on multiple sources
    providers = [
        ("AccuWeather", "~87%*", "Best in ForecastWatch studies, not on ForecastAdvisor"),
        ("Microsoft", "85.42%", "ForecastAdvisor 2024 YTD"),
        ("The Weather Channel", "84.93%", "ForecastAdvisor 2024 YTD"),
        ("Foreca", "84.01%", "ForecastAdvisor 2024 YTD"),
        ("AerisWeather", "83.19%", "ForecastAdvisor 2024 YTD"),
        ("Weatherbit", "81.33%", "ForecastAdvisor 2024 YTD"),
        ("NWS Digital", "78.04%", "ForecastAdvisor 2024 YTD"),
        ("Open-Meteo", "73.45%", "ForecastAdvisor 2024 YTD"),
    ]

    print(f"{'Rank':<6}{'Provider':<22}{'Accuracy':<12}{'Source'}")
    print("-" * 70)
    for i, (provider, accuracy, source) in enumerate(providers, 1):
        print(f"{i:<6}{provider:<22}{accuracy:<12}{source}")

    print("\n*AccuWeather accuracy estimated from their own studies")
    print(" (within 3°F accuracy metric)")

def main():
    print("\n" + "=" * 60)
    print("KALSHI NYC HIGH TEMPERATURE BETTING TOOL")
    print("=" * 60)

    # Show accuracy rankings
    show_accuracy_summary()

    # Show current forecasts
    display_current_forecasts()

    # Final recommendation
    print("\n" + "=" * 60)
    print("RECOMMENDED TOOL: AccuWeather")
    print("=" * 60)
    print("""
For Kalshi NYC high temperature betting, use:

PRIMARY: AccuWeather (accuweather.com)
  - Consistently #1 in accuracy studies
  - Lowest mean absolute error
  - Best for 1-5 day forecasts

ALWAYS CROSS-CHECK: NWS (weather.gov)
  - This is what Kalshi uses for settlement!
  - Your bet settles based on NWS Climate Report

SECONDARY: Weather Channel, Microsoft Weather
  - Use for confirmation

FREE API ACCESS: Open-Meteo
  - For automated analysis
  - Historical forecast data available
""")

if __name__ == "__main__":
    main()
