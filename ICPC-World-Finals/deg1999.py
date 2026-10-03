#!/usr/bin/env python3
"""Font-aware de-garbler for the 1999 World Finals PDF.

The PDF uses custom Type1C/Type3 fonts (no ToUnicode) whose character codes are
byte-shifted by +0x1D (29) relative to the glyphs they draw; the standard fonts
extract cleanly. This tool parses each page's content stream, tracks the active
font (by resource name -> font object id), and records every text run with its
position. Diagnostic mode shows per-font-object raw vs shifted samples so we can
confirm exactly which objects are shifted.
"""
import re
import sys
import zlib
from collections import defaultdict

PDF = "/home/thaind/qwen_test/ICPC-World-Finals/1999-ICPC-World-Finals/1999WorldFinalProblemSet.pdf"
SHIFT = 0x1D


def shift(s):
    out = []
    for ch in s:
        d = ord(ch) + SHIFT
        out.append(chr(d) if 0x20 <= d < 0x7F else ch)
    return "".join(out)


def read_pdf():
    with open(PDF, "rb") as f:
        return f.read()


def parse_objects(data):
    objs = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", data, re.S):
        objs[int(m.group(1))] = m.group(2)
    return objs


def stream_bytes(objs, objnum):
    body = objs.get(objnum)
    if body is None:
        return None
    m = re.search(rb"stream\r?\n", body)
    if not m:
        return None
    start = m.end()
    end = body.rfind(b"endstream")
    raw = body[start:end]
    if raw.endswith(b"\r\n"):
        raw = raw[:-2]
    elif raw.endswith(b"\n") or raw.endswith(b"\r"):
        raw = raw[:-1]
    try:
        return zlib.decompress(raw)
    except Exception:
        return raw


def all_page_leaf_ids(objs):
    """Collect all /Type /Page (leaf) object ids."""
    leaves = []
    for num, body in objs.items():
        if re.search(rb"/Type\s*/Page\b(?!s)", body):
            leaves.append(num)
    # order by position in the file (approximates document order for these PDFs)
    return leaves


def font_name_to_obj(page_body):
    fonts = {}
    m = re.search(rb"/Font\s*<<(.*?)>>", page_body, re.S)
    if not m:
        return fonts
    for nm in re.finditer(rb"/([A-Za-z0-9_]+)\s+(\d+)\s+0\s+R", m.group(1)):
        fonts[nm.decode()] = int(nm.group(2))
    return fonts


def page_content_bytes(objs, page_body):
    m = re.search(rb"/Contents\s+(\d+)\s+0\s+R", page_body)
    if m:
        s = stream_bytes(objs, int(m.group(1)))
        return s if s is not None else b""
    m = re.search(rb"/Contents\s*\[([^\]]*)\]", page_body)
    if m:
        refs = re.findall(rb"(\d+)\s+0\s+R", m.group(1))
        return b"".join(filter(None, (stream_bytes(objs, int(r)) for r in refs)))
    return b""


def parse_strings_in_array(content, j):
    """content[j] == '['. Return (concat_str_bytes, next_index_after_closing)."""
    parts = []
    i = j + 1
    n = len(content)
    while i < n:
        c = content[i:i + 1]
        if c == b")" and False:
            pass
        if c == b"(":
            s, i = read_literal(content, i)
            parts.append(s)
            continue
        if c == b"<" and content[i + 1:i + 2] != b"<":
            e = content.index(b">", i)
            hexs = re.sub(rb"\s", b"", content[i + 1:e])
            if len(hexs) % 2:
                hexs += b"0"
            try:
                parts.append(bytes.fromhex(hexs.decode()))
            except Exception:
                pass
            i = e + 1
            continue
        if c == b"]":
            return b"".join(parts), i + 1
        i += 1
    return b"".join(parts), n


def read_literal(content, i):
    """content[i] == '('. Return (decoded_bytes, next_index)."""
    depth = 1
    i += 1
    out = bytearray()
    n = len(content)
    while i < n and depth > 0:
        b = content[i]
        if b == 0x5C:  # backslash
            i += 1
            if i >= n:
                break
            e = content[i]
            mp = {ord("n"): 10, ord("r"): 13, ord("t"): 9,
                  ord("b"): 8, ord("f"): 12, ord("("): 40,
                  ord(")"): 41, ord("\\"): 92}
            if e in mp:
                out.append(mp[e]); i += 1
            elif 0x30 <= e <= 0x37:
                o = content[i:i + 3]
                digits = ""
                for cc in o:
                    if 0x30 <= cc <= 0x37:
                        digits += chr(cc)
                    else:
                        break
                out.append(int(digits or "0", 8) & 0xFF)
                i += len(digits)
            else:
                out.append(e); i += 1
            continue
        if b == 0x28:
            depth += 1
        elif b == 0x29:
            depth -= 1
            if depth == 0:
                i += 1
                break
        if depth > 0:
            out.append(b)
        i += 1
    return bytes(out), i


def extract_runs(content, fontmap=None):
    """Return list of (font_key, raw_bytes, x, y). font_key is the object id
    (via fontmap) if a map is given, else the raw resource name."""
    runs = []
    i = 0
    n = len(content)
    cur_font = None
    x = y = 0.0
    tlx = tly = 0.0
    leading = 0.0
    while i < n:
        c = content[i:i + 1]
        if c in b" \t\r\n":
            i += 1
            continue
        if c == b"/":
            m = re.match(rb"/([A-Za-z0-9_+.\-]+)", content[i:])
            name = m.group(1).decode()
            rest = content[i + m.end():]
            mm = re.match(rb"\s*(?:[-\d.]+\s+)*?Tf", rest)
            if mm:
                cur_font = fontmap.get(name, name) if fontmap else name
                i += m.end() + mm.end()
            else:
                i += m.end()
            continue
        if c == b"(":
            s, i = read_literal(content, i)
            # check if a show op follows
            tail = content[i:i + 30].lstrip()
            if tail.startswith(b"Tj") or tail.startswith(b"'") or tail.startswith(b'"'):
                runs.append((cur_font, s, x, y))
                if tail[:1] in (b"'", b'"'):
                    tly -= leading; tlx = 0.0; x, y = tlx, tly
            # else: string not a direct show (arrays handled by the [ branch) - skip
            continue
        if c == b"<" and content[i + 1:i + 2] != b"<":
            e = content.index(b">", i)
            hexs = re.sub(rb"\s", b"", content[i + 1:e])
            if len(hexs) % 2:
                hexs += b"0"
            try:
                s = bytes.fromhex(hexs.decode())
            except Exception:
                s = b""
            tail = content[e + 1:e + 31].lstrip()
            if tail.startswith(b"Tj") or tail.startswith(b"'") or tail.startswith(b'"'):
                runs.append((cur_font, s, x, y))
            i = e + 1
            continue
        if c == b"[":
            s, j = parse_strings_in_array(content, i)
            if content[j - 1:j] == b"]":
                tail = content[j:j + 10].lstrip()
                if tail.startswith(b"TJ"):
                    runs.append((cur_font, s, x, y))
                    i = j + 2
                    continue
            i = j
            continue
        # positioning / state operators
        m6 = re.match(rb"([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm", content[i:])
        if m6:
            x = y = float(m6.group(5)); tlx, tly = x, y
            i += m6.end()
            continue
        m2n = re.match(rb"([-\d.]+)\s+([-\d.]+)\s+(Td|TD)", content[i:])
        if m2n:
            a = float(m2n.group(1)); b = float(m2n.group(2))
            tlx += a; tly += b; x, y = tlx, tly
            if m2n.group(3) == b"TD":
                leading = -b
            i += m2n.end()
            continue
        if content[i:i + 2] == b"T*":
            tly -= leading; tlx = 0.0; x, y = tlx, tly
            i += 2
            continue
        i += 1
    return runs


WORDS = set("""the and for are but not you all can had her was one our out day get has him his how man new now old see two way who boy did its let put say she too use that with have this will your from they know were an as by we when which use each she them there can only other into some time about many then them these out over such through would could should before after because between without under again more most very just like here where while than also long even same great little first being made both well must back good small large high open turn start show give end move right hand large close point plant cover light between night side above across under into upon within upon since along among across""".split())


def score(text):
    toks = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return sum(1 for t in toks if t in WORDS)


def detect_shift(text):
    best = (0, score(text))
    for sh in range(-64, 128):
        if sh == 0:
            continue
        dec = "".join(chr(ord(c) + sh) if 0x20 <= ord(c) + sh < 0x7F else c for c in text)
        s = score(dec)
        if s > best[1]:
            best = (sh, s)
    sh, sc = best
    # require a clear English signal, else treat as wordless (leave unshifted)
    if sc < 4:
        return 0
    return sh


def decode(text, sh):
    if not sh:
        return text
    return "".join(chr(ord(c) + sh) if 0x20 <= ord(c) + sh < 0x7F else c for c in text)


# Verified per-resource-name shift table (resource names are stable across all
# pages of this PDF; every decoded sample is correct English or correct art).
SHIFTS = {"F3": 0, "F4": 0, "F5": 0, "F6": 29, "F7": 29, "F8": 0,
          "F9": 0, "F10": 30, "F11": 0, "F12": 0, "F13": 0, "F14": 29, "T1": 0}


def page_runs(objs, pnum):
    body = objs[pnum]
    fmap = font_name_to_obj(body)
    content = page_content_bytes(objs, body)
    return extract_runs(content, fmap), fmap


def build_lines(runs):
    """Group decoded runs into visual lines by y, ordered by x."""
    items = []
    for font, raw, x, y in runs:
        sh = SHIFTS.get(font, 0) if isinstance(font, str) else 0
        txt = decode(raw.decode("latin-1"), sh)
        if txt.strip() == "":
            continue
        items.append((y, x, txt))
    # PDF y=0 is at the page BOTTOM; sort top-to-bottom by y descending, then x.
    items.sort(key=lambda t: (-t[0], t[1]))
    lines = []
    cur_y = None
    for y, x, txt in items:
        if cur_y is None or abs(y - cur_y) > 3.5:
            lines.append([])
            cur_y = y
        lines[-1].append((x, txt))
    out = []
    for ln in lines:
        ln.sort(key=lambda t: t[0])
        out.append(ln)
    return out


def dump():
    data = read_pdf()
    objs = parse_objects(data)
    leaves = all_page_leaf_ids(objs)
    out = []
    for pnum in leaves:
        runs, _ = page_runs(objs, pnum)
        out.append(f"\n\n########## PAGE obj {pnum} ##########\n")
        for ln in build_lines(runs):
            out.append(" ".join(t for _, t in ln))
    with open("/tmp/1999_clean.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("wrote /tmp/1999_clean.txt", sum(len(x) for x in out), "chars")


def main():
    data = read_pdf()
    objs = parse_objects(data)
    leaves = all_page_leaf_ids(objs)
    perfont = defaultdict(bytearray)
    for pnum in leaves:
        runs, _ = page_runs(objs, pnum)
        for font, raw, x, y in runs:
            if font is not None:
                perfont[font].extend(raw)
    print("pages:", len(leaves))
    print("=== per font-object: detected shift + decoded sample ===")
    for obj, raw in sorted(perfont.items(), key=lambda kv: str(kv[0])):
        txt = raw.decode("latin-1")
        sh = detect_shift(txt)
        print(f"\n### obj {obj}  shift={sh:+d}")
        print("  DECODED:", repr(decode(txt, sh)[:150]))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dump":
        dump()
    else:
        main()
