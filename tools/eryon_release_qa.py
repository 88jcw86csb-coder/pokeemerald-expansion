#!/usr/bin/env python3
"""Inventory of unlocalized Eryon/UI text and provisional art.

Informational only: green CI is NOT certification of Portuguese language
or visual fidelity. Output is machine-readable for each release candidate.
"""
import json
from pathlib import Path
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
ENGLISH = re.compile(r"\b(?:the|your|you|please|where|what|with|choose|save|saving|welcome|cannot|can't|would|there|are|this|themselves|trainer|professor|pokemon is|not enough|item)\b", re.I)
LITERAL = re.compile(r'_(?:\(|\s*\()\s*"((?:[^"\\]|\\.)*)"\s*\)', re.S)
TEXTLINE = re.compile(r'^\s*\.string\s+"((?:[^"\\]|\\.)*)"',re.M)

def collect():
    sources = [
        ROOT/"src/strings.c", ROOT/"src/main_menu.c",
        ROOT/"data/text/birch_speech.inc",
    ]
    names = json.loads((ROOT/"data/maps/map_groups.json").read_text(encoding="utf-8"))
    for region in ("gMapGroup_Eryon","gMapGroup_GymEryon"):
        sources += [ROOT/"data/maps"/name/"scripts.inc" for name in names[region]]
    findings=[]
    totals=Counter()
    for file in sources:
        text=file.read_text(encoding="utf-8")
        blobs = LITERAL.findall(text) if file.suffix==".c" else TEXTLINE.findall(text)
        for value in blobs:
            totals["strings"] += 1
            if ENGLISH.search(value):
                findings.append({"path":str(file.relative_to(ROOT)), "sample":value[:95]})
        totals["files"]+=1
    return {"check":"advisory_not_fully_translated",
            "registered_eryon_maps":len(names["gMapGroup_Eryon"]),
            "gym_maps":len(names["gMapGroup_GymEryon"]),
            "text_files_scanned":totals["files"],
            "strings_scanned":totals["strings"],
            "english_heuristic_count":len(findings),
            "example_english_text":findings[:45],
            "visual_validation":"needs_emulator_screenshots_and_human_review",
            "translation_status":"INCOMPLETE_WHILE_ENGLISH_TEXT_REMAINS"}

def main():
    report=collect()
    path=ROOT/"build/eryon-qa.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"ERYON QA: {report['strings_scanned']} text segments from {report['text_files_scanned']} sources")
    print(f"ERYON QA: {report['english_heuristic_count']} potential English entries (advisory)")
    print("ERYON QA: passing structural tests never certifies visual sharpness or full Portuguese localization.")
    print("ERYON QA report:",path)

if __name__=="__main__":main()
