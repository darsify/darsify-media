"""Original music + SFX for a reel from events.json. Usage: python3 audio.py out/RL-01"""
import json, sys, wave, pathlib
import numpy as np
out = pathlib.Path(sys.argv[1]); meta = json.loads((out / 'events.json').read_text())
SR = 44100; D = meta['total'] + 0.05; N = int(SR * D)
rng = np.random.default_rng(meta.get('seed', 1))
mus = np.zeros((N, 2)); sfx = np.zeros((N, 2))
T = lambda n: np.arange(n) / SR
def place(buf, t, sig, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    if sig.ndim == 1: sig = np.stack([sig * (1 - max(pan, 0)), sig * (1 + min(pan, 0))], 1)
    n = min(len(sig), N - i); buf[i:i + n] += sig[:n] * g
def lpf(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def hpf(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (fc / np.maximum(f, 1)) ** 4); return np.fft.irfft(X, len(x))
def bpf(x, lo, hi): return hpf(lpf(x, hi), lo)
def adsr(n, a=.005, d=.1, s=.6, r=.1):
    e = np.ones(n) * s; A = int(a * SR); Dd = int(d * SR); R = int(r * SR)
    e[:A] = np.linspace(0, 1, A); e[A:A + Dd] = np.linspace(1, s, len(e[A:A + Dd])); e[-R:] *= np.linspace(1, 0, R); return e
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def kick():
    n = int(.35 * SR); t = T(n); f = 50 + 110 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def clap():
    n = int(.22 * SR); return bpf(rng.standard_normal(n) * np.exp(-T(n) * 22), 900, 5000) * 1.4
def hat(o=False):
    n = int((.18 if o else .05) * SR); return hpf(rng.standard_normal(n), 7000) * np.exp(-T(n) * (18 if o else 70))
def pluck(m, d=.35, bright=.35):
    n = int(d * SR); t = T(n); f = hz(m)
    return (np.sin(2 * np.pi * f * t) + bright * np.sin(4 * np.pi * f * t) + .12 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 9) * adsr(n, .003, .05, 1, .03)
def pad(ms, d):
    n = int(d * SR); t = T(n); x = sum(sum(np.sin(2 * np.pi * hz(m) * (1 + det) * t + det * 900) for det in (-.003, 0, .003)) for m in ms) / (3 * len(ms))
    return lpf(x, 1800) * adsr(n, .25, .3, .8, .35)
def bassn(m, d):
    n = int(d * SR); t = T(n); f = hz(m); x = np.sin(2 * np.pi * f * t) + .3 * np.sign(np.sin(2 * np.pi * f * t)) * .4
    return lpf(x, 600) * adsr(n, .005, .08, .7, .05)
def bell(m, d=.5):
    n = int(d * SR); t = T(n); f = hz(m); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 8)) * np.exp(-t * 6)

# ---- progressions by mood (root, triad) in C; transposed by key ----
PROG = {
 'bright': [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])],      # C G Am F
 'warm':   [(41, [60, 65, 69]), (48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69])],      # F C G Am
 'drive':  [(45, [60, 64, 69]), (41, [60, 65, 69]), (48, [60, 64, 67]), (43, [59, 62, 67])],      # Am F C G
 'chill':  [(48, [60, 64, 67, 71]), (45, [60, 64, 67, 69]), (41, [60, 64, 65, 69]), (43, [62, 65, 67, 71])],  # Cmaj7 Am7 Fmaj7 G7
}
mood = meta.get('mood', 'bright'); key = meta.get('key', 0); P = [(r + key, [m + key for m in ch]) for r, ch in PROG.get(mood, PROG['bright'])]
bpm = meta.get('bpm', 120); bt = 60 / bpm; off = 0.15
endt = meta.get('endt') or D
nb = int((D - off) / bt)
for b in range(nb):
    t = off + b * bt
    if t > D - .3: break
    end = t >= endt - .05; pre = endt - 2 * bt * 4 <= t < endt - .05
    bar = b // 4; root, ch = P[bar % 4]; arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
    intro = t < off + 4 * bt
    if not intro and not (pre and b % 2):
        place(mus, t, kick(), .8)
    if not intro and b % 4 in (1, 3): place(mus, t, clap(), .32 if not end else .42)
    place(mus, t, hat(), .1, .3); place(mus, t + bt / 2, hat(b % 4 == 3), .09, .3)
    if not intro:
        place(mus, t, bassn(root, bt * .45), .4); place(mus, t + bt / 2, bassn(root + (12 if b % 2 else 0), bt * .4), .3)
    place(mus, t, pluck(arp[b % 4] if mood != 'chill' else arp[(b * 3) % 4], .35, .45 if mood == 'drive' else .35), .15, -.25)
    place(mus, t + bt / 2, pluck(arp[(b + 2) % 4] + (12 if end else 0)), .1, .25)
    if b % 4 == 0: place(mus, t, pad(ch, 4 * bt), .32 if not pre else .24)
    if end and b % 4 == 0: place(mus, t, pad([m + 12 for m in ch], 4 * bt), .12)
# riser into the end card
if meta.get('endt'):
    i0, i1 = int(max(0, endt - 2.2) * SR), int(endt * SR); n = i1 - i0
    if n > 0:
        rise = hpf(rng.standard_normal(n), 2000) * np.linspace(0, 1, n) ** 2 * .16
        sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(200, 900, n)) / SR) * np.linspace(0, 1, n) ** 3 * .07
        mus[i0:i1] += np.stack([rise + sweep] * 2, 1)
    n = int(1.2 * SR); t = T(n); place(mus, endt, np.sin(2 * np.pi * np.cumsum(45 + 80 * np.exp(-t * 8)) / SR) * np.exp(-t * 3), .65)
    place(mus, D - 1.6, pad([P[0][0], P[0][1][0], P[0][1][1], P[0][1][2], P[0][1][0] + 12], 1.5), .4)
fade = np.ones(N); fs = max(0, N - int(.6 * SR)); fade[fs:] = np.linspace(1, 0, N - fs); mus *= fade[:, None]
fi = int(.25 * SR); mus[:fi] *= np.linspace(0, 1, fi)[:, None]

# ---- SFX ----
def swish(d=.25, lo=800, hi=6000):
    n = int(d * SR); return bpf(rng.standard_normal(n), lo, hi) * np.sin(np.linspace(0, np.pi, n)) ** 2
def thump():
    n = int(.25 * SR); t = T(n); return np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 12) + 40) / SR) * np.exp(-t * 14)
def ding(m=88, d=.6):
    n = int(d * SR); t = T(n); f = hz(m); return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)) * np.exp(-t * 5)
def bloop(f0=500, f1=1100, d=.14):
    n = int(d * SR); f = np.linspace(f0, f1, n); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.linspace(0, np.pi, n))
def pop(f=700):
    n = int(.09 * SR); t = T(n); return np.sin(2 * np.pi * np.cumsum(f * np.exp(-t * 25) + f * .4) / SR) * np.exp(-t * 35)
def click(): n = int(.025 * SR); return hpf(rng.standard_normal(n), 2500) * np.exp(-T(n) * 220)
def tick(): n = int(.03 * SR); t = T(n); return (np.sin(2 * np.pi * 3200 * t) * .6 + hpf(rng.standard_normal(n), 3000) * .5) * np.exp(-t * 180)
def pen(): n = int(.12 * SR); return bpf(rng.standard_normal(n), 2000, 6000) * np.exp(-T(n) * 25) * .7
def boing():
    n = int(.35 * SR); t = T(n); f = 300 + 180 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 6) + np.linspace(0, 250, n); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def stamp():
    th = thump(); n = int(.06 * SR); x = bpf(rng.standard_normal(n), 300, 3000) * np.exp(-T(n) * 60); th[:n] += x; return th
def sparkle():
    o = np.zeros(int(1.0 * SR))
    for k, m in enumerate([84, 88, 91, 96, 100]):
        s = ding(m, .6) * .5; i = int(k * .06 * SR); o[i:i + len(s)] += s[:len(o) - i]
    return o
def msg_tone(): return bloop(900, 1500, .1) * .8 + np.pad(bloop(1300, 1900, .08), (int(.07 * SR), 0))[:int(.1 * SR)]

for ev in meta['events']:
    t, k = ev['t'], ev['k']; pan = float(rng.uniform(-.4, .4))
    if k == 'word': place(sfx, t, pop(600 + rng.integers(0, 400)), .14, pan)
    elif k == 'soft': place(sfx, t, swish(.3, 1500, 7000), .12)
    elif k in ('pop', 'pop_s'): place(sfx, t, pop(800 + rng.integers(0, 500)), .3 if k == 'pop' else .18, pan)
    elif k == 'pop_hi': place(sfx, t, pop(1100), .35)
    elif k == 'stamp': place(sfx, t, stamp(), .7); place(sfx, t + .05, ding(91, .4), .12)
    elif k == 'whoosh_s': place(sfx, t, swish(.3, 600, 4000), .12, pan)
    elif k == 'whoosh': place(sfx, t, swish(.5, 400, 6000), .45)
    elif k == 'boing': place(sfx, t, boing(), .3, pan)
    elif k == 'msg': place(sfx, t, msg_tone(), .3, -.2)
    elif k == 'msg_me': place(sfx, t, bloop(700, 1200, .12), .3, .2)
    elif k == 'card': place(sfx, t, swish(.22, 1200, 7000), .22, pan); place(sfx, t + .08, pop(900), .14)
    elif k == 'ding_s': place(sfx, t, ding(89, .5), .22)
    elif k == 'pen': place(sfx, t, pen(), .35, pan)
    elif k == 'rise': place(sfx, t, swish(.6, 300, 2500), .12)
    elif k == 'click': place(sfx, t, click(), .6)
    elif k == 'success': place(sfx, t, bloop(700, 1500, .14), .3); place(sfx, t + .09, bloop(900, 1800, .12), .22)
    elif k == 'type':
        tt = t
        while tt < ev['t1']: place(sfx, tt + rng.uniform(0, .02), click(), .26, pan); tt += .055 + rng.uniform(0, .03)
    elif k == 'count':
        tt = t; gap = .05
        while tt < ev['t1']: place(sfx, tt, tick(), .25); tt += gap
    elif k == 'thump': place(sfx, t, thump(), .45, pan); place(sfx, t, swish(.12, 2000, 6000), .1)
    elif k == 'sparkle': place(sfx, t, sparkle(), .42)
    elif k == 'cut': place(sfx, t - .08, swish(.2, 600, 4000), .26); place(sfx, t, thump(), .3)
    elif k == 'wipe': place(sfx, t, swish(.6, 300, 6000), .6)
mix = mus * .55 + sfx * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2); mix /= np.abs(mix).max() * 1.05
w = wave.open(str(out / 'audio.wav'), 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print('audio ok', round(D, 2), 's')
