"""Build the GetRecruiters edition of the 2026 Recruiter Salary Guide.

The numbers come from the guide the 100X site already publishes, so both always match. This swaps the
look and the name: a light cover, the GetRecruiters orange, and GetRecruiters as the only brand.

    python tools/make_salary_guide.py <100x-workforce-salary-guide-recruiters.html> [cover-html-path]

Writes downloads/getrecruiters-salary-guide-recruiters.html. Chrome then prints that page to
downloads/GetRecruiters-Salary-Guide-2026-Recruiters.pdf, and shoots the cover page (the second path)
at 680x880 for img/getrecruiters-recruiters-cover.png.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "downloads" / "getrecruiters-salary-guide-recruiters.html"

TOKENS = """:root {
  --ink:#1F1F1F; --navy:#551B00; --panel:#FFFFFF; --blue:#C2410C; --cyan:#FF6200; --band:#FFD6BA;
  --paper: #FFFFFF; --wash: #FFF7F2; --muted: #5A504A; --rule: #F1E3D9;
  --font: 'DM Sans', 'Segoe UI', Helvetica, Arial, sans-serif; --display: 'DM Sans', 'Segoe UI', Helvetica, Arial, sans-serif;
  color-scheme: light;
}"""

LIGHT = """
/* GetRecruiters edition: everything light and easy to read. */
h1 { font-weight: 300; letter-spacing: -.02em; color: #1F1F1F; }
h2 { font-weight: 400; letter-spacing: -.015em; color: #1F1F1F; }
.cover { background: var(--wash); color: var(--ink); border-top: 16px solid #FF6200; }
.cover::after { display: none; }
.cover .eyebrow { color: #C2410C; font-size: .9rem; }
.cover h1 { font-size: clamp(3.6rem, 10vw, 6rem); font-weight: 300; color: #1F1F1F; }
.cover .lede { color: #41302A; font-size: 1.4rem; line-height: 1.35; }
.tile { border: 1px solid var(--rule); background: #fff; }
.tile b { color: #C2410C; font-weight: 500; font-size: 2.5rem; letter-spacing: -.02em; }
.tile span { color: var(--ink); font-size: 1rem; font-weight: 500; }
.tile small { color: var(--muted); }
.cover .src { color: var(--muted); }
.grl { display: inline-grid; gap: 6px; justify-self: start; }
.gw { display: inline-flex; align-items: flex-start; gap: 3px; font: 700 42px/1 'Quicksand', 'DM Sans', sans-serif; letter-spacing: -.02em; color: #1F1F1F; }
.gw svg { width: 16px; height: 16px; margin-top: 2px; fill: #FF6200; }
.gw svg circle { fill: #fff; }
.gt { font-size: 17px; font-weight: 600; line-height: 1; color: #C2410C; }
.chart .fill { fill: #FF6200; }
.chart .dot { fill: #551B00; }
.takeaway { border-left-color: #FF6200; }
ol.tips li::marker { color: #C2410C; }
.cta { background: #FFEFE5; color: var(--ink); }
.cta h2 { color: #551B00; }
.cta p { color: #41302A; }
.cta .go { background: #C2410C; color: #fff; font-weight: 600; }
body.only-cover { background: var(--wash); }
.only-cover .doc { max-width: none; padding: 0; }
.only-cover section:not(.cover) { display: none; }
.only-cover .cover { width: 680px; height: 880px; padding: 56px 48px; border-radius: 0; border-left: 0; border-right: 0; border-bottom: 0; align-content: center; }
.only-cover .tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); }
"""

WORDMARK = ('<span class="grl"><span class="gw">getrecruiters<svg viewBox="0 0 30 30" aria-hidden="true">'
            '<rect width="30" height="30" rx="7"/><circle cx="8" cy="8" r="3.2"/><circle cx="22" cy="8" r="3.2"/>'
            '<circle cx="15" cy="15" r="3.2"/><circle cx="8" cy="22" r="3.2"/><circle cx="22" cy="22" r="3.2"/></svg></span>'
            '<span class="gt">Recruiters for Anything</span></span>')

CTA = """<section class="cta">
  <h2>Need 1 recruiter or a whole team?</h2>
  <p>GetRecruiters finds recruiters and puts them to work. Hire as a Temp, Temp-to-Perm, or Direct Hire. We can payroll every hire, with benefits and 401(k) handled. You only pay when you hire.</p>
  <a class="go" href="https://www.getrecruiters.com/request-talent.html" target="_blank" rel="noopener">Tell us who you need &rarr; getrecruiters.com</a>
</section>"""


def swap(html, pattern, new, label):
    out, n = re.subn(pattern, lambda _: new, html, flags=re.S)
    if n < 1:
        sys.exit(f"nothing matched for {label}: the source guide changed")
    return out


def main():
    html = Path(sys.argv[1]).read_text(encoding="utf-8")
    html = swap(html, r"<title>.*?</title>", "<title>GetRecruiters Salary Guide 2026 · Recruiters</title>", "title")
    html = swap(html, r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">',
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700'
                '&family=Quicksand:wght@700&display=swap">', "fonts")
    html = swap(html, r"/\* Layout: a printed report\..*?\*/", "/* Layout: a printed report. Light cover, then white pages. */", "layout note")
    html = swap(html, r":root \{.*?\n\}", TOKENS, "tokens")
    html = html.replace("</style>", LIGHT + "</style>", 1)
    html = swap(html, r'<span class="lock">.*?</span></span>(?=\n)', WORDMARK, "logo")
    html = swap(html, r'<section class="cta">.*?</section>', CTA, "closing page")
    html = swap(html, r"Recruiters also count in our HR &amp; Recruiting guide\. This guide adds everyone",
                "This guide counts everyone", "other guide note")
    html = swap(html, r'<p class="small muted">100X Workforce[^<]*</p>',
                '<p class="small muted">GetRecruiters Group, a division of NorthPoint Search Group · getrecruiters.com · © 2026</p>', "footer")

    left = re.findall(r"100x|claude\.ai|zipapply", html, flags=re.I)
    if left:
        sys.exit(f"another brand is still in the guide: {sorted(set(left))}")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT)
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(html.replace("<body>", '<body class="only-cover">', 1), encoding="utf-8")
        print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()
