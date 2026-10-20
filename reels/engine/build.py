"""Darsify reel builder: spec JSON -> reel.html + events.json (for audio).
Usage: python3 build.py specs/RL-01.json out/RL-01
"""
import json, re, sys, pathlib, html as H
ENG = pathlib.Path(__file__).resolve().parent
A = ENG / 'assets'
INK, ROYAL, SKY, ORANGE, DEEP, WHITE, PINK, GREEN, RED = '#0b1e30', '#2655a3', '#5e8bc8', '#f26229', '#cb4627', '#ffffff', '#e0567f', '#22a06b', '#e5484d'
uri = lambda p: p.as_uri()

ICONS = {
 'link': '<path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
 'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
 'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 'check': '<path d="M5 12l5 5 9-10"/>',
 'doc': '<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h8M9 17h6"/>',
 'wallet': '<path d="M3 7h16a2 2 0 0 1 2 2v10H5a2 2 0 0 1-2-2z"/><path d="M3 7l12-4v4M16 13h2"/>',
 'users': '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M17 4a4 4 0 0 1 0 8M22 21a6 6 0 0 0-4-6"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'school': '<path d="M2 10l10-6 10 6-10 6z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
 'building': '<path d="M4 21V5l8-3 8 3v16M2 21h20M9 21v-4h6v4M8 8h2M14 8h2M8 12h2M14 12h2"/>',
 'person': '<circle cx="12" cy="7" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 'ai': '<path d="M12 3l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/><path d="M19 15l1 2 2 1-2 1-1 2-1-2-2-1 2-1z"/>',
 'chat': '<path d="M4 4h16v12H8l-4 4z"/>',
 'exam': '<path d="M5 3h14v18H5z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
 'repeat': '<path d="M4 12a8 8 0 0 1 14-5l2 2M20 12a8 8 0 0 1-14 5l-2-2"/><path d="M20 4v5h-5M4 20v-5h5"/>',
 'cart': '<path d="M3 4h2l2 12h11l2-8H7"/><circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/>',
 'bus': '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 21v-3M16 21v-3"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 'star': '<path d="M12 3l3 6 6 1-4.5 4 1 6-5.5-3-5.5 3 1-6L3 10l6-1z"/>',
 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
}
def icon(name, size=56, color=WHITE, sw=2):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, ICONS["star"])}</svg>'
TICK = '<svg width="38" height="38" viewBox="0 0 40 40"><path d="M7 21l9 9 17-19" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>'

def svg_mascot(name, w):
    s = (A / 'mascots' / f'{name}.svg').read_text()
    s = re.sub(r'<title>.*?</title>', '', s); s = re.sub(r'\bid="(\w+)"', r'class="\1"', s)
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    return s.replace('width="278" height="294"', f'width="{w}" height="{round(w*294/278)}" style="overflow:visible;display:block"')

class B:
    """Collects markup + audio events for one scene; times relative to scene start."""
    def __init__(s, spec): s.h=[]; s.hud=[]; s.ev=[]; s.spec=spec; s.ar=spec.get('lang')=='ar'; s.sc={}
    def add(s, x): s.h.append(x)
    def e(s, t, kind, **kw): s.ev.append(dict(t=round(t,3), k=kind, **kw))

def esc(x): return H.escape(str(x))
def acc_words(text, accent):
    """split a line into word spans; *word* or *several words* -> accent colour"""
    out = []; on = False
    for w in text.split(' '):
        st = w.startswith('*'); en = w.endswith('*') and len(w) > 1
        if st: on = True
        out.append((w.strip('*'), on))
        if en: on = False
    return out

def head(b, lines, t0=.15, y=300, size=150, step=.1, color=WHITE, accent=None, align='start', a='up', sound=True, maxw=920, weight=800, lh=1.0):
    accent = accent or b.spec['_accent']
    ar0 = b.ar
    if b.sc.get('en'): b.ar = False
    try: return _head(b, lines, t0, y, size, step, color, accent, align, a, sound, maxw, weight, lh)
    finally: b.ar = ar0
def _head(b, lines, t0, y, size, step, color, accent, align, a, sound, maxw, weight, lh):
    fam = 'A' if b.ar else 'M'
    style = f'top:{y}px;left:80px;right:80px;text-align:{"right" if b.ar and align=="start" else align};font-family:{fam};font-weight:{weight};font-size:{size}px;line-height:{lh};color:{color};' + ('' if b.ar else 'text-transform:uppercase;letter-spacing:-.01em;')
    hz = b.sc.get('headz')
    if hz: style += f'transform:translateZ({hz}px);'
    b.add(f'<div class="abs" style="{style}" {"dir=rtl" if b.ar else ""}>')
    k = 0
    for ln in lines:
        b.add(f'<div class="line" data-fit="{maxw}">')
        for w, isacc in acc_words(ln, accent):
            b.add(f'<span class="w" data-in="{t0+k*step:.2f}" data-a="{a}" style="display:inline-block;{"color:"+accent+";" if isacc else ""}">{esc(w)}</span> ')
            if sound and k < 8: b.e(t0+k*step, 'word')
            k += 1
        b.add('</div>')
    b.add('</div>')
    return t0 + k*step

def text(b, s, t, y, size=46, color=WHITE, weight=400, a='up', x=80, w=920, align=None, extra=''):
    fam = 'A' if b.ar else 'M'; al = align or ('right' if b.ar else 'left')
    b.add(f'<div class="abs" data-in="{t}" data-a="{a}" style="left:{x}px;width:{w}px;top:{y}px;font-family:{fam};font-size:{size}px;font-weight:{weight};color:{color};line-height:1.3;text-align:{al};{extra}" {"dir=rtl" if b.ar else ""}>{s}</div>')

def mascot(b, who, ex, x, y, w=300, t=0.2, hop=None, jump=None, shake=None, out=None, ph=0, bubble=None, z=None, talk=None):
    exs = sorted(set(e for _, e in ex))
    lay = ''.join(f'<div class="ex" data-e="{e}" style="position:absolute;inset:0;opacity:0">{svg_mascot(f"{who}-{e}", w)}</div>' for e in exs)
    attrs = f'data-in="{t}" data-ex=\'{json.dumps(ex)}\' data-ph="{ph}"'
    if hop is not None: attrs += f' data-hop="{hop}"'
    if jump: attrs += f' data-jump="{",".join(map(str,jump))}"'
    if shake is not None: attrs += f' data-shake="{shake}"'
    if out is not None: attrs += f' data-out="{out}"'
    if z: attrs += f' data-z="{z}"'
    if talk: attrs += f' data-talk="{"|".join(f"{a:.2f}:{c:.2f}" for a, c in talk)}"'
    b.add(f'<div class="masc" {attrs} style="left:{x}px;top:{y}px;width:{w}px;height:{round(w*294/278)}px">{lay}</div>')
    b.e(t+.1, 'whoosh_s')
    if jump:
        for j in jump: b.e(j, 'boing')
    if bubble:
        bx, by = bubble.get('x', x + w - 40), bubble.get('y', y - 90)
        side = bubble.get('side', 'l')
        b.add(f'<div class="bub {"r" if side=="r" else ""}" data-in="{bubble["t"]}" data-a="pop" data-base="" style="left:{bx}px;top:{by}px;{"font-family:A;" if b.ar else ""}" {"dir=rtl" if b.ar else ""}>{esc(bubble["text"])}</div>')
        b.e(bubble['t'], 'pop')

def mascots_default(b, sc, base_y=1240):
    for m in sc.get('mascots', []):
        mascot(b, m['who'], m.get('ex', [[0, 'happy']]), m.get('x', 390), m.get('y', base_y), m.get('w', 300), m.get('t', .2),
               m.get('hop'), m.get('jump'), m.get('shake'), m.get('out'), m.get('ph', 0), m.get('bubble'), m.get('z'))

# ---------------- scene types ----------------
def sc_hook(b, sc):
    y = sc.get('y', 330)
    if sc.get('kicker'):
        text(b, esc(sc['kicker']), .05, y - 90, size=sc.get('ksize', 62), weight=300, extra='letter-spacing:.06em;' + ('' if b.ar else 'text-transform:uppercase;'))
    end = head(b, sc['head'], t0=sc.get('t0', .2), y=y, size=sc.get('size', 150), step=sc.get('step', .12), color=sc.get('color', WHITE), accent=sc.get('accent'))
    if sc.get('sub'):
        text(b, esc(sc['sub']), sc.get('subt', end + .2), sc.get('suby', y + 160 * len(sc['head']) + 40), size=sc.get('subsize', 50), weight=400, color='rgba(255,255,255,.92)')
        b.e(sc.get('subt', end + .2), 'soft')
    if sc.get('stamp'):
        st = sc['stamp']; b.add(f'<div class="stampT" data-in="{st["t"]}" data-a="stamp" data-rot="{st.get("rot",-10)}" style="left:{st.get("x",250)}px;top:{st.get("y",900)}px;border-color:{st.get("c",ORANGE)};color:{st.get("c",ORANGE)};{"font-family:A;" if b.ar else ""}">{esc(st["text"])}</div>')
        b.e(st['t'], 'stamp')
    for c in sc.get('chips', []):
        b.add(f'<div class="chipT" data-in="{c["t"]}" data-a="pop" data-float="{c.get("f",8)}" data-ph="{c.get("ph",0)}" style="left:{c["x"]}px;top:{c["y"]}px;{"background:"+c["bg"]+";border-color:"+c["bg"]+";" if c.get("bg") else ""}{"font-family:A;" if b.ar else ""}">{esc(c["text"])}</div>')
        b.e(c['t'], 'pop')
    mascots_default(b, sc)

def sc_chat(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 96), step=.08)
    top = sc.get('py', 560); ph = sc.get('ph', 760)
    name = esc(sc.get('name', 'Group A · Parents')); sub = esc(sc.get('status', 'online'))
    b.add(f'<div class="phone" style="top:{top}px;height:{ph}px"><div class="phead"><div class="pav">{esc(sc.get("av","P"))}</div><div><div class="pname">{name}</div><div class="pst">{sub}</div></div>'
          + (f'<div class="badge" data-in="{sc["msgs"][0]["t"]}" data-a="pop"><span data-count="{sc["msgs"][0]["t"]},{sc["msgs"][-1]["t"]},1,{sc["unread"] if type(sc.get("unread")) is int and sc.get("unread") is not True else len(sc["msgs"])}" data-fmt="{{}}">1</span></div>' if sc.get('unread') else '')
          + '</div><div class="pbody">')
    # messages stack from top; later ones push earlier ones up (pre-computed offsets)
    msgs = sc['msgs']; yy = 30; pos = []
    for m in msgs:
        lines = max(1, len(m['text']) // 26 + 1)
        hgt = 40 + lines * 50
        pos.append((yy, hgt)); yy += hgt + 22
    body_h = ph - 130
    for i, m in enumerate(msgs):
        y0, hgt = pos[i]
        side = 'me' if m.get('me') else 'them'
        b.add(f'<div class="msg {side}" data-in="{m["t"]}" data-a="pop" style="top:{y0}px;{"font-family:A;direction:rtl;" if b.ar else ""}">{esc(m["text"])}<span class="mt">{esc(m.get("time",""))}</span></div>')
        b.e(m['t'], 'msg_me' if m.get('me') else 'msg')
    b.add('</div></div>')
    # scroll: shift pbody when overflow
    over = max(0, yy - body_h)
    if over > 0:
        b.add(f'<style>#S{b.idx} .pbody{{}}</style>')
        b.spec.setdefault('_scroll', {})[b.idx] = (msgs[-1]['t'] - .6, over)
    mascots_default(b, sc, 1350)

def sc_list(b, sc):
    end = head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 110), step=.08)
    y = sc.get('ly', 280 + 125 * len(sc['head']) + 60); gap = sc.get('gap', 210)
    for i, it in enumerate(sc['items']):
        t = it.get('t', end + .3 + i * sc.get('istep', .9))
        badge = f'<div class="num">{i+1}</div>' if not it.get('icon') else f'<div class="num ic">{icon(it["icon"], 54)}</div>'
        b.add(f'<div class="lcard" data-in="{t}" data-a="{"right" if b.ar else "left"}" style="top:{y+i*gap}px;{"direction:rtl;font-family:A;" if b.ar else ""}">{badge}<div><div class="lt">{esc(it["title"])}</div>' + (f'<div class="ld">{esc(it["desc"])}</div>' if it.get('desc') else '') + '</div></div>')
        b.e(t, 'card')
    mascots_default(b, sc, 1300)

def panel_rows(b, blocks):
    out = []
    for bl in blocks:
        if 'row' in bl:
            r = bl['row']; chip = ''
            if r.get('chip'):
                if r.get('to'):
                    chip = f'<span class="chipS {r["chip"]}" data-swap="{r["at"]}" data-swapcls="{r["chip"]}|{r["to"]}"><span class="sa">{esc(r["ctext"])}</span><span class="sb">{esc(r["totext"])}</span></span>'
                    b.e(r['at'], 'ding_s')
                else:
                    chip = f'<span class="chipS {r["chip"]}">{esc(r["ctext"])}</span>'
            tk = ''
            if r.get('tick') is not None:
                tk = f'<span class="cb" data-tick="{r["tick"]}" data-fill="{GREEN}">{TICK}</span>'; b.e(r['tick'], 'pen')
            ins = f' data-in="{r["in"]}" data-a="up"' if r.get('in') is not None else ''
            if r.get('in') is not None: b.e(r['in'], 'pop_s')
            out.append(f'<div class="trow"{ins}><span style="flex:1;font-weight:700">{esc(r["l"])}</span>' + (f'<span class="muted" style="width:{r.get("mw",230)}px">{esc(r["m"])}</span>' if r.get('m') else '') + chip + tk + '</div>')
        elif 'bar' in bl:
            r = bl['bar']
            out.append(f'<div style="display:flex;align-items:center;gap:20px;margin:16px 0"><span class="muted" style="width:{r.get("lw",260)}px">{esc(r["l"])}</span><div class="track"><div class="fillb" data-bar="{r["at"]},{r.get("d",.7)},{r["w"]}" style="background:{r.get("c",SKY)}"></div></div><span style="width:110px;text-align:right;font-weight:700;font-size:30px">{esc(r["v"])}</span></div>')
            b.e(r['at'], 'rise')
        elif 'btn' in bl:
            r = bl['btn']
            out.append(f'<div style="position:relative;display:flex;justify-content:flex-end;margin-top:24px"><span class="btnS" data-press="{r["at"]}">{esc(r["label"])}</span>'
                       + (f'<div class="toast" data-in="{r["at"]+.25}" data-a="up">✓ {esc(r["toast"])}</div>' if r.get('toast') else '') + '</div>')
            b.e(r['at'], 'click'); b.e(r['at'] + .25, 'success')
        elif 'type' in bl:
            r = bl['type']
            out.append(f'<div class="muted lbl">{esc(r.get("label","YOUR MESSAGE"))}</div><div class="inp"><span data-type="{r["t0"]},{r["t1"]}" data-text="{esc(r["text"])}"></span><span class="caret">|</span></div>')
            b.e(r['t0'], 'type', t1=r['t1'])
        elif 'note' in bl:
            out.append(f'<div class="muted" style="margin-top:16px">{bl["note"]}</div>')
        elif 'big' in bl:
            r = bl['big']
            out.append(f'<div style="display:flex;align-items:baseline;gap:18px;margin:6px 0 10px"><span style="font-size:96px;font-weight:800" data-count="{r["t0"]},{r["t1"]},{r["from"]},{r["to"]}" data-fmt="{esc(r.get("fmt","{}"))}">{r["from"]}</span><span class="muted">{esc(r["l"])}</span></div>')
            b.e(r['t0'], 'count', t1=r['t1'])
        elif 'chips' in bl:
            out.append('<div style="display:flex;gap:14px;flex-wrap:wrap;margin:14px 0">' + ''.join(f'<span class="chipS {c.get("k","sel")}">{esc(c["text"])}</span>' for c in bl['chips']) + '</div>')
        elif 'hr' in bl:
            out.append('<div style="height:2px;background:rgba(255,255,255,.07);margin:14px 0"></div>')
    return ''.join(out)

def sc_ui(b, sc):
    end = .1
    if sc.get('head'): end = head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08)
    p = sc['panel']; mark = uri(A / 'logos' / 'darsify-mark-white.svg')
    cards = ''
    for c in p.get('cards', [p]):
        cards += f'<div class="pcard" style="margin-top:22px{";"+c["style"] if c.get("style") else ""}">' + (f'<div style="font-size:36px;font-weight:700;margin-bottom:8px">{esc(c["ctitle"])}</div>' if c.get('ctitle') else '') + panel_rows(b, c.get('blocks', [])) + '</div>'
    stamp = ''
    if p.get('stamp'):
        st = p['stamp']; stamp = f'<div class="stampT" data-in="{st["t"]}" data-a="stamp" data-rot="-12" style="left:{st.get("x",420)}px;top:{st.get("y",300)}px;border-color:{GREEN};color:{GREEN};background:rgba(255,255,255,.96);font-size:54px">{esc(st["text"])}</div>'
        b.e(st['t'], 'stamp')
    b.add(f'<div class="pnl" style="top:{sc.get("py",600)}px;{"transform:translateZ(%spx);" % sc["pz"] if sc.get("pz") else ""}"><div class="pbar"><img src="{mark}" style="width:34px"><span class="crumb">{esc(p.get("crumb","Darsify"))}</span><span class="pnew">+ New</span></div>'
          f'<div style="padding:34px 44px 40px;position:relative"><div class="ptitle">{esc(p["title"])}</div>' + (f'<div class="psub">{esc(p["sub"])}</div>' if p.get('sub') else '') + cards + stamp + '</div></div>')
    mascots_default(b, sc, 1380)

def sc_split(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08)
    ly = sc.get('ly', 560)
    L, R = sc['left'], sc['right']
    lx, rx = (560, 70) if b.ar else (70, 560)
    b.add(f'<div class="col" style="left:{lx}px;top:{ly}px;background:rgba(0,0,0,.28)" data-in="{L.get("t",.4)}" data-a="up"><div class="ch" style="color:#ffb59a;{"font-family:A;" if b.ar else ""}">{esc(L["title"])}</div></div>')
    b.add(f'<div class="col" style="left:{rx}px;top:{ly}px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.25)" data-in="{R.get("t",.6)}" data-a="up"><div class="ch" style="{"font-family:A;" if b.ar else ""}">{esc(R["title"])}</div></div>')
    b.e(L.get('t', .4), 'card'); b.e(R.get('t', .6), 'card')
    for i, it in enumerate(L['items']):
        t = it['t']; y = ly + 130 + i * 140
        b.add(f'<div class="sitem" data-in="{t}" data-a="up" style="left:{lx+30}px;top:{y}px;{"font-family:A;direction:rtl;" if b.ar else ""}"><span class="sx">{icon("x",30,"#ffb59a",3)}</span><span class="stx" data-strike="{it.get("strike",99)}">{esc(it["text"])}</span></div>')
        b.e(t, 'pop_s')
        if it.get('strike') is not None and it['strike'] < 90: b.e(it['strike'], 'pen')
    for i, it in enumerate(R['items']):
        t = it['t']; y = ly + 130 + i * 140
        b.add(f'<div class="sitem" style="left:{rx+30}px;top:{y}px;{"font-family:A;direction:rtl;" if b.ar else ""}" data-in="{t}" data-a="up"><span class="cb" data-tick="{t+.1}" data-fill="{GREEN}" style="width:44px;height:44px;flex:none">{TICK}</span><span>{esc(it["text"])}</span></div>')
        b.e(t, 'pen')
    mascots_default(b, sc, 1420)

def sc_counter(b, sc):
    if sc.get('kicker'): text(b, esc(sc['kicker']), .05, sc.get('y', 420) - 100, size=60, weight=300, extra='letter-spacing:.06em;text-transform:uppercase;', align='center')
    fam = 'A' if b.ar else 'M'
    b.add(f'<div class="abs" data-in="{sc.get("t0",.2)}" data-a="zoom" style="left:0;right:0;top:{sc.get("y",420)}px;text-align:center;font-family:M;font-weight:800;font-size:{sc.get("nsize",330)}px;line-height:1;color:{sc.get("ncolor",WHITE)}"><span data-count="{sc.get("t0",.2)},{sc.get("t1",1.6)},{sc["from"]},{sc["to"]}" data-fmt="{esc(sc.get("fmt","{}"))}">{sc["from"]}</span></div>')
    b.e(sc.get('t0', .2), 'count', t1=sc.get('t1', 1.6)); b.e(sc.get('t1', 1.6), 'stamp')
    if sc.get('label'):
        b.add(f'<div class="abs" data-in="{sc.get("t1",1.6)+.1}" data-a="up" style="left:80px;right:80px;top:{sc.get("y",420)+sc.get("nsize",330)+30}px;text-align:center;font-family:{fam};font-weight:800;font-size:{sc.get("lsize",76)}px;line-height:1.1;{"" if b.ar else "text-transform:uppercase;"}" {"dir=rtl" if b.ar else ""}>{sc["label"]}</div>')
    if sc.get('sub'):
        text(b, esc(sc['sub']), sc.get('t1', 1.6) + .6, sc.get('y', 420) + sc.get('nsize', 330) + 230, size=46, align='center')
    mascots_default(b, sc, 1300)

def sc_chips(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 300), size=sc.get('size', 110), step=.09)
    merge = sc.get('merge')
    for i, c in enumerate(sc['chips']):
        out = f' data-out="{merge+i*.03}" data-outa="shrink"' if merge else ''
        b.add(f'<div class="chipT" data-in="{c["t"]}" data-a="pop" data-float="{c.get("f",10)}" data-ph="{i*1.3}"{out} style="left:{c["x"]}px;top:{c["y"]}px;{"background:"+c["bg"]+";border-color:"+c["bg"]+";" if c.get("bg") else ""}{"font-family:A;" if b.ar else ""}">' + (icon(c['icon'], 40) + '&nbsp;&nbsp;' if c.get('icon') else '') + f'{esc(c["text"])}</div>')
        b.e(c['t'], 'pop')
    if merge:
        wm = uri(A / 'logos' / 'darsify-wordmark-navy.svg')
        b.add(f'<div class="dcard" data-in="{merge+.25}" data-a="pop" style="left:290px;top:{sc.get("my",880)}px"><img src="{wm}" style="width:400px"></div>')
        b.e(merge, 'whoosh'); b.e(merge + .25, 'sparkle')
        if sc.get('mtext'):
            text(b, esc(sc['mtext']), merge + .6, sc.get('my', 880) + 230, size=60, weight=800, align='center', extra='' if b.ar else 'text-transform:uppercase;')
    mascots_default(b, sc, 1320)

def sc_paper(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08)
    for i, p in enumerate(sc['papers']):
        x = 170 + (i % 3) * 30 + (i * 37) % 120; y = sc.get('py', 640) + i * 34; rot = [-8, 6, -3, 9, -6, 4, -10][i % 7]
        out = f' data-out="{sc["fly"]+i*.05}" data-outa="up"' if sc.get('fly') else ''
        b.add(f'<div class="paper" data-in="{p["t"]}" data-a="drop" data-rot="{rot}"{out} style="left:{x}px;top:{y}px"><div class="ptit">{esc(p["text"])}</div><div class="pl"></div><div class="pl" style="width:70%"></div><div class="pl"></div><div class="pl" style="width:55%"></div></div>')
        b.e(p['t'] + .5, 'thump')
    if sc.get('fly'): b.e(sc['fly'], 'whoosh')
    if sc.get('stamp'):
        st = sc['stamp']; b.add(f'<div class="stampT" data-in="{st["t"]}" data-a="stamp" style="left:{st.get("x",230)}px;top:{st.get("y",1000)}px;border-color:{st.get("c",ORANGE)};color:{st.get("c",ORANGE)};background:rgba(255,255,255,.96);{"font-family:A;" if b.ar else ""}">{esc(st["text"])}</div>')
        b.e(st['t'], 'stamp')
    mascots_default(b, sc, 1420)

def sc_exam(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 260), size=sc.get('size', 100), step=.08)
    ey = sc.get('ey', 640)
    tabs = ''.join(f'<span class="etab {"on" if i==sc.get("on",0) else ""}">{esc(x)}</span>' for i, x in enumerate(sc.get('tabs', [])))
    if tabs: b.add(f'<div class="etabs" data-in=".3" data-a="up" style="top:{ey-110}px">{tabs}</div>')
    ch = ''.join(f'<div class="ech" ' + (f'data-swap="{sc["pick_at"]}" data-swapcls="o|o sel"' if i == sc.get('pick') else '') + f'><span class="el">{"ABCD"[i]}</span><span>{esc(c)}</span></div>' for i, c in enumerate(sc['choices']))
    rtl = 'direction:rtl;font-family:A;' if sc.get('rtl') else ''
    b.add(f'<div class="exam" data-in=".35" data-a="up" style="top:{ey}px;{rtl}"><div class="ehead"><div><div class="esec">{esc(sc.get("section","Reading and Writing"))}</div><div class="edir">Directions ⌄</div></div>'
          f'<div class="etime" data-count="{sc.get("c0",.4)},{sc.get("c1",4)},{sc.get("tfrom",1908)},{sc.get("tto",1904)}" data-fmt="{{}}" data-clock="1">31:48</div><div class="etools">⋯</div></div>'
          f'<div class="ebody"><div class="eq">{esc(sc["q"])}</div>{ch}</div><div class="efoot"><span class="enav">Question {sc.get("qn","1 of 27")}</span><span class="enext" data-press="{sc.get("next_at",99)}">Next</span></div></div>')
    if sc.get('pick') is not None: b.e(sc['pick_at'], 'click')
    if sc.get('stamp'):
        st = sc['stamp']; b.add(f'<div class="stampT" data-in="{st["t"]}" data-a="stamp" style="left:{st.get("x",300)}px;top:{st.get("y",ey+420)}px;border-color:{GREEN};color:{GREEN};background:rgba(255,255,255,.97)">{esc(st["text"])}</div>')
        b.e(st['t'], 'stamp')
    mascots_default(b, sc, 1420)

def sc_timeline(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08)
    y = sc.get('ly', 600); gap = sc.get('gap', 150)
    b.add(f'<div class="abs" style="left:250px;top:{y}px;width:4px;height:{gap*len(sc["rows"])-40}px;background:rgba(255,255,255,.25)"></div>')
    for i, r in enumerate(sc['rows']):
        t = r['t']
        b.add(f'<div class="trw" data-in="{t}" data-a="left" style="top:{y+i*gap}px;{"direction:rtl;font-family:A;" if b.ar else ""}"><span class="ttime">{esc(r["time"])}</span><span class="tdot" style="background:{r.get("c",ORANGE)}"></span><span class="ttxt stx" data-strike="{r.get("strike",99)}">{esc(r["text"])}</span>' + (f'<span class="tag">{esc(r["tag"])}</span>' if r.get('tag') else '') + '</div>')
        b.e(t, 'pop_s')
        if r.get('strike', 99) < 90: b.e(r['strike'], 'pen')
    mascots_default(b, sc, 1420)

def sc_tiles(b, sc):
    end = head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08)
    y = sc.get('ty', 640); gap = sc.get('gap', 290)
    for i, tl in enumerate(sc['tiles']):
        t = tl.get('t', end + .3 + i * .8)
        b.add(f'<div class="tile" data-in="{t}" data-a="up" style="top:{y+i*gap}px;{"direction:rtl;font-family:A;" if b.ar else ""}"><div class="tic" style="background:{tl.get("c",ORANGE)}">{icon(tl.get("icon","star"),64)}</div><div><div class="tt">{esc(tl["title"])}</div><div class="td">{esc(tl["desc"])}</div></div></div>')
        b.e(t, 'card')
    mascots_default(b, sc, 1450)

def sc_end(b, sc):
    ar = b.ar
    wm = uri(A / 'logos' / 'darsify-wordmark-navy.svg')
    b.add('<div class="abs" style="inset:0;background:#eef3f8"></div>')
    for i, w in enumerate(sc.get('words', [])):
        pos = [[110, 330], [640, 300], [80, 760], [690, 800], [150, 1030], [620, 1060]][i % 6]
        b.add(f'<div class="ec" data-in="{.05+i*.05}" data-a="pop" data-out="{.75+i*.05}" data-outa="shrink" style="left:{pos[0]}px;top:{pos[1]}px;{"font-family:A;" if ar else ""}">{esc(w)}</div>')
    b.add(f'<div class="dcard" data-in="1.0" data-a="pop" style="left:290px;top:420px"><img src="{wm}" style="width:400px"></div>')
    # brand rule: the slogan is always English, never translated
    l1, l2 = sc.get('l1', 'TEACH MORE.'), sc.get('l2', 'CHASE LESS.')
    fam = 'A' if ar else 'M'
    b.add(f'<div class="abs" data-in="1.35" data-a="up" style="left:0;right:0;top:700px;text-align:center;font-family:M;font-weight:800;font-size:112px;line-height:1.05;color:{INK}">{esc(l1)}<br><span style="color:{ORANGE}">{esc(l2)}</span></div>')
    join = sc.get('join', 'انضم لينا دلوقتي على <b>Darsify.net</b>' if ar else 'Join us now at <b>Darsify.net</b>')
    b.add(f'<div class="abs" data-in="1.75" data-a="up" style="left:0;right:0;top:960px;text-align:center;font-family:{fam};font-size:50px;color:{INK}" {"dir=rtl" if ar else ""}>{join}</div>')
    b.add(f'<div class="btnJ" data-in="2.0" data-a="pop" style="{"font-family:A;" if ar else ""}">{esc(sc.get("btn","انضم لينا" if ar else "JOIN US"))}</div>')
    b.add(f'<div class="abs" data-in="2.2" data-a="fade" style="left:0;right:0;top:1210px;text-align:center;font-size:34px;color:{ROYAL};font-weight:700">#WeplanYouteach</div>')
    for k, (who, x) in enumerate([('dars', 170), ('ustaz', 400), ('dara', 650)]):
        mascot(b, who, [[0, 'happy'], [2.6 + k * .12, 'celebrate']], x, 1290, 260 if who != 'ustaz' else 280, 2.25 + k * .12, hop=2.6 + k * .12, ph=k)
    b.e(.05, 'whoosh'); b.e(1.0, 'sparkle'); b.e(1.35, 'thump'); b.e(1.75, 'pop'); b.e(2.0, 'pop_hi')


# ---------------- v2: story (classroom dialogue), ring (3D carousel), flip card ----------------
SHOTS = {'wide': (540, 960, 1.0, 0, 0), 'class': (540, 1020, 1.08, 0, 0),
         'dars': (310, 1250, 1.3, 6, 0), 'dara': (790, 1250, 1.3, -6, 0), 'students': (540, 1320, 1.15, 0, -2),
         'ustaz': (700, 690, 1.34, -7, 2), 'board': (395, 590, 1.42, 5, 3), 'boardwide': (540, 640, 1.18, 0, 2)}
VOICE = {'ustaz': 0, 'dars': 1, 'dara': 2}

def bubble_html(b, who, text, t, t_out, pos):
    side = pos.get('side', 'l'); fam = 'font-family:A;' if b.ar else ''
    anchor = f'left:{pos["x"]}px;' if side == 'l' else f'right:{1080 - pos["x"]}px;'
    tt = t + .12; t1 = tt + max(.35, len(text) * .032)
    return (f'<div class="sbub {side} {who}" data-in="{t}" data-a="pop" data-base="translateZ(60px) translateY(-100%)" data-out="{t_out}" data-outa="shrink" style="{anchor}top:{pos["y"]}px;{fam}" {"dir=rtl" if b.ar else ""}>'
            f'<span class="ghost">{esc(text)}</span><span class="typed" data-type="{tt:.2f},{t1:.2f}" data-text="{esc(text)}"></span></div>'), t1

def sc_story(b, sc):
    ar = b.ar; fam = 'font-family:A;' if ar else ''
    # --- set: floor, board, clock, desks (world space; camera moves through it) ---
    b.add('<div class="abs floor"></div>')
    b.add('<div class="abs wallline"></div>')
    mark = uri(A / 'logos' / 'darsify-mark-white.svg')
    b.add(f'<div class="board" style="transform:translateZ(-30px)"><img src="{mark}" class="bmark"><div class="btitle" style="{fam}">{esc(sc.get("boardtitle", ""))}</div>')
    for it in sc.get('board', []):
        t = it['t']
        if 'write' in it:
            t1 = t + it.get('dur', max(.4, len(it['write']) * .045))
            b.add(f'<div class="bw" style="left:{it.get("x",40)}px;top:{it.get("y",110)}px;font-size:{it.get("size",50)}px;color:{it.get("c","#fff")};{fam}" {"dir=rtl" if ar else ""}><span data-type="{t:.2f},{t1:.2f}" data-text="{esc(it["write"])}"></span></div>')
            b.e(t, 'chalk', t1=t1)
        elif 'panel' in it:
            pn = it['panel']; cards = ''.join(f'<div class="pcard" style="margin-top:20px">' + panel_rows(b, c.get('blocks', [])) + '</div>' for c in pn.get('cards', [pn]))
            b.add(f'<div class="pnl bp" data-in="{t}" data-a="pop" style="left:{it.get("x",30)}px;top:{it.get("y",100)}px;width:920px;transform-origin:0 0" data-base="scale({it.get("scale",.63)})"><div class="pbar"><img src="{mark}" style="width:34px"><span class="crumb">{esc(pn.get("crumb","Darsify"))}</span><span class="pnew">+ New</span></div>'
                  f'<div style="padding:30px 40px 36px"><div class="ptitle">{esc(pn["title"])}</div>' + (f'<div class="psub">{esc(pn["sub"])}</div>' if pn.get('sub') else '') + cards + '</div></div>')
            b.e(t, 'card')
        elif 'stamp' in it:
            b.add(f'<div class="stampT" data-in="{t}" data-a="stamp" data-rot="-9" style="left:{it.get("x",120)}px;top:{it.get("y",380)}px;border-color:{it.get("c",ORANGE)};color:{it.get("c",ORANGE)};background:#fff;font-size:{it.get("size",52)}px;{fam}">{esc(it["stamp"])}</div>')
            b.e(t, 'stamp')
    b.add('</div>')
    b.add('<div class="clock" style="transform:translateZ(-30px)"><div class="hand h" data-spin="0,%s,%s" data-r0="40"></div><div class="hand m" data-spin="0,%s,%s" data-r0="0"></div><div class="cdot"></div></div>' % (sc['d'], sc.get('clockh', 30), sc['d'], sc.get('clockm', 360)))
    # --- cast ---
    cast = {'ustaz': dict(x=730, y=610, w=300), 'dars': dict(x=110, y=1135, w=330), 'dara': dict(x=640, y=1135, w=330)}
    cast.update({k: {**cast.get(k, {}), **v} for k, v in sc.get('cast', {}).items()})
    present = sc.get('present', ['ustaz', 'dars', 'dara'])
    ex = {w: list(cast[w].get('ex', [[0, 'neutral' if w != 'ustaz' else 'happy']])) for w in present}
    talk = {w: [] for w in present}
    bub_pos = {'dars': dict(x=70, y=1120, side='l'), 'dara': dict(x=1010, y=1120, side='r'), 'ustaz': dict(x=930, y=300, side='r')}
    kf = [[0, *SHOTS[sc.get('open', 'wide')], .01]]
    for c in sc.get('shots', []):
        kf.append([c[0], *SHOTS[c[1]], c[2] if len(c) > 2 else .7])
    lines = sc['lines']
    for i, ln in enumerate(lines):
        who = ln['who']; t = ln['t']
        dur = ln.get('dur', max(1.5, .9 + len(ln['text']) * .045))
        nxt = lines[i + 1]['t'] if i + 1 < len(lines) else sc['d']
        t_out = min(t + dur, nxt - .05) if ln.get('hold') is None else ln['hold']
        html_, t1 = bubble_html(b, who, ln['text'], t, t_out, {**bub_pos[who], **ln.get('pos', {})})
        b.add(html_)
        b.e(t, 'pop'); b.e(t + .12, 'talk', t1=t1, who=VOICE.get(who, 1))
        talk[who].append((t + .1, t1 + .05))
        if ln.get('ex'): ex[who].append([t, ln['ex']])
        for rw, re_ in ln.get('react', {}).items(): ex[rw].append([ln.get('rt', t + .5), re_])
        shot = ln.get('shot', who)
        if shot and shot != 'none':
            kf.append([max(0, t - .25), *SHOTS[shot], ln.get('cd', .6)]); b.e(max(0, t - .25), 'cam')
    kf.sort(key=lambda k: k[0])
    # desks drawn after students so they sit in front
    for w in present:
        c = cast[w]; e_ = sorted(ex[w], key=lambda q: q[0])
        mascot(b, w, e_, c['x'], c['y'], c['w'], c.get('t', .1), hop=c.get('hop'), jump=c.get('jump'), ph=VOICE[w], z=c.get('z', 0 if w == 'ustaz' else 20), talk=talk[w])
    for x in (60, 590):
        b.add(f'<div class="desk" style="left:{x}px;transform:translateZ(60px)"><div class="dtop"></div><div class="dfront"></div></div>')
    b.cam = kf
    if sc.get('caption'):
        cp = sc['caption']; b.hud.append(f'<div class="capt" data-in="{cp.get("t",.2)}" data-a="up" style="{fam}" {"dir=rtl" if ar else ""}>{esc(cp["text"])}</div>')

def sc_ring(b, sc):
    end = head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08) if sc.get('head') else .2
    y = sc.get('ry', 900)
    items = ''.join(f'<div class="rt" style="{"direction:rtl;font-family:A;" if b.ar else ""}{"background:"+tl["bg"]+";" if tl.get("bg") else ""}">{('<div style="position:absolute;right:30px;top:30px">' + svg_mascot(tl["mascot"], 260) + '</div><div style="height:270px"></div>') if tl.get("mascot") else ('<div class="tic" style="background:' + tl.get("c",ORANGE) + '">' + icon(tl.get("icon","star"),72) + '</div>')}<div class="tt">{esc(tl["title"])}</div><div class="td">{esc(tl["desc"])}</div></div>' for tl in sc['tiles'])
    steps = sc.get('steps', [[0, 0]] + [[sc.get('t0', 1.2) + i * sc.get('step', 1.4), i] for i in range(1, len(sc['tiles']))])
    b.add(f'<div class="ringw" data-in="{sc.get("tin_r",.3)}" data-a="zoom" style="top:{y}px"><div class="ring" data-ring=\'{json.dumps(steps)}\' data-r="{sc.get("r",400)}">{items}</div></div>')
    for st in steps[1:]: b.e(st[0], 'whoosh_s'); b.e(st[0] + .45, 'card')
    b.e(sc.get('tin_r', .3), 'card')
    mascots_default(b, sc, 1450)

def sc_flip(b, sc):
    if sc.get('head'): head(b, sc['head'], t0=.1, y=sc.get('y', 280), size=sc.get('size', 104), step=.08)
    F, Bk = sc['front'], sc['back']; fam = 'font-family:A;' if b.ar else ''
    def face(f, cls):
        rows = ''.join(f'<div class="frow">' + (icon('x', 34, '#ffb59a', 3) if cls == 'front' else icon('check', 34, '#4fd39a', 3)) + f'<span>{esc(r)}</span></div>' for r in f.get('rows', []))
        return f'<div class="face {cls}" style="{fam}" {"dir=rtl" if b.ar else ""}><div class="fk">{esc(f.get("kicker",""))}</div><div class="ft">{esc(f["title"])}</div>{rows}</div>'
    b.add(f'<div class="flipw" data-in="{sc.get("t0",.3)}" data-a="pop" style="top:{sc.get("fy",620)}px"><div class="flipc" data-flip="{sc["at"]}">{face(F,"front")}{face(Bk,"back")}</div></div>')
    b.e(sc.get('t0', .3), 'card'); b.e(sc['at'], 'whoosh'); b.e(sc['at'] + .6, 'sparkle')
    mascots_default(b, sc, 1450)

TYPES = dict(hook=sc_hook, chat=sc_chat, list=sc_list, ui=sc_ui, split=sc_split, counter=sc_counter, chips=sc_chips,
             paper=sc_paper, exam=sc_exam, timeline=sc_timeline, tiles=sc_tiles, end=sc_end, story=sc_story, ring=sc_ring, flip=sc_flip)

FAM = {
 'orange': ('radial-gradient(90% 45% at 0% 0%,#fe6e27 0%,rgba(254,110,39,0) 70%),linear-gradient(180deg,#f26229 0%,#cb4627 38%,#5d3222 72%,#000a16 100%)', INK),
 'blue': ('radial-gradient(80% 40% at 100% 0%,rgba(94,139,200,.85) 0%,rgba(94,139,200,0) 70%),linear-gradient(180deg,#2655a3 0%,#1c4486 36%,#10295a 70%,#000a16 100%)', ORANGE),
 'ink': ('radial-gradient(80% 40% at 50% 0%,#1d3a63 0%,rgba(29,58,99,0) 75%),linear-gradient(180deg,#0f2640 0%,#0b1e30 50%,#050f1a 100%)', ORANGE),
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:M,Arial;color:#fff;background:#0b1e30}
.bgl{position:absolute;inset:0;opacity:0}
.abs{position:absolute}
.scene{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}
.masc{position:absolute;transform-origin:50% 100%}
.w{will-change:transform}
.chipT{position:absolute;height:96px;padding:0 42px;border:3px solid #fff;border-radius:999px;font-size:40px;font-weight:700;text-transform:uppercase;display:flex;align-items:center;white-space:nowrap;background:rgba(255,255,255,.08)}
.stampT{position:absolute;padding:16px 36px;border:9px solid;border-radius:22px;font-size:64px;font-weight:800;white-space:nowrap;text-transform:uppercase}
.bub{position:absolute;padding:22px 32px;border-radius:44px 44px 44px 12px;background:#fff;color:#0b1e30;font-size:38px;font-weight:700;white-space:nowrap;box-shadow:0 14px 28px rgba(0,0,0,.3);opacity:0;transform-origin:0% 100%}
.bub.r{border-radius:44px 44px 12px 44px;transform-origin:100% 100%}
.phone{position:absolute;left:110px;width:860px;background:#eae2d8;border-radius:46px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.45);border:10px solid #0b1e30}
.phead{height:120px;background:#0b1e30;display:flex;align-items:center;gap:22px;padding:0 30px;position:relative}
.pav{width:74px;height:74px;border-radius:50%;background:#5e8bc8;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:32px}
.pname{font-size:36px;font-weight:700}.pst{font-size:24px;color:#9fb3cf}
.badge{position:absolute;right:30px;top:32px;min-width:60px;height:56px;border-radius:28px;background:#22a06b;color:#fff;font-weight:800;font-size:30px;display:flex;align-items:center;justify-content:center;padding:0 14px}
.pbody{position:relative;height:calc(100% - 120px);overflow:hidden}
.msg{position:absolute;max-width:640px;padding:20px 28px 30px;border-radius:30px;font-size:36px;line-height:1.3;color:#0b1e30;box-shadow:0 4px 8px rgba(0,0,0,.12)}
.msg.them{left:26px;background:#fff;border-top-left-radius:8px;transform-origin:0 0}
.msg.me{right:26px;background:#d4f0c4;border-top-right-radius:8px;transform-origin:100% 0}
.msg .mt{position:absolute;right:16px;bottom:6px;font-size:20px;color:#7a8a99}
.lcard{position:absolute;left:80px;width:920px;min-height:170px;display:flex;align-items:center;gap:34px;padding:26px 36px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.22);border-radius:36px;backdrop-filter:blur(6px)}
.num{flex:none;width:96px;height:96px;border-radius:50%;background:#f26229;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800}
.num.ic{background:#f26229}
.lt{font-size:46px;font-weight:800;line-height:1.15}.ld{font-size:32px;color:rgba(255,255,255,.85);margin-top:8px;line-height:1.3}
.pnl{position:absolute;left:80px;width:920px;background:#0a1628;border:2px solid rgba(255,255,255,.10);border-radius:34px;overflow:visible;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.pbar{display:flex;align-items:center;gap:20px;height:78px;padding:0 30px;background:#07111f;border-bottom:2px solid rgba(255,255,255,.07);border-radius:34px 34px 0 0}
.crumb{flex:1;font-size:24px;color:#8fa1bd}.pnew{background:#3d74d8;border-radius:14px;padding:8px 18px;font-size:22px;font-weight:700}
.ptitle{font-size:50px;font-weight:800}.psub{font-size:27px;color:#8fa1bd;margin-top:10px;line-height:1.35}
.pcard{background:#0f1f38;border:2px solid rgba(255,255,255,.09);border-radius:26px;padding:22px 30px}
.muted{color:#8fa1bd;font-size:29px}.lbl{font-size:24px;font-weight:700;letter-spacing:.05em;margin-top:8px}
.chipS{display:inline-flex;align-items:center;height:54px;padding:0 22px;border-radius:14px;font-size:27px;font-weight:700;white-space:nowrap}
.chipS.paid{background:rgba(34,160,107,.2);color:#4fd39a}.chipS.pend{background:rgba(242,98,41,.2);color:#ff9a6e}.chipS.sel{background:#2655a3;color:#fff;border:2px solid #5e8bc8}.chipS.bad{background:rgba(229,72,77,.2);color:#ff8a8d}.chipS.info{background:rgba(94,139,200,.22);color:#a9c4ec}
.trow{display:flex;align-items:center;gap:16px;height:94px;font-size:33px;border-bottom:2px solid rgba(255,255,255,.06)}
.track{flex:1;height:28px;border-radius:14px;background:rgba(255,255,255,.08);overflow:hidden}.fillb{height:100%;width:0;border-radius:14px}
.inp{background:#07111f;border:2px solid rgba(255,255,255,.12);border-radius:18px;padding:22px 24px;font-size:31px;min-height:92px;margin-top:12px;line-height:1.35}
.caret{color:#5e8bc8}
.btnS{display:inline-flex;align-items:center;height:76px;padding:0 44px;border-radius:18px;background:#3d74d8;font-size:32px;font-weight:700}
.toast{position:absolute;left:0;right:0;top:0;justify-content:center;height:76px;padding:0 30px;border-radius:18px;background:#22a06b;display:flex;align-items:center;font-size:30px;font-weight:700;white-space:nowrap}
.cb{width:52px;height:52px;border-radius:12px;border:4px solid #3a4f70;display:inline-flex;align-items:center;justify-content:center}
.col{position:absolute;width:450px;height:820px;border-radius:40px}
.ch{text-align:center;font-size:48px;font-weight:800;margin-top:36px;letter-spacing:.02em}
.sitem{position:absolute;width:390px;display:flex;align-items:center;gap:18px;font-size:36px;font-weight:700;line-height:1.2}
.sx{flex:none;width:44px;height:44px;border-radius:12px;border:3px solid #ffb59a;display:flex;align-items:center;justify-content:center}
.stx{position:relative;--sk:0%}.stx:after{content:'';position:absolute;left:0;top:52%;height:5px;width:var(--sk);background:#f26229;border-radius:3px}
.dcard{position:absolute;width:500px;height:190px;border-radius:44px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 26px 60px rgba(11,30,48,.25)}
.paper{position:absolute;width:600px;height:400px;background:#fbfaf6;border-radius:12px;box-shadow:0 16px 34px rgba(0,0,0,.35);padding:40px 46px;color:#0b1e30}
.ptit{font-size:44px;font-weight:800;margin-bottom:26px}.pl{height:16px;background:#d9dee6;border-radius:8px;margin:18px 0;width:90%}
.exam{position:absolute;left:70px;width:940px;height:780px;background:#fff;border-radius:30px;color:#0b1e30;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.ehead{height:120px;display:flex;align-items:center;justify-content:space-between;padding:0 34px;border-bottom:3px dashed #c8cfdb}
.esec{font-size:30px;font-weight:800}.edir{font-size:24px;text-decoration:underline;margin-top:6px}.etime{font-size:52px;font-weight:800}.etools{font-size:44px;font-weight:800}
.ebody{padding:34px 40px}.eq{font-size:34px;line-height:1.4;margin-bottom:26px}
.ech{display:flex;align-items:center;gap:22px;height:84px;border:3px solid #c8cfdb;border-radius:16px;padding:0 24px;margin-bottom:16px;font-size:32px}
.ech.sel{border-color:#3d4fd8;background:#eef0ff}.ech .el{width:46px;height:46px;border-radius:50%;border:3px solid #0b1e30;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:24px}
.ech.sel .el{background:#3d4fd8;border-color:#3d4fd8;color:#fff}
.efoot{position:absolute;left:0;right:0;bottom:0;height:100px;border-top:2px solid #e3e7ee;display:flex;align-items:center;justify-content:space-between;padding:0 34px}
.enav{background:#0b1e30;color:#fff;border-radius:12px;padding:12px 26px;font-size:26px;font-weight:700}.enext{background:#3d4fd8;color:#fff;border-radius:40px;padding:14px 40px;font-size:28px;font-weight:700}
.etabs{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:14px}
.etab{padding:14px 30px;border-radius:999px;background:rgba(255,255,255,.12);font-size:30px;font-weight:700;border:2px solid rgba(255,255,255,.25)}.etab.on{background:#fff;color:#0b1e30}
.trw{position:absolute;left:80px;width:920px;display:flex;align-items:center;gap:30px;height:110px}
.ttime{width:140px;font-size:38px;font-weight:800;text-align:right}.tdot{flex:none;width:30px;height:30px;border-radius:50%;border:5px solid #fff}
.ttxt{font-size:40px;font-weight:700}.tag{margin-left:auto;background:rgba(255,255,255,.16);border-radius:12px;padding:8px 16px;font-size:26px;font-weight:700}
.tile{position:absolute;left:80px;width:920px;height:250px;display:flex;align-items:center;gap:36px;padding:0 40px;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.22);border-radius:40px}
.tic{flex:none;width:130px;height:130px;border-radius:34px;display:flex;align-items:center;justify-content:center}
.tt{font-size:50px;font-weight:800}.td{font-size:32px;color:rgba(255,255,255,.88);margin-top:10px;line-height:1.3}
.ec{position:absolute;height:84px;padding:0 34px;border:3px solid #0b1e30;color:#0b1e30;border-radius:999px;font-size:34px;font-weight:700;display:flex;align-items:center;text-transform:uppercase;white-space:nowrap}
.btnJ{position:absolute;left:340px;top:1060px;width:400px;height:110px;border-radius:999px;background:#f26229;color:#fff;font-size:44px;font-weight:800;display:flex;align-items:center;justify-content:center;letter-spacing:.04em;box-shadow:0 18px 36px rgba(242,98,41,.35)}

.scene{perspective:1800px;perspective-origin:540px 960px}
.cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;transform-style:preserve-3d}
.floor{left:-700px;width:2480px;top:930px;height:1700px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.035) 0 3px,transparent 3px 160px),linear-gradient(180deg,rgba(5,15,26,.35),rgba(5,15,26,.75))}
.wallline{left:-700px;width:2480px;top:918px;height:14px;background:rgba(255,255,255,.12)}
.board{position:absolute;left:60px;top:290px;width:660px;height:580px;background:#0b1e30;border:16px solid #2655a3;border-radius:22px;box-shadow:0 30px 60px rgba(0,0,0,.45);overflow:visible}
.bmark{position:absolute;right:22px;top:20px;width:42px;opacity:.6}
.btitle{position:absolute;left:34px;top:24px;font-size:30px;font-weight:700;color:#8fa1bd;letter-spacing:.06em;text-transform:uppercase}
.bw{position:absolute;font-weight:800;white-space:nowrap;line-height:1.1}
.bp{position:absolute}
.clock{position:absolute;left:805px;top:330px;width:150px;height:150px;border-radius:50%;background:#fff;border:10px solid #2655a3;box-shadow:0 10px 24px rgba(0,0,0,.3)}
.hand{position:absolute;left:65px;bottom:65px;width:10px;border-radius:5px;background:#0b1e30;transform-origin:50% 100%}
.hand.h{height:42px;left:65px}.hand.m{height:58px;background:#f26229}
.cdot{position:absolute;left:60px;top:60px;width:20px;height:20px;border-radius:50%;background:#0b1e30}
.desk{position:absolute;top:1395px;width:430px;height:260px}
.dtop{height:38px;border-radius:14px;background:#eef3f8;box-shadow:0 8px 0 #c9d4e2}
.dfront{margin:0 18px;height:200px;background:linear-gradient(180deg,#2655a3,#1c4486);border-radius:0 0 18px 18px}
.sbub{position:absolute;max-width:520px;padding:24px 34px;background:#fff;color:#0b1e30;font-size:44px;font-weight:700;line-height:1.25;border-radius:42px;box-shadow:0 16px 34px rgba(0,0,0,.35);opacity:0;transform:translateZ(120px)}
.sbub.l{border-bottom-left-radius:10px;transform-origin:0% 100%}.sbub.r{border-bottom-right-radius:10px;transform-origin:100% 100%}
.sbub.ustaz{background:#f26229;color:#fff}.sbub.dara{background:#fff}.sbub.dars{background:#fff}
.sbub .ghost{visibility:hidden}.sbub .typed{position:absolute;left:34px;right:34px;top:24px}
.capt{position:absolute;left:80px;right:80px;top:270px;text-align:center;font-size:54px;font-weight:800;text-transform:uppercase;text-shadow:0 6px 18px rgba(0,0,0,.45)}
.ringw{position:absolute;left:0;width:1080px;height:0;transform-style:preserve-3d}
.ring{position:absolute;left:540px;top:0;transform-style:preserve-3d}
.rt{position:absolute;left:-360px;top:0;width:720px;height:560px;padding:44px;border-radius:44px;background:#12305c;border:3px solid rgba(255,255,255,.25);box-shadow:0 30px 60px rgba(0,0,0,.4);backface-visibility:hidden}
.rt .tic{margin-bottom:34px}.rt .tt{font-size:58px}.rt .td{font-size:36px}
.flipw{position:absolute;left:110px;width:860px;height:760px;perspective:2200px}
.flipc{position:absolute;inset:0;transform-style:preserve-3d}
.face{position:absolute;inset:0;border-radius:48px;padding:56px;backface-visibility:hidden;box-shadow:0 34px 70px rgba(0,0,0,.45)}
.face.front{background:#3a2216;border:3px solid rgba(255,181,154,.4)}.face.back{background:#fff;color:#0b1e30;transform:rotateY(180deg)}
.fk{font-size:34px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;opacity:.75}.ft{font-size:76px;font-weight:800;line-height:1.05;margin:16px 0 34px}
.frow{display:flex;align-items:center;gap:22px;font-size:42px;font-weight:700;margin:22px 0}
#wipe{position:absolute;inset:0;background:#0b1e30;clip-path:circle(0% at 50% 62%);opacity:0}
"""

def build(spec_path, out_dir):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    fam = spec.get('family', 'orange'); spec['_accent'] = FAM[fam][1]
    t = 0.0; scenes = []; events = []; bgs = []
    for i, sc in enumerate(spec['scenes']):
        b = B(spec); b.idx = i; b.sc = sc; b.cam = None
        f = sc.get('family', fam if sc['type'] != 'end' else None)
        if f: spec['_accent'] = sc.get('accent') or FAM[f][1]
        TYPES[sc['type']](b, sc)
        d = sc['d']; s, e = t, t + d
        last = i == len(spec['scenes']) - 1
        tin = sc.get('tin', 'cut' if sc['type'] == 'end' else 'up')
        nxt = spec['scenes'][i + 1] if not last else {}
        tout = 'whip' if nxt.get('tin') == 'whip' else ''
        kf = b.cam or sc.get('cam') or [[0, 540, 960, 1, 0, 0, .01]]
        if b.cam is None and sc.get('cam'):
            for k in kf[1:]: b.e(k[0], 'cam')
        if tin in ('whip',): events.append(dict(t=round(s, 3), k='whip'))
        if tin in ('flip', 'dolly', 'drop'): events.append(dict(t=round(s, 3), k='whoosh'))
        scenes.append(f'<div class="scene" id="S{i}" data-s="{s:.3f}" data-e="{e:.3f}" data-tin="{tin}" data-tout="{tout}" {"data-last=1" if last else ""}>'
                      f'<div class="cam" data-cam=\'{json.dumps(kf)}\' data-drift="{sc.get("drift", 0)}">' + ''.join(b.h) + '</div>' + ''.join(b.hud) + '</div>')
        if f: bgs.append((f, s, e))
        events += [dict(ev, t=round(ev['t'] + s, 3), **({'t1': round(ev['t1'] + s, 3)} if 't1' in ev else {})) for ev in b.ev]
        if i > 0 and sc['type'] != 'end' and tin in ('up', 'zoom', 'cut'): events.append(dict(t=round(s, 3), k='cut'))
        if sc['type'] == 'end': events.append(dict(t=round(s - .45, 3), k='wipe')); spec['_endt'] = s
        t = e
    total = round(t, 3)
    # merge consecutive same-family bg layers
    layers = []
    for f, s, e in bgs:
        if layers and layers[-1][0] == f and abs(layers[-1][2] - s) < 1e-6: layers[-1][2] = e
        else: layers.append([f, s, e])
    F = A / 'fonts'
    fonts = ''.join(f"@font-face{{font-family:{n};font-weight:{w};src:url({(F/f).as_uri()})}}" for n, w, f in [
        ('M', 300, 'Montserrat-Light.ttf'), ('M', 400, 'Montserrat-Regular.ttf'), ('M', 500, 'Montserrat-Medium.ttf'), ('M', 700, 'Montserrat-Bold.ttf'), ('M', 800, 'Montserrat-ExtraBold.ttf'),
        ('A', 300, 'Almarai-Light.ttf'), ('A', 400, 'Almarai-Regular.ttf'), ('A', 700, 'Almarai-Bold.ttf'), ('A', 800, 'Almarai-ExtraBold.ttf')])
    bg = ''.join(f'<div class="bgl" data-s="{s if k else -1}" data-e="{e}" style="background:{FAM[f][0]}"></div>' for k, (f, s, e) in enumerate(layers))
    endt = spec.get('_endt')
    wipe = f'<div id="wipe" data-at="{endt-.45:.3f}"></div>' if endt else ''
    # chat scrolls
    scroll_js = ''
    for idx, (ts, over) in spec.get('_scroll', {}).items():
        scroll_js += f"""(function(){{const s=document.getElementById('S{idx}');const pb=s.querySelector('.pbody');const a=+s.dataset.s;const old=window.renderFrame;window.renderFrame=function(t){{old(t);const lt=t-a;[...pb.children].forEach(m=>m.style.marginTop=(-{over}*eio((lt-{ts})/.5))+'px');}};}})();"""
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{fonts}{CSS}</style></head><body>{bg}{"".join(scenes)}{wipe}<script>{(ENG/"anim.js").read_text()}\n{scroll_js}\nwindow.TOTAL={total};</script></body></html>'
    (out / 'reel.html').write_text(html)
    meta = dict(id=spec['id'], total=total, events=sorted(events, key=lambda x: x['t']), bpm=spec.get('bpm', 120), seed=spec.get('seed', 1), key=spec.get('key', 0), mood=spec.get('mood', 'bright'), endt=endt, cover=spec.get('cover', 1.2))
    (out / 'events.json').write_text(json.dumps(meta, indent=1))
    print(spec['id'], 'total', total, 's', len(events), 'events')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
