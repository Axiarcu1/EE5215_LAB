"""Extract embedded PNGs from I2C-Master-Controller-Report.docx in document order."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "I2C-Master-Controller-Report.docx"
OUT = ROOT / "figures" / "i2c_from_docx"


def main() -> None:
    z = zipfile.ZipFile(DOCX)
    xml = z.read("word/document.xml").decode("utf-8")
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")

    rid_map: dict[str, str] = {}
    for m in re.finditer(
        r'Relationship Id="(rId\d+)"[^>]+Target="([^"]+)"',
        rels,
    ):
        rid_map[m.group(1)] = m.group(2)

    embed_ids = re.findall(r'r:embed="(rId\d+)"', xml)
    ordered: list[str] = []
    seen: set[str] = set()
    for rid in embed_ids:
        target = rid_map.get(rid, "")
        if "media/" not in target:
            continue
        name = target.split("/")[-1]
        if name not in seen:
            seen.add(name)
            ordered.append(name)

    OUT.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(ordered, start=1):
        data = z.read(f"word/media/{name}")
        (OUT / f"fig{i:02d}.png").write_bytes(data)
    z.close()


if __name__ == "__main__":
    main()
