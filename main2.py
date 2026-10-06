#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DiaaSuperCUPP v5.0 - 2 Million Password Wordlist Generator
For Authorized Security Testing Only
"""

import itertools
import random
import os
import re
from datetime import datetime


# ██████████████████████████████████
# BANNER
# ██████████████████████████████████

def banner():
    print("=" * 70)
    print("   DiaaSuperCUPP - 2 MILLION PASSWORD GENERATOR")
    print("   For Authorized Security Testing Only")
    print("=" * 70)


# ██████████████████████████████████
# DATA COLLECTION
# ██████████████████████████████████

def get_user_data():
    print("\n[+] Enter target information (leave blank if unknown)\n")

    data = {
        'first': input("First Name           : ").strip(),
        'last': input("Last Name            : ").strip(),
        'nick': input("Nickname             : ").strip(),
        'bday': input("Birthdate (DD MM YYYY): ").strip(),
        'partner': input("Partner Name         : ").strip(),
        'pbday': input("Partner Birthdate    : ").strip(),
        'pet': input("Pet Name             : ").strip(),
        'company': input("Company/Work         : ").strip(),
        'keywords': input("Extra Keywords (comma separated): ").strip(),
        'phone': input("Phone Number (last 4+ digits)   : ").strip(),
        'address': input("Street/City Name     : ").strip(),
    }
    return data


# ██████████████████████████████████
# KEYWORD PARSER - split into clean words
# ██████████████████████████████████

def parse_keywords(raw):
    """
    Split keywords on any of: , ; | / \\ - _ + space tab
    Return clean list of unique words (>=2 chars) preserving original case.
    """
    if not raw:
        return []
    parts = re.split(r'[,;|/\\\-_+\s]+', raw)
    kws = []
    seen = set()
    for p in parts:
        p = p.strip()
        if len(p) >= 2 and p.lower() not in seen:
            seen.add(p.lower())
            kws.append(p)
    return kws


# ██████████████████████████████████
# DEEP CASE MUTATIONS
# ██████████████████████████████████

def generate_all_case_variations(word, max_random=6):
    if not word or len(word) < 2:
        return [word] if word else []

    variations = set()
    wl = word.lower()
    wu = word.upper()
    n = len(wl)

    variations.add(wl)
    variations.add(wu)
    variations.add(wl.capitalize())
    variations.add(wl.title())

    for i in range(n):
        t = list(wl); t[i] = t[i].upper(); variations.add(''.join(t))
        t = list(wu); t[i] = t[i].lower(); variations.add(''.join(t))

    if n >= 2:
        t = list(wl); t[0] = t[0].upper(); t[-1] = t[-1].upper()
        variations.add(''.join(t))

    t = list(wl)
    for i in range(1, n, 2): t[i] = t[i].upper()
    variations.add(''.join(t))

    t = list(wl)
    for i in range(0, n, 2): t[i] = t[i].upper()
    variations.add(''.join(t))

    if n >= 4:
        t = list(wl)
        for i in range(1, n - 1): t[i] = t[i].upper()
        variations.add(''.join(t))

        mid = n // 2
        variations.add(wl[:mid].upper() + wl[mid:])
        variations.add(wl[:mid] + wl[mid:].upper())

    if n >= 3:
        for _ in range(max_random):
            t = list(wl)
            for pos in random.sample(range(n), min(2, n)):
                t[pos] = t[pos].upper()
            variations.add(''.join(t))

    if n >= 4:
        for _ in range(3):
            t = list(wl)
            for pos in random.sample(range(n), min(3, n)):
                t[pos] = t[pos].upper()
            variations.add(''.join(t))

    vowels = 'aeiou'
    t = list(wl)
    for i, c in enumerate(t):
        if c in vowels: t[i] = c.upper()
    variations.add(''.join(t))

    t = list(wl)
    for i, c in enumerate(t):
        if c not in vowels: t[i] = c.upper()
    variations.add(''.join(t))

    return list(variations)


# ██████████████████████████████████
# LEET
# ██████████████████████████████████

def generate_leet_variations(word):
    leet_map = {
        'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
        's': ['5', '$'], 't': ['7'], 'l': ['1'], 'b': ['8'],
        'g': ['9'], 'z': ['2'], 'c': ['('], 'd': ['|)'],
    }
    variations = {word}
    wl = word.lower()

    for ch, reps in leet_map.items():
        if ch in wl:
            for r in reps[:2]:
                variations.add(wl.replace(ch, r))
                variations.add(wl.replace(ch, r).capitalize())

    # double
    for ch1, r1 in leet_map.items():
        if ch1 in wl:
            tmp = wl.replace(ch1, r1[0])
            for ch2, r2 in leet_map.items():
                if ch2 != ch1 and ch2 in tmp:
                    variations.add(tmp.replace(ch2, r2[0]))
                    break

    # triple
    if len(wl) >= 5:
        tmp = wl
        cnt = 0
        for ch, reps in leet_map.items():
            if ch in tmp and cnt < 3:
                tmp = tmp.replace(ch, reps[0], 1)
                cnt += 1
        variations.add(tmp)

    return list(variations)


# ██████████████████████████████████
# DATE EXTRACTION
# ██████████████████████████████████

def parse_birthdate_deep(bday_str):
    parts = set()
    if not bday_str:
        return []

    clean = re.sub(r'[-/.,]', ' ', bday_str)
    tokens = [t for t in clean.split() if t.isdigit()]
    full = ''.join(tokens)
    if full and len(full) >= 4:
        parts.add(full)

    for token in tokens:
        parts.add(token)

        if len(token) == 8:
            day, month, year = token[0:2], token[2:4], token[4:8]
            ys = year[2:]
            for combo in [
                day + month, month + day,
                day + year, year + day,
                month + year, year + month,
                day + month + ys, day + month + year,
                month + day + year, year + month + day,
                ys + day + month, year + ys,
                day + month + year[2:],
            ]:
                parts.add(combo)
            for sep in ['', '_', '-', '.', '@', '#']:
                parts.add(f"{day}{sep}{month}{sep}{year}")
                parts.add(f"{day}{sep}{month}{sep}{ys}")
                parts.add(f"{month}{sep}{year}")
                parts.add(f"{day}{sep}{year}")
        elif len(token) == 6:
            month, year = token[0:2], token[2:6]
            ys = year[2:]
            parts.update([month + ys, ys + month, month + year, year + month])
        elif len(token) == 4 and 1900 <= int(token) <= 2100:
            parts.add(token[2:])

    if len(tokens) >= 2:
        d, m = tokens[0], tokens[1]
        if len(d) <= 2 and len(m) <= 2:
            parts.update([d + m, m + d, d + '_' + m, m + '_' + d])

    if len(tokens) >= 3:
        y = tokens[-1]
        if len(y) == 4:
            d, m, ys = tokens[0], tokens[1], y[2:]
            parts.update([
                d + m + y, d + m + ys,
                m + y, d + y,
                y + d + m, ys + d + m,
            ])

    return [p for p in parts if p and len(p) >= 1]


# ██████████████████████████████████
# BASE WORDS
# ██████████████████████████████████

def extract_all_base_words(data):
    all_words = set()
    fields = ['first', 'last', 'nick', 'partner', 'pet', 'company', 'phone', 'address']

    for key in fields:
        val = data.get(key, '').strip()
        if val and len(val) >= 2:
            all_words.add(val)
            all_words.add(val[::-1])
            all_words.add(val.capitalize())
            all_words.add(val.upper())
            if len(val) >= 3:
                all_words.add(val[:3]); all_words.add(val[-3:])
                all_words.add(val[:3].capitalize()); all_words.add(val[-3:].capitalize())
            if len(val) >= 4:
                all_words.add(val[:4]); all_words.add(val[-4:])

    # Birthdate parts (as "date words" not name words)
    all_words.update(parse_birthdate_deep(data.get('bday', '')))
    all_words.update(parse_birthdate_deep(data.get('pbday', '')))

    # Keywords
    for kw in parse_keywords(data.get('keywords', '')):
        all_words.add(kw)
        all_words.add(kw[::-1])
        all_words.add(kw.capitalize())
        all_words.add(kw.upper())
        all_words.add(kw.lower())

    return list(all_words)


# ██████████████████████████████████
# SUFFIXES
# ██████████████████████████████████

def get_extended_suffixes():
    pool = []
    for y in range(1960, 2031):
        pool.append(str(y)); pool.append(str(y)[2:])
    for i in range(0, 1000):
        pool.append(str(i)); pool.append(str(i).zfill(2))
        pool.append(str(i).zfill(3)); pool.append(str(i).zfill(4))

    pool.extend([
        '123', '1234', '12345', '123456', '1234567', '12345678', '123456789',
        '321', '4321', '54321', '654321', '7654321',
        '0000', '00000', '1111', '2222', '3333', '4444', '5555', '6666',
        '7777', '8888', '9999', '112233', '445566', '778899',
        '101010', '121212', '123123', '321321', '456456', '789789',
        '147', '258', '369', '159', '753', '852',
    ])

    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '?', '_', '-', '.', '+', '=', '~', '|', ':']
    pool.extend(symbols)

    for s in symbols[:10]:
        pool.append(s + s)
    pool.extend(['!!!', '@@@', '###', '$$$', '***', '???', '+++', '===', '!@#', '#$%', '_-.', '...', '..'])

    for y in range(1990, 2031):
        for s in ['!', '@', '#', '$', '_', '-', '.', '*', '!@', '@#']:
            pool.append(f"{y}{s}")
            pool.append(f"{s}{y}")
            pool.append(f"{s}{y}{s}")

    for y in range(90, 131):
        for s in ['!', '@', '#', '$', '_']:
            pool.append(f"{s}{y}"); pool.append(f"{y}{s}")

    pool.extend([
        'love', 'life', 'god', 'angel', 'dark', 'light', 'fire', 'king', 'queen',
        'master', 'warrior', 'ninja', 'samurai', 'knight', 'wizard', 'dragon',
        'phoenix', 'lion', 'tiger', 'wolf', 'fox', 'eagle', 'ghost', 'shadow',
        'storm', 'thunder', 'rain', 'snow', 'ice', 'blaze', 'flame',
        'admin', 'root', 'user', 'pass', 'word', 'welcome', 'hello', 'secret',
        'super', 'mega', 'ultra', 'best', 'top', 'pro', 'real', 'true',
        'one', 'two', 'three', 'zero', 'first', 'last',
    ])

    return pool


# ██████████████████████████████████
# MAIN ENGINE
# ██████████████████████████████████

def generate_wordlist(data, filename, target_min=2_000_000):
    print(f"\n[*] Parsing inputs...")

    # --- Separate pools ---
    keywords_raw = parse_keywords(data.get('keywords', ''))
    keywords = []
    for kw in keywords_raw:
        keywords.extend(generate_all_case_variations(kw, max_random=4))
        if len(kw) >= 3:
            keywords.extend(generate_leet_variations(kw))
    keywords = list(set([k for k in keywords if len(k) >= 2]))
    print(f"[+] Keyword variations: {len(keywords):,} (from {len(keywords_raw)} raw keywords)")

    # Names / other fields
    name_pool = set()
    for key in ['first', 'last', 'nick', 'partner', 'pet', 'company', 'address', 'phone']:
        val = data.get(key, '').strip()
        if val and len(val) >= 2:
            name_pool.add(val); name_pool.add(val.capitalize())
            name_pool.add(val.lower()); name_pool.add(val.upper())
            name_pool.add(val[::-1])
            if len(val) >= 3:
                name_pool.add(val[:3]); name_pool.add(val[-3:])
            if len(val) >= 4:
                name_pool.add(val[:4]); name_pool.add(val[-4:])
    name_pool = list(name_pool)

    # Date pool
    date_pool = set()
    date_pool.update(parse_birthdate_deep(data.get('bday', '')))
    date_pool.update(parse_birthdate_deep(data.get('pbday', '')))
    # add years & short
    for y in range(1960, 2031):
        date_pool.add(str(y)); date_pool.add(str(y)[2:])
    date_pool = list(date_pool)
    print(f"[+] Name/field words: {len(name_pool):,}")
    print(f"[+] Date variations : {len(date_pool):,}")

    suffixes = get_extended_suffixes()
    print(f"[+] Suffix pool     : {len(suffixes):,}")

    # --- Open file ---
    f = open(filename, 'w', encoding='utf-8')
    seen = set()
    count = 0

    def add(pwd):
        nonlocal count
        if 8 <= len(pwd) <= 40 and pwd not in seen:
            seen.add(pwd)
            f.write(pwd + '\n')
            count += 1
            if len(seen) > 1_500_000:
                seen.clear()
            return True
        return False

    seps = ['', '_', '-', '.', '@', '#', '!', '$', '*', '+']
    syms = ['!', '@', '#', '$', '%', '^', '&', '*', '?', '_', '-', '.', '+']
    years_full = [str(y) for y in range(1960, 2031)]
    years_short = [str(y)[2:] for y in range(1960, 2031)]

    # ══════════════════════════════════
    # PHASE 1 — Name + Date
    # ══════════════════════════════════
    print("\n[*] PHASE 1: Name + Date ...")
    ns = name_pool[:600] if len(name_pool) > 600 else name_pool
    ds = date_pool[:400] if len(date_pool) > 400 else date_pool
    for i, n in enumerate(ns):
        if count >= target_min * 0.05: break
        for d in ds:
            add(n + d); add(d + n)
            for s in seps[:4]:
                add(f"{n}{s}{d}"); add(f"{d}{s}{n}")
            add(n.capitalize() + d)
            add(n[::-1] + d)
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 2 — Keyword + Date  (المرحلة الأساسية)
    # ══════════════════════════════════
    print("\n[*] PHASE 2: KEYWORD + Date (Core) ...")
    kws_main = keywords[:4000] if len(keywords) > 4000 else keywords
    ds_main  = date_pool[:500] if len(date_pool) > 500 else date_pool

    for i, k in enumerate(kws_main):
        if count >= target_min * 0.20: break
        for d in ds_main:
            add(k + d)
            add(d + k)
            for s in seps[:5]:
                add(f"{k}{s}{d}")
                add(f"{d}{s}{k}")
            # symbol sandwiches
            for s in syms[:4]:
                add(f"{k}{s}{d}{s}")
                add(f"{s}{k}{d}")
            if i % 100 == 0 and count % 20000 < 500:
                print(f"    → {count:,}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 3 — Keyword + Keyword
    # ══════════════════════════════════
    print("\n[*] PHASE 3: KEYWORD × KEYWORD ...")
    kw_pair = keywords[:700] if len(keywords) > 700 else keywords
    for i, k1 in enumerate(kw_pair):
        if count >= target_min * 0.32: break
        for k2 in kw_pair:
            if k1 == k2: continue
            add(k1 + k2)
            add(k1 + '_' + k2)
            add(k1 + '.' + k2)
            add(k1 + '@' + k2)
            add(k1 + '#' + k2)
            add(k1.capitalize() + k2)
            add(k1 + k2.capitalize())
        if i % 100 == 0:
            print(f"    → {count:,}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 4 — Keyword + Name/Field
    # ══════════════════════════════════
    print("\n[*] PHASE 4: KEYWORD + Name/Field ...")
    kws4 = keywords[:1500] if len(keywords) > 1500 else keywords
    ns4  = name_pool[:300] if len(name_pool) > 300 else name_pool
    for i, k in enumerate(kws4):
        if count >= target_min * 0.42: break
        for n in ns4:
            add(k + n)
            add(n + k)
            add(k + '_' + n)
            add(n + '_' + k)
            add(k + '@' + n)
            add(n + '@' + k)
            add(k.capitalize() + n)
            add(n.capitalize() + k)
        if i % 200 == 0:
            print(f"    → {count:,}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 5 — Keyword + Suffix
    # ══════════════════════════════════
    print("\n[*] PHASE 5: KEYWORD + Suffix (numbers/symbols/years) ...")
    kws5 = keywords[:2500] if len(keywords) > 2500 else keywords
    sufs5 = suffixes[:1500]
    for i, k in enumerate(kws5):
        if count >= target_min * 0.55: break
        for s in sufs5:
            add(k + s)
            add(s + k)
        if i % 200 == 0:
            print(f"    → {count:,}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 6 — Keyword + Symbol + Year (killer combo)
    # ══════════════════════════════════
    print("\n[*] PHASE 6: KEYWORD + Symbol + Year (killer combo) ...")
    kws6 = keywords[:1200] if len(keywords) > 1200 else keywords
    for i, k in enumerate(kws6):
        if count >= target_min * 0.65: break
        for y in years_full[:45]:
            for s in syms[:8]:
                add(f"{k}{s}{y}")
                add(f"{k}{y}{s}")
                add(f"{s}{k}{y}")
                add(f"{y}{s}{k}")
                add(f"{k.capitalize()}{s}{y}")
            for ys in years_short[:25]:
                add(k + ys)
                add(k + '@' + ys)
        if i % 100 == 0:
            print(f"    → {count:,}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 7 — Name + Date (deep)
    # ══════════════════════════════════
    print("\n[*] PHASE 7: Name + Symbol + Date (deep) ...")
    for i, n in enumerate(ns):
        if count >= target_min * 0.72: break
        for y in years_full[:40]:
            for s in syms[:6]:
                add(f"{n}{s}{y}")
                add(f"{n}{y}{s}")
                add(f"{s}{n}{y}")
                add(f"{n.capitalize()}{s}{y}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 8 — Triple: Keyword + Name + Date
    # ══════════════════════════════════
    print("\n[*] PHASE 8: Triple (Keyword + Name + Date) ...")
    for _ in range(120000):
        if count >= target_min * 0.80: break
        k = random.choice(keywords) if keywords else random.choice(name_pool)
        n = random.choice(name_pool) if name_pool else k
        d = random.choice(date_pool) if date_pool else str(random.randint(1900, 2030))
        s = random.choice(syms)
        add(f"{k}{n}{d}")
        add(f"{k}_{n}_{d}")
        add(f"{k}{s}{n}{d}")
        add(f"{n}{k}{d}")
        add(f"{k}{d}{s}{n}")
        add(f"{k.capitalize()}_{n}_{d}{s}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 9 — Keyword + Keyword + Date
    # ══════════════════════════════════
    print("\n[*] PHASE 9: Keyword + Keyword + Date ...")
    for _ in range(120000):
        if count >= target_min * 0.88: break
        k1 = random.choice(keywords) if keywords else 'user'
        k2 = random.choice(keywords) if keywords else 'pass'
        d  = random.choice(date_pool) if date_pool else str(random.randint(1900, 2030))
        s  = random.choice(syms)
        add(f"{k1}{k2}{d}")
        add(f"{k1}_{k2}_{d}")
        add(f"{k1}{s}{k2}{d}")
        add(f"{d}{s}{k1}{k2}")
        add(f"{k1}{k2}{s}{d}")
        add(f"{k1.capitalize()}{k2.capitalize()}{d}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 10 — Four-part madness
    # ══════════════════════════════════
    print("\n[*] PHASE 10: Four-part combinations ...")
    for _ in range(100000):
        if count >= target_min * 0.95: break
        k = random.choice(keywords) if keywords else 'user'
        n = random.choice(name_pool) if name_pool else 'name'
        d = random.choice(date_pool) if date_pool else '2000'
        s = random.choice(syms)
        add(f"{k}{s}{n}{s}{d}")
        add(f"{n}_{k}_{d}{s}")
        add(f"{k}{d}{n}{s}")
        add(f"{s}{k}{n}{d}")
        add(f"{k.capitalize()}{n.capitalize()}_{d}{s}")
    print(f"    → {count:,}")

    # ══════════════════════════════════
    # PHASE 11 — Fill to target
    # ══════════════════════════════════
    print("\n[*] PHASE 11: Fill to target ...")
    fill = 0
    while count < target_min:
        k = random.choice(keywords) if keywords else 'user'
        n = random.choice(name_pool) if name_pool else 'name'
        d = random.choice(date_pool) if date_pool else str(random.randint(1900, 2030))
        s = random.choice(syms)
        suf = random.choice(suffixes[:800])
        add(k + d)
        add(k + s + d)
        add(k + suf)
        add(k + s + suf)
        add(n + k + d)
        add(k + n + s + d)
        add(s + k + d + s)
        add(k.capitalize() + '_' + n + '_' + d + s)
        add(k[::-1] + d + s)
        add(k + s + d + suf)
        fill += 1
        if fill % 20000 == 0:
            print(f"    → {count:,}")
    print(f"    → {count:,}")

    f.close()
    return count


# ██████████████████████████████████
# MAIN
# ██████████████████████████████████

def main():
    banner()

    print("\n[!] WARNING: For AUTHORIZED security testing only!")

    data = get_user_data()

    # fallback defaults
    if not any([data['first'], data['last'], data['nick'], data['keywords']]):
        print("\n[!] No inputs detected. Adding defaults...")
        data['first'] = 'admin'
        data['keywords'] = 'admin, password, welcome, love, life, god, master'

    target = 2_000_000   # ← عدّلها لو عايز 1M أو 3M
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"DiaaSuperCUPP_v5_{target//1_000_000}M_{timestamp}.txt"

    print("\n" + "=" * 70)
    print(f"   STARTING GENERATION — Target: {target:,}")
    print("=" * 70)

    import time
    t0 = time.time()
    total = generate_wordlist(data, filename, target_min=target)
    el = time.time() - t0

    print("\n" + "=" * 70)
    print(f"   ✓ SUCCESS: {total:,} passwords")
    print(f"   ✓ Time : {el/60:.1f} minutes")
    print(f"   ✓ Speed: {total/el:.0f} pwd/s")
    print(f"   ✓ Size : {os.path.getsize(filename)/1024/1024:.1f} MB")
    print(f"   ✓ File : {filename}")
    print("=" * 70)

    if input("\n[?] Show 25 random samples? (y/n): ").strip().lower() == 'y':
        with open(filename, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
        for i, s in enumerate(random.sample(lines, min(25, len(lines))), 1):
            print(f"   {i:2d}. {s.strip()}")


if __name__ == "__main__":
    main()
