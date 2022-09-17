from pathlib import Path

CACHE_DIR = Path.home() / '.cache' / 'AzusaUploaderToolbox'


def ensure_dirs():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


ensure_dirs()
