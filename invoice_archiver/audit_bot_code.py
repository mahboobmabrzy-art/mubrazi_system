import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

patterns = {
    "Hardcoded_Token": re.compile(r"API_TOKEN\s*=\s*['\"].+['\"]"),
    "Placeholder_IDs": re.compile(r"YOUR_"),
    "Missing_MediaFileUpload": re.compile(r"MediaFileUpload\s*\("),
    "Tempfile_Recommendation": re.compile(r"open\(.+invoice_.*\.jpg"),
    "No_cleanup_risk": re.compile(r"remove\("),
    "Drive_fields_missing": re.compile(r"fields\s*=\s*['\"]id,\s*webViewLink['\"]"),
}

def scan_file(path):
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()

        for name, pat in patterns.items():
            if pat.search(txt):
                findings.append(name)
        return findings
    except Exception:
        return ["ReadError"]

def main():
    issues = []
    for base, _, files in os.walk(ROOT):
        for fn in files:
            if fn.endswith(".py"):
                p = os.path.join(base, fn)
                fnds = scan_file(p)
                if fnds:
                    issues.append((p, sorted(set(fnds))))
    out = "audit_report.txt"
    with open(out, "w", encoding="utf-8") as f:
        for p, fnds in issues:
            f.write(p + "\n")
            for x in fnds:
                f.write(f" - {x}\n")
            f.write("\n")
    print(f"Done. Report saved to: {out}")
    print(f"Scanned {len(issues)} files with findings.")

if __name__ == "__main__":
    main()
