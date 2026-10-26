"""Make the site's logo, share image and favicons from the NorthPoint-family logo files.

Sources live in img/brand/ (from the "NorthPoint Next Step" logo pack):
  GetRecruiters-trans.png   - color logo, see-through background
  GetRecruiters-trans-W.png - white-text version for dark backgrounds
The arrow favicons are the same family arrow Staff Financial and LawStaff use.

Run from the site root:  python tools/make_images.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
SIBLING_ICONS = ROOT.parent / "staff-financial-group" / "img"  # same arrow favicons


def cropped_logo(src, pad=10):
    """Trim the empty canvas around the logo, keeping a little breathing room."""
    im = Image.open(src).convert("RGBA")
    left, top, right, bottom = im.getchannel("A").getbbox()
    return im.crop((max(left - pad, 0), max(top - pad, 0), min(right + pad, im.width), min(bottom + pad, im.height)))


def share_image(logo):
    """1200x630 white card with the logo centered, for link previews."""
    card = Image.new("RGB", (1200, 630), "white")
    w = 860
    h = round(logo.height * w / logo.width)
    scaled = logo.resize((w, h), Image.LANCZOS)
    card.paste(scaled, ((1200 - w) // 2, (630 - h) // 2), scaled)
    return card


if __name__ == "__main__":
    logo = cropped_logo(IMG / "brand" / "GetRecruiters-trans.png")
    logo.save(IMG / "getrecruiters-logo.png", optimize=True)
    share_image(logo).save(IMG / "og-image.png", optimize=True)
    for name in ("favicon-32.png", "favicon-180.png", "favicon-512.png"):
        if (SIBLING_ICONS / name).exists():
            (IMG / name).write_bytes((SIBLING_ICONS / name).read_bytes())
    print("getrecruiters-logo.png", logo.size, "| og-image.png | favicons copied from Staff Financial")
