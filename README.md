# Solar-Dashboard Deutschland

Dieses Projekt ist die einfachste robuste Architektur für ein tagesaktuelles MaStR-Dashboard:

- `index.html` = statisches Frontend für GitHub Pages
- `data/solar-latest.json` = Datei, die das Frontend lädt
- `raw/*.csv` = MaStR-Exporte als Eingabe
- `scripts/update_mastr_data.py` = wandelt CSV in JSON um
- `.github/workflows/update-solar-data.yml` = täglicher GitHub-Action-Job

## So gehst du vor

1. Neues GitHub-Repository anlegen.
2. Alle Dateien aus diesem Ordner hochladen.
3. In GitHub `Settings > Pages` öffnen und GitHub Pages für den Branch `main` aktivieren.
4. Die Seite wird über `index.html` gestartet.
5. Einen oder mehrere MaStR-CSV-Exporte in den Ordner `raw/` legen.
6. In GitHub unter `Actions` den Workflow **Update solar dashboard data** manuell starten.
7. Danach wird `data/solar-latest.json` erzeugt bzw. aktualisiert.
8. Das Dashboard lädt diese JSON-Datei automatisch.

## Tägliche Aktualisierung

Der Workflow läuft täglich via Cron und schreibt die neue JSON-Datei ins Repository zurück.

## Wichtige Realität

Dieses Setup ist absichtlich stabil und simpel. Es ruft das MaStR nicht direkt im Browser ab, sondern verarbeitet vorbereitete CSV-Dateien. Für eine vollautomatische Live-Anbindung an Webdienste mit Authentifizierung muss das Python-Skript erweitert werden.
