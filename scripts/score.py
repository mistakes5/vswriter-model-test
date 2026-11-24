"""Score round-2 outputs: verbatim quote check, printed-page check, lint counts."""
import re, sys, json, pathlib

S = pathlib.Path(sys.argv[1]); O = pathlib.Path(sys.argv[2])
OFFSET = {"Mellamphy": 9, "Carlson": 414, "Munn": -8}
AUTH = {"Mellamphy": "Mellamphy-2021.md", "Carlson": "Carlson-2015.md", "Munn": "Munn-2022.md"}

def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"(\w)- (\w)", r"\1\2", t)          # rejoin hyphenated line breaks
    t = re.sub(r"[*_`]", "", t)
    return re.sub(r"\s+", " ", t).strip().lower()

pages = {}
for a, f in AUTH.items():
    raw = (S / "readings" / f).read_text()
    out = []
    for blk in re.split(r'<a id="pdf-page-\d+"></a>', raw)[1:]:
        body = blk.split("\n", 6)[-1]
        nums = re.findall(r"^\s*(\d{1,3})\s{2,}\S|\S\s{2,}(\d{1,3})\s*$", body, re.M)
        printed = next((int(x or y) for x, y in nums), None)
        out.append((printed, norm(body)))
    pages[a] = out

def locate(a, q):
    qn = norm(q).strip(' ."\',')
    off = OFFSET[a]   # printed page = PDF page + offset (checked against running headers)
    for i, (p, b) in enumerate(pages[a]):
        if qn in b: return i + 1 + off, False
    for i, (p, b) in enumerate(pages[a][:-1]):   # spans a page break
        if qn in b + " " + pages[a][i + 1][1]: return i + 1 + off, True
    return None, None

def para(text):
    m = re.split(r"DRAFTED PARAGRAPH\**[^\n]*\n", text, flags=re.I)
    return m[-1].strip()

rows = []
for f in sorted(O.glob("*-[123].md")):
    t = f.read_text(); p = para(t)
    cites = re.findall(r'"([^"]{8,}?)"[^"]{0,80}?\((?:[A-Z][\w\s.&]*?)?(Mellamphy|Carlson|Munn)[^:)]*:\s*(\d+)', p.replace("“", '"').replace("”", '"'))
    res = []
    for q, a, pg in cites:
        printed, span = locate(a, q)
        res.append({"author": a, "words": len(q.split()), "verbatim": printed is not None,
                    "page_cited": int(pg), "page_true": printed, "page_ok": printed == int(pg), "spans": span})
    lint = {
        "em_dash": p.count("—"), "semicolon": len(re.findall(r";", p)),
        "suggests/aligns": len(re.findall(r"\b(suggest|align)", p, re.I)),
        "neg_parallel": len(re.findall(r"\bnot (?:merely |simply |just )?\w+[^.]{0,40}?\bbut\b|\brather than\b", p, re.I)),
        "contraction": len(re.findall(r"\b\w+n't\b|\b\w+'(?:re|ll|ve|d)\b", p)),
    }
    picked21 = "21" in [c["page_cited"].__str__() for c in res if c["author"] == "Mellamphy"]
    rows.append({"file": f.name, "words": len(p.split()), "quotes": res, "lint": lint, "mellamphy_p21": picked21})

json.dump(rows, open(O / "scores.json", "w"), indent=1)
for r in rows:
    q = " | ".join(f'{c["author"][:4]} {c["words"]}w v={"Y" if c["verbatim"] else "N"} p{c["page_cited"]}/{c["page_true"]}' for c in r["quotes"])
    print(f'{r["file"]:42} {r["words"]:4}w  {q}  lint={ {k: v for k, v in r["lint"].items() if v} }')
