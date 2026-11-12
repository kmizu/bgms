"""Still Water -- a slow ambient piece for mindfulness, synthesised directly.

Everything moves on an 11 second cycle (5.5 s swell, 5.5 s release, about
5.5 breaths per minute); chords change every two cycles.  No percussion, no
dissonance, only sine-based pads, soft bells and a breath-like noise bed.
Needs numpy and ffmpeg.
"""
import os
import subprocess
import wave

import numpy as np

SR = 44100
BREATH = 11.0
CHORD = 2 * BREATH
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)

# D major, no leading-tone pull: every chord shares tones with its neighbours
CHORDS = {
    'Dadd9': (50, 57, 64, 66), 'Gmaj7': (43, 50, 59, 66), 'Bm7': (47, 54, 57, 62),
    'Asus2': (45, 52, 59, 64), 'Em9': (52, 59, 62, 66),
}
PROGRESSION = ['Dadd9', 'Gmaj7', 'Dadd9', 'Bm7', 'Gmaj7', 'Dadd9', 'Em9', 'Asus2',
               'Dadd9', 'Gmaj7', 'Bm7', 'Gmaj7', 'Em9', 'Asus2', 'Gmaj7', 'Dadd9']
PENTA = [62, 64, 66, 69, 71, 74, 76, 78, 81, 83]
TOTAL = len(PROGRESSION) * CHORD + 24.0
N = int(TOTAL * SR)
mix = np.zeros((2, N))


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(buf, start, sig):
    i = int(start * SR)
    if i < 0:
        sig, i = sig[:, -i:], 0
    n = min(sig.shape[1], N - i)
    if n > 0:
        buf[:, i:i + n] += sig[:, :n]


def pad_note(m, dur, amp):
    """Slowly beating sine cluster with raised-cosine fades."""
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    env = np.ones_like(t)
    a, r = int(6 * SR), int(8 * SR)
    env[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    env[-r:] = 0.5 + 0.5 * np.cos(np.pi * np.arange(r) / r)
    out = np.zeros((2, len(t)))
    for c, det in enumerate((-0.0007, 0.0007)):
        ph = rng.uniform(0, 2 * np.pi, 3)
        s = np.sin(2 * np.pi * f * (1 + det) * t + ph[0])
        s += 0.6 * np.sin(2 * np.pi * f * t + ph[1])
        s += 0.22 * np.sin(2 * np.pi * 2 * f * (1 - det) * t + ph[2])
        s += 0.06 * np.sin(2 * np.pi * 3 * f * t)
        out[c] = s * env * amp
    return out


def bell(m, amp, pan):
    dur = 9.0
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    s = np.zeros_like(t)
    for mult, a, dec in ((1, 1.0, 2.6), (2, 0.30, 1.6), (3, 0.10, 1.0), (4.2, 0.04, 0.6)):
        s += a * np.sin(2 * np.pi * f * mult * t) * np.exp(-t / dec)
    att = int(0.02 * SR)
    s[:att] *= np.linspace(0, 1, att)
    return np.stack([s * amp * np.cos(pan * np.pi / 2), s * amp * np.sin(pan * np.pi / 2)])


# ---- pads and drone ---------------------------------------------------------
pads = np.zeros((2, N))
for i, name in enumerate(PROGRESSION):
    for k, m in enumerate(CHORDS[name]):
        add(pads, i * CHORD - 3, pad_note(m, CHORD + 8, 0.16 if k else 0.22))
add(pads, 0, pad_note(38, TOTAL - 1, 0.13))            # low D drone throughout
tt = np.arange(N) / SR
breath = 0.5 - 0.5 * np.cos(2 * np.pi * tt / BREATH)   # 0 -> 1 -> 0 every 11 s
mix += pads * (0.68 + 0.32 * breath)

# ---- bells: a slow pentatonic random walk, only stepwise motion ------------------
bells = np.zeros((2, N))
idx = 4
for i in range(2, len(PROGRESSION) - 2):
    dense = 6 <= i < 12
    for q in range(8):                                  # 2.75 s grid
        if rng.random() < (0.42 if dense else 0.28):
            idx = int(np.clip(idx + rng.choice([-2, -1, -1, 1, 1, 2]), 0, len(PENTA) - 1))
            when = i * CHORD + q * BREATH / 4 + rng.uniform(-0.05, 0.05)
            pan = rng.uniform(0.25, 0.75)
            add(bells, when, bell(PENTA[idx], rng.uniform(0.10, 0.16), pan))
            if dense and rng.random() < 0.3:
                add(bells, when + BREATH / 8, bell(PENTA[idx] + 12, 0.04, 1 - pan))
mix += bells

# ---- breath-like noise bed ------------------------------------------------------
freqs = np.fft.rfftfreq(N, 1 / SR)
shape = np.zeros_like(freqs)
band = (freqs > 150) & (freqs < 3000)
shape[band] = 1 / np.sqrt(freqs[band])
for c in range(2):
    nz = np.fft.irfft(np.fft.rfft(rng.standard_normal(N)) * shape, N)
    mix[c] += nz / np.abs(nz).max() * 0.035 * breath ** 1.5

# ---- long, dark reverb ----------------------------------------------------------
L = int(7 * SR)
ti = np.arange(L) / SR
wet = np.zeros_like(mix)
size = 1 << int(np.ceil(np.log2(N + L)))
fir = np.fft.rfftfreq(L, 1 / SR)
for c in range(2):
    ir = rng.standard_normal(L) * np.exp(-ti / 1.3)
    ir = np.fft.irfft(np.fft.rfft(ir) / (1 + (fir / 2500) ** 2), L)   # roll off highs
    ir /= np.sqrt((ir ** 2).sum())
    wet[c] = np.fft.irfft(np.fft.rfft(mix[c], size) * np.fft.rfft(ir, size), size)[:N]
mix = 0.6 * mix + 0.5 * wet

# ---- fades, output --------------------------------------------------------------
fi, fo = int(12 * SR), int(26 * SR)
mix[:, :fi] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(fi) / fi)
mix[:, -fo:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(fo) / fo)
mix *= 0.7 / np.abs(mix).max()

os.makedirs(os.path.join(ROOT, 'mp3'), exist_ok=True)
wav = os.path.join(ROOT, 'mp3', 'still_water.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav,
                '-af', 'loudnorm=I=-20:TP=-2.0:LRA=11', '-ar', '44100', '-b:a', '192k',
                os.path.join(ROOT, 'mp3', 'still_water.mp3')], check=True)
os.remove(wav)

# quick numeric report
mono = mix.mean(0)
spec = np.abs(np.fft.rfft(mono[:1 << 22]))
fr = np.fft.rfftfreq(1 << 22, 1 / SR)
print('length %.0fs  centroid %.0fHz  energy>4kHz %.4f%%' % (
    TOTAL, (spec * fr).sum() / spec.sum(), 100 * (spec[fr > 4000] ** 2).sum() / (spec ** 2).sum()))
win = SR
rms = np.sqrt((mono[:N // win * win].reshape(-1, win) ** 2).mean(1))
print('1s RMS dB: min(body) %.1f max %.1f' % (20 * np.log10(rms[20:-30].min()), 20 * np.log10(rms.max())))
