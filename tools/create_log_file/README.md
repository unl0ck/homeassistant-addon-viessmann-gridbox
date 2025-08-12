# Gridbox Monitor

Holt Live-Energiedaten aus deiner Viessmann Gridbox.

## Installation

```bash
pip install playwright python-dotenv
playwright install chromium
```

## Konfiguration

Erstelle eine `.env` Datei:

```
USERNAME=deine.email@beispiel.de
PASSWORD=deinPasswort123
```

## Verwendung

```bash
python main.py
```

## Ausgabe

- `api_responses.txt` - Live- und historische Energiedaten als JSON
- `live_view.png` - Screenshot der Webseite
- `auth.json` - Gespeicherte Login-Session **nicht an mich senden!!!!**
