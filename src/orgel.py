"""Still Water (music box) -- a slow 3/4 lullaby for a synthesised music box.

One bar lasts 2.75 s, so a four-bar phrase is one 11 s breath cycle, the same
pacing as mindful.py.  Melody and chords are hand-written; the comb tones are
additive synthesis.  Needs numpy, mido (via engine.py) and ffmpeg.
"""
import os
import subprocess
import wave

import numpy as np

from engine import Chord, parse_line, pc_of

SR = 44100
BAR = 6                    # units are eighth notes, 3/4 time
UNIT = 2.75 / BAR          # seconds per eighth at full speed
SCALE = [pc_of(n) for n in 'd e f# g a b c#'.split()]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(11)

A1 = ('D D G G Bm Bm G A',
      'f#5.4 a5.2 | d6.6 | b5.4 d6.2 | g5.6 | f#5.4 b5.2 | d6.4 c#6.2 | b5.4 g5.2 | a5.6')
A2 = ('D D G G Em A D D',
      'f#5.4 a5.2 | d6.4 e6.2 | d6.4 b5.2 | g5.4 a5.2 | b5.4 g5.2 | a5.4 e5.2 |'
      'f#5.4 e5.2 | d5.6')
B1 = ('G G D D Em Em A A',
      'd6.4 b5.2 | g6.4 f#6.2 | f#6.4 d6.2 | a5.6 | b5.4 g5.2 | e6.4 d6.2 |'
      'c#6.4 a5.2 | e5.2 a5.2 c#6.2')
INTRO = ('D D G G', None)
# (section, accompaniment density, add lower harmony)
FORM = [(INTRO, 1, False), (A1, 1, False), (A2, 1, False), (B1, 2, False), (A2, 2, False),
        (A1, 2, True), (A2, 2, True), (B1, 2, True), (A2, 1, True), (A2, 1, False)]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def third_below(p):
    pc = p % 12
    return p - (pc - SCALE[(SCALE.index(pc) - 2) % 7]) % 12


# ---- score -> (unit, pitch, amp) and chord spans ---------------------------------
notes, chords, pos = [], [], 0
for (chart, melody), density, harm in FORM:
    syms = chart.split()
    for b, sym in enumerate(syms):
        ch = Chord(sym)
        root = 55 + (ch.root - 55) % 12
        third = root + ch.ivs[1] + 12
        fifth = root + 7
        chords.append((pos + b * BAR, sorted(48 + (pc - 48) % 12 for pc in ch.pcs)))
        if density == 1:
            pat = ((0, root), (2, fifth), (4, third))
        else:
            pat = ((0, root), (1, fifth), (2, third), (3, fifth), (4, third), (5, fifth))
        for u, p in pat:
            notes.append((pos + b * BAR + u, p, 0.42 if u == 0 else 0.30))
    if melody:
        line, _ = parse_line(melody, BAR, 'orgel')
        for s, d, p in line:
            notes.append((pos + s, p, 0.80))
            if harm and d >= 4:
                notes.append((pos + s, third_below(p), 0.40))
    pos += len(syms) * BAR
total_units = pos

# ---- tempo map: steady, then winding down over the last eight bars ---------------
rit_start = total_units - 8 * BAR
edges = np.zeros(total_units + 1)
for u in range(total_units):
    slow = max(0.0, (u - rit_start) / (8 * BAR))
    edges[u + 1] = edges[u] + UNIT * (1 + 0.9 * slow ** 2)
START = 1.0
TOTAL = START + edges[-1] + 9.0
N = int(TOTAL * SR)


def when(u):
    return START + edges[int(u)]


def tine(m, amp):
    """Music-box comb tooth: decaying sine with a short inharmonic 'ping'."""
    f = hz(m)
    dec = float(np.clip(2.2 * (523.0 / f) ** 0.6, 0.6, 3.5))
    t = np.arange(int(min(6.0, dec * 6) * SR)) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / dec)
    s += 0.22 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / (dec * 0.45))
    s += 0.07 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / (dec * 0.25))
    if 6.27 * f < 14000:
        s += 0.09 * np.sin(2 * np.pi * 6.27 * f * t) * np.exp(-t / 0.07)
    a = int(0.002 * SR)
    s[:a] *= np.linspace(0, 1, a)
    return s * amp


dry = np.zeros((2, N))
for u, p, amp in notes:
    s = tine(p, amp * rng.uniform(0.9, 1.05))
    i = int((when(u) + rng.uniform(-0.006, 0.006)) * SR)
    pan = np.clip(0.5 + (p - 74) / 60 + rng.uniform(-0.05, 0.05), 0.2, 0.8)
    n = min(len(s), N - i)
    dry[0, i:i + n] += s[:n] * np.cos(pan * np.pi / 2)
    dry[1, i:i + n] += s[:n] * np.sin(pan * np.pi / 2)

# ---- very quiet pad underneath, swelling once per four bars (11 s) -----------------
pad = np.zeros((2, N))
for k, (u, voicing) in enumerate(chords):
    t0 = when(u) - 1.0
    end = when(min(u + BAR, total_units)) + 2.5
    t = np.arange(int((end - t0) * SR)) / SR
    env = np.minimum(1, t / 2.0) * np.minimum(1, (t[-1] - t) / 2.5)
    for m in voicing:
        for c, det in enumerate((-0.0007, 0.0007)):
            s = np.sin(2 * np.pi * hz(m) * (1 + det) * t + rng.uniform(0, 6.28)) * env * 0.05
            i = int(t0 * SR)
            n = min(len(s), N - i)
            pad[c, i:i + n] += s[:n]
tt = np.arange(N) / SR
pad *= 0.6 + 0.4 * (0.5 - 0.5 * np.cos(2 * np.pi * (tt - START) / 11.0))
mix = dry + pad

# ---- small wooden-box reverb ---------------------------------------------------
L = int(3.5 * SR)
ti = np.arange(L) / SR
fir = np.fft.rfftfreq(L, 1 / SR)
size = 1 << int(np.ceil(np.log2(N + L)))
wet = np.zeros_like(mix)
for c in range(2):
    ir = rng.standard_normal(L) * np.exp(-ti / 0.55)
    ir = np.fft.irfft(np.fft.rfft(ir) / (1 + (fir / 4000) ** 2), L)
    ir /= np.sqrt((ir ** 2).sum())
    wet[c] = np.fft.irfft(np.fft.rfft(mix[c], size) * np.fft.rfft(ir, size), size)[:N]
mix = 0.75 * mix + 0.3 * wet
fo = int(5 * SR)
mix[:, -fo:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(fo) / fo)
mix *= 0.7 / np.abs(mix).max()

os.makedirs(os.path.join(ROOT, 'mp3'), exist_ok=True)
wav = os.path.join(ROOT, 'mp3', 'still_water_orgel.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav,
                '-af', 'loudnorm=I=-20:TP=-2.0:LRA=11', '-ar', '44100', '-b:a', '192k',
                os.path.join(ROOT, 'mp3', 'still_water_orgel.mp3')], check=True)
os.remove(wav)

mono = mix.mean(0)
spec = np.abs(np.fft.rfft(mono[:1 << 22]))
fr = np.fft.rfftfreq(1 << 22, 1 / SR)
rms = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
print('length %.0fs  notes %d  centroid %.0fHz  energy>6kHz %.3f%%  box %.1fdB  pad %.1fdB' % (
    TOTAL, len(notes), (spec * fr).sum() / spec.sum(),
    100 * (spec[fr > 6000] ** 2).sum() / (spec ** 2).sum(), rms(dry), rms(pad)))
