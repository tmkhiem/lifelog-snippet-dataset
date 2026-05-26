import json
from pathlib import Path

def build():
    caption_dir = Path("captions")
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    if not caption_dir.exists():
        print("captions/ directory not found — nothing to build.")
        return

    total = 0
    for caption_file in sorted(caption_dir.glob("*.txt")):
        date_str = caption_file.stem          # e.g. "20200101"
        month = date_str[4:6]                 # e.g. "01"
        entries = []

        with open(caption_file, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                if len(line) < 21:
                    continue
                timestamp = line[:19]         # "2020-01-01 04:49:42"
                caption = line[21:].lstrip()  # skip ": "

                date_part = timestamp[:10].replace("-", "")   # "20200101"
                time_part = timestamp[11:].replace(":", "")   # "044942"
                img = f"keyframes/{month}/{date_part}_{time_part}_000.jpg"

                entries.append({"img": img, "ts": timestamp, "cap": caption})

        out = out_dir / f"{date_str}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

        total += len(entries)
        print(f"  {date_str}: {len(entries):>5} entries -> {out}")

    days = len(list(caption_dir.glob("*.txt")))
    print(f"\nTotal: {total} entries across {days} day(s)")

if __name__ == "__main__":
    build()
