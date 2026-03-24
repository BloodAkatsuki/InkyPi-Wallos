# InkyPi Wallos Plugin

Ein [InkyPi](https://github.com/fatihak/InkyPi)-Plugin, das Abonnement-Daten aus einer selbst gehosteten [Wallos](https://github.com/henrywhitaker3/Wallos)-Instanz anzeigt.

## Features

- Zeigt die nächsten fälligen Abonnements sortiert nach Fälligkeitsdatum
- Farbkodierung: rot (≤ 3 Tage), orange (≤ 7 Tage)
- Optionale Anzeige der monatlichen Gesamtkosten
- Optionale Logos der Abonnements
- Konfigurierbare Anzahl angezeigter Abonnements (3–10)
- Responsives Layout für Quer- und Hochformat

## Installation

1. Den Ordner `wallos/` nach `src/plugins/wallos/` in deiner InkyPi-Installation kopieren:
   ```bash
   cp -r wallos/ /pfad/zu/InkyPi/src/plugins/wallos/
   ```
2. InkyPi neu starten
3. In der Web-UI: Plugin hinzufügen → **Wallos** auswählen
4. Wallos-URL und API-Key eingeben

## Konfiguration

| Einstellung | Beschreibung | Standard |
|---|---|---|
| Wallos URL | URL deiner Wallos-Instanz | – |
| API Key | Wallos API-Key | – |
| Anzahl Abonnements | Wie viele Einträge angezeigt werden | 5 |
| Monatskosten anzeigen | Gesamtkosten im Header | ✓ |
| Logos anzeigen | Abonnement-Logos | ✓ |
| Farbe: Fällig bald | Farbe für ≤ 3 Tage | `#c62828` |
| Farbe: Fällig diese Woche | Farbe für ≤ 7 Tage | `#e65100` |

## Wallos API

Das Plugin nutzt folgende Wallos-Endpunkte:

- `GET /api/subscriptions?apiKey=...&sort=next_payment&state=0`
- `GET /api/getmonthlycost?apiKey=...&month=...&year=...`

## Lizenz

MIT – siehe [LICENSE](LICENSE)
