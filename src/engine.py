"""Tiny sequencing engine for battle BGMs.

Time unit is one 16th note.  A song is a list of sections; each section has a
chord chart and a hand-written melody, and the engine derives bass, rhythm
guitar, pads, arpeggios, stabs and drums from the chords.
"""
import random
import re

import mido

TPU = 120  # ticks per 16th (480 ppq)
NOTE_PC = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
QUALITIES = {
    '': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10),
    'maj7': (0, 4, 7, 11), 'dim': (0, 3, 6), 'm7b5': (0, 3, 6, 10),
    'sus4': (0, 5, 7), 'aug': (0, 4, 8), '5': (0, 7),
}
KICK, SNARE, CHH, OHH, CRASH, RIDE, CHINA = 36, 38, 42, 46, 49, 51, 52
TOMS = (50, 47, 45, 43)


def pc_of(name):
    name = name.lower()
    pc = NOTE_PC[name[0]]
    for a in name[1:]:
        pc += 1 if a == '#' else -1
    return pc % 12


def pitch_of(tok):
    m = re.fullmatch(r'([a-g][#b]*)(-?\d)', tok.lower())
    if not m:
        raise ValueError('bad pitch ' + tok)
    return pc_of(m.group(1)) + 12 * (int(m.group(2)) + 1)


class Chord:
    def __init__(self, sym):
        m = re.fullmatch(r'([A-G][#b]?)([^/]*)(?:/([A-G][#b]?))?', sym)
        if not m or m.group(2) not in QUALITIES:
            raise ValueError('bad chord ' + sym)
        self.sym = sym
        self.root = pc_of(m.group(1))
        self.ivs = QUALITIES[m.group(2)]
        self.bass = pc_of(m.group(3)) if m.group(3) else self.root
        self.pcs = [(self.root + i) % 12 for i in self.ivs]


def parse_chords(text, bar):
    """'Dm | Bb C' -> [(start, length, Chord)] with bars split evenly."""
    spans, pos = [], 0
    for b in text.split('|'):
        syms = b.split()
        n = len(syms)
        if bar % n:
            raise ValueError('cannot split bar: ' + b)
        for s in syms:
            spans.append((pos, bar // n, Chord(s)))
            pos += bar // n
    return spans, pos


def parse_line(text, bar, label=''):
    """'d5.4 r.2 -.2 | ...' -> [(start, dur, pitch)]; '-' ties, 'r' rests."""
    notes, pos = [], 0
    for i, b in enumerate(text.split('|')):
        total = 0
        for tok in b.split():
            name, dur = tok.rsplit('.', 1)
            dur = int(dur)
            if name == '-':
                s, d, p = notes[-1]
                notes[-1] = (s, d + dur, p)
            elif name != 'r':
                notes.append((pos + total, dur, pitch_of(name)))
            total += dur
        if total != bar:
            raise ValueError('%s bar %d has %d units, want %d' % (label, i + 1, total, bar))
        pos += bar
    return notes, pos


class Song:
    def __init__(self, title, bpm, bar, scale, channels, seed=1):
        self.title, self.bpm, self.bar = title, bpm, bar
        self.scale = [pc_of(n) for n in scale.split()]
        self.channels = channels  # name -> (channel, program, volume, pan)
        self.events = []          # (unit, kind, channel, a, b)
        self.pos = 0
        self.rng = random.Random(seed)

    # ---- low level -------------------------------------------------------
    def note(self, ch, start, dur, pitch, vel, gate=0.92):
        if ch not in self.channels:
            return
        c = self.channels[ch][0]
        vel = max(1, min(127, int(vel + self.rng.randint(-3, 3))))
        pitch = int(pitch)
        self.events.append((start, 1, c, pitch, vel))
        self.events.append((start + max(dur * gate, 0.3), 0, c, pitch, 0))

    def cc(self, ch, at, num, val):
        self.events.append((at, 2, self.channels[ch][0], num, val))

    def drum(self, start, pitch, vel):
        vel = max(1, min(127, int(vel + self.rng.randint(-4, 4))))
        self.events.append((start, 1, 9, pitch, vel))
        self.events.append((start + 0.9, 0, 9, pitch, 0))

    # ---- helpers ---------------------------------------------------------
    def bass_pitch(self, pc):
        return 28 + (pc - 4) % 12

    def third_below(self, pitch):
        pc = pitch % 12
        if pc not in self.scale:
            return pitch - 3
        target = self.scale[(self.scale.index(pc) - 2) % 7]
        return pitch - (pc - target) % 12

    def voicing(self, chord, low):
        return sorted(low + (pc - low) % 12 for pc in chord.pcs)

    # ---- section ---------------------------------------------------------
    def section(self, chords, melody=None, lead=(), harmony=None, lines=(),
                drums=None, bass=None, gtr=None, pad=None, arp=None,
                stabs=None, hits=None, timp=False, fill=True, crash=True,
                lead_vel=104):
        B, base = self.bar, self.pos
        spans, length = parse_chords(chords, B)
        nbars = length // B

        all_lines = list(lines)
        if melody:
            all_lines.insert(0, (melody, list(lead)))
        for text, voices in all_lines:
            notes, ln = parse_line(text, B, self.title)
            if ln != length:
                raise ValueError('%s: line is %d units, chords %d' % (self.title, ln, length))
            for s, d, p in notes:
                for ch, tr, scale in voices:
                    q = self.third_below(p) if tr == 'third' else p
                    if tr != 'third':
                        q += tr
                    else:
                        q += harmony or 0
                    accent = 6 if s % B == 0 else 0
                    self.note(ch, base + s, d, q, lead_vel * scale + accent, gate=0.96)
                    if d >= 6:   # delayed vibrato on long notes
                        self.cc(ch, base + s, 1, 0)
                        self.cc(ch, base + s + 3, 1, 45)
                        self.cc(ch, base + s + 4.5, 1, 75)
                        self.cc(ch, base + s + d, 1, 0)

        def hit_units(span_start, span_len):
            return [u for u in range(span_len) if hits[(span_start + u) % B] == 'x']

        for i, (s, ln, ch) in enumerate(spans):
            nxt = spans[i + 1][2] if i + 1 < len(spans) else None
            root = self.bass_pitch(ch.bass)
            at = base + s

            # ---------------- bass
            if hits:
                for u in hit_units(s, ln):
                    self.note('bass', at + u, 2, root, 112, gate=0.8)
            elif bass == 'long':
                self.note('bass', at, ln, root, 100)
            elif bass:
                step = 1 if bass in ('16', 'gallop') else 2
                for u in range(0, ln, step):
                    k = u // step
                    if bass == '8oct':
                        off = (0, 0, 12, 0, 0, 12, 0, 12)[k % 8]
                    elif bass == '16':
                        off = (0, 0, 12, 0, 0, 0, 12, 0, 0, 0, 12, 0, 0, 12, 7, 12)[k % 16]
                    elif bass == 'gallop':
                        if u % 4 == 1:
                            continue
                        off = 12 if u % 8 == 6 else 0
                    elif bass == '68':
                        off = (0, 0, 12, 0, 12, 7)[k % 6]
                    else:  # pedal8
                        off = 0
                    p = root + off
                    last = u + step >= ln
                    if last and nxt and nxt.bass != ch.bass and bass != 'pedal8':
                        nb = self.bass_pitch(nxt.bass)
                        if nb < root:
                            nb += 12 if root - nb > 6 else 0
                        p = nb - (2 if (nb - 2) % 12 in self.scale else 1)
                    vel = 108 if u % 4 == 0 else 92
                    self.note('bass', at + u, step, p, vel, gate=0.85)

            # ---------------- rhythm guitar
            g = 40 + (ch.bass - 4) % 12
            fifth = 7 if 7 in ch.ivs else (6 if 6 in ch.ivs else 8)
            if hits:
                for u in hit_units(s, ln):
                    for p in (g, g + fifth, g + 12):
                        self.note('gtr', at + u, 2, p, 108, gate=0.8)
            elif gtr == 'chug':
                step = 1 if B == 16 else 2
                acc = (0, 6, 12) if B == 16 else (0, 6)
                for u in range(0, ln, step):
                    if (s + u) % B in acc or u == 0:
                        for p in (g, g + fifth, g + 12):
                            self.note('gtr', at + u, step, p, 104, gate=0.9)
                    else:
                        for p in (g, g + fifth):
                            self.note('gtr', at + u, step, p, 74, gate=0.5)
            elif gtr == 'power':
                for u in range(0, ln, 8 if B == 16 else 6):
                    d = min(8 if B == 16 else 6, ln - u)
                    for p in (g, g + fifth, g + 12):
                        self.note('gtr', at + u, d, p, 98)
            elif gtr == 'stab8':
                for u in range(0, ln, 2):
                    for p in (g, g + fifth, g + 12):
                        self.note('gtr', at + u, 2, p, 100 if u % 4 == 0 else 84, gate=0.6)

            # ---------------- pad
            v = self.voicing(ch, 55)
            if pad == 'sus':
                for p in v:
                    self.note('pad', at, ln, p, 78, gate=1.0)
            elif pad == 'stacc':
                for u in range(0, ln, 2):
                    for p in v:
                        self.note('pad', at + u, 2, p, 86 if u % 4 == 0 else 70, gate=0.55)
            elif pad == 'kizami':
                for u in range(ln):
                    grp = v[1:] if u % 2 == 0 else v[:1]
                    for p in grp:
                        self.note('pad', at + u, 1, p + 12, 84 if u % 4 == 0 else 68, gate=0.7)
            if 'choir' in self.channels and pad:
                for p in v:
                    self.note('choir', at, ln, p, 70, gate=1.0)

            # ---------------- arpeggio
            if arp:
                tones = self.voicing(ch, 60)
                tones = tones + [t + 12 for t in tones]
                if B == 16:
                    pat = (0, 2, 1, 2, 3, 2, 1, 2) if arp == 'wave' else (0, 1, 2, 3, 4, 3, 2, 1)
                    step = 1
                else:
                    pat = (0, 1, 2, 3, 2, 1)
                    step = 2 if arp != 'fast' else 1
                for k, u in enumerate(range(0, ln, step)):
                    self.note('arp', at + u, step, tones[pat[k % len(pat)]],
                              88 if k % len(pat) == 0 else 72, gate=0.8)

            # ---------------- brass stabs
            sv = self.voicing(ch, 60)
            if hits:
                for u in hit_units(s, ln):
                    for p in sv:
                        self.note('stab', at + u, 2, p, 110, gate=0.75)
            elif stabs == 'change':
                for p in sv:
                    self.note('stab', at, 3, p, 100, gate=0.8)
            elif stabs == 'sync':
                for u in ((0, 3, 6) if B == 16 else (0, 6)):
                    if u < ln:
                        for p in sv:
                            self.note('stab', at + u, 2, p, 100, gate=0.75)

            # ---------------- timpani
            if timp and s % (2 * B) == 0:
                self.note('timp', at, 4, root + 12, 110)

        if timp:
            r = self.bass_pitch(spans[-1][2].bass) + 12
            half = B // 2
            for u in range(half):
                self.note('timp', base + length - half + u, 1, r, 60 + 55 * u // half)

        # -------------------- drums
        for b in range(nbars):
            self.drum_bar(drums, base + b * B, hits,
                          first=(b == 0 and crash),
                          big_fill=(fill and b == nbars - 1),
                          small_fill=(fill and b % 4 == 3 and b != nbars - 1))
        self.pos += length

    def drum_bar(self, style, at, hits, first, big_fill, small_fill):
        B = self.bar
        half = B // 2
        if first and (style or hits):
            self.drum(at, CRASH, 118)
        if hits:
            for u in range(B):
                if hits[u] == 'x' and not (big_fill and u >= half):
                    self.drum(at + u, KICK, 116)
                    self.drum(at + u, SNARE if u else KICK, 104)
                    if u:
                        self.drum(at + u, CHINA, 96)
        elif style:
            P = {
                # style: (kick, snare, cymbal positions, cymbal note)
                'rock':   ('x.....x.x.x.....', '....x.......x...', 2, CHH),
                'drive':  ('x.x...x.x.x...x.', '....x.......x...', 2, CHH),
                'dbeat':  ('x...x...x...x...', '..x...x...x...x.', 4, RIDE),
                'double': ('xxxxxxxxxxxxxxxx', '....x.......x...', 4, CHINA),
                'half':   ('x.....x...x.....', '........x.......', 2, RIDE),
                '68':     ('x.........x.', '......x.....', 2, CHH),
                '68drive': ('x...x.....x.', '......x.....', 2, RIDE),
                '68double': ('x.x.x.x.x.x.', '......x.....', 6, CHINA),
            }[style]
            kick, snare, cstep, cym = P
            for u in range(B):
                if big_fill and u >= half:
                    break
                if kick[u] == 'x':
                    self.drum(at + u, KICK, 112 if u % 4 == 0 else 98)
                if snare[u] == 'x':
                    self.drum(at + u, SNARE, 114)
                if u % cstep == 0 and not (first and u == 0):
                    self.drum(at + u, cym, 92 if u % 4 == 0 else 70)
            if small_fill:
                for u in (B - 2, B - 1):
                    self.drum(at + u, SNARE, 100 + 8 * (u - B + 2))
        if big_fill and (style or hits):
            n = B - half
            for k in range(n):
                u = half + k
                if k < n // 2:
                    inst = SNARE
                else:
                    inst = TOMS[min(3, (k - n // 2) * 4 // (n - n // 2))]
                self.drum(at + u, inst, 88 + 34 * k // n)
                if k % 2 == 0:
                    self.drum(at + u, KICK, 104)

    # ---- output ----------------------------------------------------------
    def seconds(self, units):
        return units * 60.0 / self.bpm / 4

    def write(self, path, cut=None):
        mid = mido.MidiFile(ticks_per_beat=TPU * 4)
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        tr.append(mido.MetaMessage('track_name', name=self.title, time=0))
        tr.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.bpm), time=0))
        num, den = (4, 4) if self.bar == 16 else (6, 8)
        tr.append(mido.MetaMessage('time_signature', numerator=num, denominator=den, time=0))
        for name, (c, prog, vol, pan) in self.channels.items():
            if c != 9:
                tr.append(mido.Message('program_change', channel=c, program=prog, time=0))
            tr.append(mido.Message('control_change', channel=c, control=7, value=vol, time=0))
            tr.append(mido.Message('control_change', channel=c, control=10, value=pan, time=0))
            tr.append(mido.Message('control_change', channel=c, control=91, value=50, time=0))
        evs = []
        for (u, kind, c, a, b) in self.events:
            if cut is not None:
                if kind != 0 and u >= cut:
                    continue
                u = min(u, cut)
            evs.append((int(round(u * TPU)), kind, c, a, b))
        evs.sort(key=lambda e: (e[0], e[1] != 0, e[1]))  # note-offs first
        now = 0
        for t, kind, c, a, b in evs:
            if kind == 1:
                msg = mido.Message('note_on', channel=c, note=a, velocity=b, time=t - now)
            elif kind == 0:
                msg = mido.Message('note_off', channel=c, note=a, velocity=0, time=t - now)
            else:
                msg = mido.Message('control_change', channel=c, control=a, value=b, time=t - now)
            tr.append(msg)
            now = t
        tr.append(mido.MetaMessage('end_of_track', time=TPU * 8))
        mid.save(path)
