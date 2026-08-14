#!/usr/bin/env python3
from pathlib import Path
import shutil

candidates = [
    Path("app/FleaPit™ _media_hub_index.html"),
    Path("app/FleaPit™_media_hub_index.html"),
]
path = next((p for p in candidates if p.exists()), None)
if path is None:
    raise SystemExit("ERROR: FleaPit media hub was not found under app/.")

text = path.read_text(encoding="utf-8")
tag = '<script src="fleapit_333_ohmic_bridge.js" defer></script>'
if tag in text:
    print("ALREADY PATCHED:", path)
    raise SystemExit(0)

backup = path.with_suffix(path.suffix + ".pre-ohmic-bridge")
if not backup.exists():
    shutil.copy2(path, backup)

anchor = "</body>"
if anchor not in text:
    raise SystemExit("ERROR: </body> was not found; no change made.")
text = text.replace(anchor, f"  {tag}\n{anchor}", 1)
path.write_text(text, encoding="utf-8")
print("PATCHED:", path)
print("BACKUP:", backup)
