import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
RAW_DIR = ROOT / 'raw'
OUTPUT_FILE = DATA_DIR / 'solar-latest.json'

def normalize_number(value):
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None

def get_first(row, keys):
    for key in keys:
        value = row.get(key)
        if value is not None and str(value).strip() != '':
            return value
    return None

def iter_csv_rows():
    if not RAW_DIR.exists():
        return []
    for file in RAW_DIR.glob('*.csv'):
        with open(file, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            headers = reader.fieldnames or []
            if len(headers) == 1:
                f.seek(0)
                reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                yield row

def transform(row):
    lat = normalize_number(get_first(row, ['Koordinate: Breitengrad (WGS84)', 'Breitengrad', 'Latitude', 'lat']))
    lon = normalize_number(get_first(row, ['Koordinate: Längengrad (WGS84)', 'Koordinate: Laengengrad (WGS84)', 'Längengrad', 'Laengengrad', 'Longitude', 'lon']))
    power = normalize_number(get_first(row, ['Nettonennleistung der Einheit', 'Nettonennleistung', 'Leistung', 'power_kw']))
    if lat is None or lon is None or power is None:
        return None
    return {
        'unit_id': get_first(row, ['MaStR-Nummer der Einheit', 'EinheitMastrNummer', 'MaStRNummer']),
        'name': get_first(row, ['Name der Einheit', 'Einheitname', 'Name', 'Anlagenname']) or 'Solaranlage',
        'operator': get_first(row, ['Name des Anlagenbetreibers', 'Anlagenbetreiber']),
        'state': get_first(row, ['Bundesland']),
        'city': get_first(row, ['Ort', 'Gemeinde', 'Standort']),
        'type': get_first(row, ['Solaranlagenart', 'Anlagentyp', 'Art der Einheit']),
        'power_kw': power,
        'lat': lat,
        'lon': lon,
    }

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for row in iter_csv_rows():
        item = transform(row)
        if item:
            items.append(item)
    payload = {
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'source': 'Marktstammdatenregister CSV export(s)',
        'count': len(items),
        'items': items,
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    print(f'Wrote {len(items)} items to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
