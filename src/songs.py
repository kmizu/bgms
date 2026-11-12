"""Four original boss battle themes (16th-note units; see engine.py)."""
from engine import Song

# General MIDI programs
TRUMPET, STRINGS, BRASS, DIST, OVERDRIVE = 56, 48, 61, 30, 29
PICKBASS, FINGERBASS, HARP, PIANO, HARPSI = 34, 33, 46, 0, 6
ROCKORGAN, CHURCHORGAN, CHOIR, TIMPANI = 18, 19, 52, 47


# ---------------------------------------------------------------------------
# 1. Blade of Fate -- D minor, trumpet & strings over a 16th-note bass
# ---------------------------------------------------------------------------
def blade_of_fate():
    s = Song('Blade of Fate', 170, 16, 'd e f g a bb c', {
        'tp': (0, TRUMPET, 112, 58), 'vn': (1, STRINGS, 100, 70),
        'gtr': (2, OVERDRIVE, 76, 36), 'bass': (3, PICKBASS, 112, 64),
        'pad': (4, STRINGS, 74, 84), 'arp': (5, HARP, 92, 44),
        'stab': (6, BRASS, 88, 76), 'timp': (7, TIMPANI, 104, 64),
        'drums': (9, 0, 112, 64)})

    def intro():
        s.section('Dm | C | Bb | A',
                  'd5.3 a4.3 d5.2 f5.3 e5.3 d5.2 | e5.3 c5.3 e5.2 g5.3 f5.3 e5.2 |'
                  'f5.3 d5.3 f5.2 bb5.3 a5.3 g5.2 |'
                  'e5.2 c#5.2 e5.2 a5.2 a4.1 b4.1 c#5.1 d5.1 e5.1 f5.1 g5.1 a5.1',
                  lead=[('vn', 0, 1.0), ('vn', 12, 0.8)],
                  hits='x..x..x.x..x..x.', timp=True)

    a_chords = 'Dm | Bb | C | Dm | Gm | C | F | A'
    a_head = ('a4.2 d5.6 e5.2 f5.6 | g5.4 f5.2 d5.6 r.2 f5.2 | e5.6 c5.2 e5.2 g5.6 |'
              'f5.3 e5.3 d5.10 | bb4.2 d5.6 g5.2 bb5.6 | a5.4 g5.2 e5.6 r.2 g5.2 |'
              'a5.6 f5.2 a5.2 c6.6 |')

    def body():
        s.section(a_chords, a_head + 'bb5.3 a5.3 g5.2 a5.8',
                  lead=[('tp', 0, 1.0)],
                  drums='rock', bass='16', gtr='chug', pad='stacc', stabs='change')
        s.section(a_chords, a_head + 'a5.2 g5.2 f5.2 e5.2 c#5.2 e5.2 a5.4',
                  lead=[('tp', 0, 1.0), ('vn', 12, 0.75)],
                  drums='drive', bass='16', gtr='chug', pad='kizami', stabs='change')
        s.section('Bb | C | Am | Dm | Bb | C | Dm | A',
                  'd5.8 f5.4 bb5.4 | a5.6 g5.2 e5.8 | c5.8 e5.4 a5.4 |'
                  'g5.2 f5.2 e5.2 f5.10 | d5.8 f5.4 bb5.4 | c6.6 bb5.2 g5.4 e5.4 |'
                  'a5.3 g5.3 f5.2 e5.3 f5.3 d5.2 | e5.8 c#5.2 e5.2 g5.2 a5.2',
                  lead=[('vn', 0, 1.0), ('vn', 12, 0.7)],
                  drums='half', bass='8oct', gtr='power', pad='sus', arp='wave',
                  timp=True)
        s.section('Bb C | Am Dm | Gm C | F | Bb C | Am Dm | Gm | A',
                  'd6.6 c6.2 c6.2 bb5.2 c6.4 | e6.6 d6.2 d6.4 a5.4 |'
                  'bb5.6 a5.2 g5.2 a5.2 bb5.2 c6.2 | a5.12 f5.2 a5.2 |'
                  'd6.6 c6.2 c6.2 d6.2 e6.4 | e6.4 c6.2 a5.2 f6.6 e6.2 |'
                  'd6.6 c6.2 bb5.4 g5.4 | a5.8 e5.2 a5.2 c#6.2 e6.2',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0)],
                  drums='dbeat', bass='16', gtr='chug', pad='sus', stabs='sync',
                  timp=True)
    return s, intro, body, 4


# ---------------------------------------------------------------------------
# 2. Crimson Roar -- E minor, twin-guitar speed rock
# ---------------------------------------------------------------------------
def crimson_roar():
    s = Song('Crimson Roar', 184, 16, 'e f# g a b c d', {
        'ld': (0, DIST, 98, 54), 'ld2': (1, DIST, 84, 80),
        'gtr': (2, DIST, 70, 30), 'bass': (3, PICKBASS, 114, 64),
        'pad': (4, ROCKORGAN, 66, 90), 'stab': (6, BRASS, 78, 74),
        'riff': (8, OVERDRIVE, 96, 96), 'timp': (7, TIMPANI, 100, 64),
        'drums': (9, 0, 114, 64)})

    ra = ('e3.1 e3.1 e4.1 e3.1 e3.1 d4.1 e3.1 e3.1 '
          'b3.1 e3.1 e3.1 a3.1 e3.1 g3.1 a3.1 b3.1')
    rb = ('e3.1 e3.1 e4.1 e3.1 e3.1 d4.1 e3.1 e3.1 '
          'c4.1 e3.1 e3.1 b3.1 g3.1 a3.1 b3.1 d4.1')
    riff2 = ra + '|' + rb
    riff_voices = [('riff', 0, 0.95), ('gtr', 0, 0.9), ('bass', -12, 1.0)]

    def intro():
        s.section('Em | Em', lines=[(riff2, riff_voices)],
                  hits='x.......x.......', fill=False)
        s.section('Em | Em', 'e5.8 g5.8 | b5.8 d6.4 d#6.4',
                  lead=[('ld', 0, 1.0), ('ld2', -12, 0.9)],
                  lines=[(riff2, riff_voices)], drums='double', pad='sus')

    def body():
        a = ('e5.4 b5.4 a5.2 g5.2 a5.2 b5.2 | g5.6 f#5.2 e5.8 |'
             'e5.4 c6.4 b5.2 a5.2 b5.2 c6.2 | a5.6 f#5.2 d5.4 f#5.2 a5.2 |'
             'b5.4 e6.4 d6.2 b5.2 d6.2 e6.2 | g6.6 f#6.2 e6.8 |'
             'c6.3 e6.3 g6.2 f#6.3 e6.3 c6.2 | d#6.6 b5.2 f#5.2 b5.2 d#6.2 f#6.2')
        s.section('Em | Em | C | D | Em | Em | C | B', a,
                  lead=[('ld', -12, 1.0)],
                  drums='dbeat', bass='8oct', gtr='chug', pad='sus')
        s.section('Am | D | G | C | Am | B | Em | B',
                  'c6.6 b5.2 a5.4 e5.4 | f#5.6 a5.2 d6.8 | b5.6 a5.2 g5.4 d5.4 |'
                  'e5.6 g5.2 c6.4 e6.4 | e6.3 d6.3 c6.2 b5.3 c6.3 a5.2 |'
                  'b5.6 d#6.2 f#6.8 | g6.4 f#6.2 e6.2 b5.8 |'
                  'f#5.2 b5.2 d#6.2 f#6.2 f#5.1 g5.1 a5.1 b5.1 c#6.1 d#6.1 e6.1 f#6.1',
                  lead=[('ld', -12, 1.0)],
                  drums='half', bass='gallop', gtr='power', pad='sus', stabs='change',
                  timp=True)
        s.section('C | D | Bm | Em | C | D | Em | B',
                  'g6.6 e6.2 e6.4 g6.4 | f#6.6 d6.2 d6.4 f#6.4 |'
                  'f#6.4 d6.2 b5.2 d6.4 f#6.4 | e6.10 r.2 b5.2 e6.2 |'
                  'g6.6 e6.2 c6.2 e6.2 g6.4 | a6.6 f#6.2 d6.4 f#6.4 |'
                  'g6.3 f#6.3 e6.2 d6.3 e6.3 b5.2 | b5.4 d#6.4 f#6.8',
                  lead=[('ld', -12, 1.0), ('ld2', 'third', 0.9)], harmony=-12,
                  drums='double', bass='16', gtr='chug', pad='sus', stabs='sync')
        s.section('Em | Em | Em | Em', 'e6.16 | -.16 | b5.16 | -.8 d6.4 d#6.4',
                  lead=[('ld', -12, 0.95), ('ld2', 'third', 0.85)], harmony=-12,
                  lines=[(riff2 + '|' + riff2, riff_voices)], drums='dbeat', pad='sus')
    return s, intro, body, 4


# ---------------------------------------------------------------------------
# 3. Throne of the Abyss -- C minor, 6/8, organ / harpsichord gothic
# ---------------------------------------------------------------------------
def throne_of_abyss():
    s = Song('Throne of the Abyss', 188, 12, 'c d eb f g ab bb', {
        'vn': (0, STRINGS, 112, 60), 'tp': (1, TRUMPET, 100, 72),
        'gtr': (2, OVERDRIVE, 74, 34), 'bass': (3, FINGERBASS, 108, 64),
        'pad': (4, CHURCHORGAN, 70, 64), 'arp': (5, HARPSI, 100, 40),
        'stab': (6, BRASS, 84, 80), 'timp': (7, TIMPANI, 106, 64),
        'drums': (9, 0, 110, 64)})

    def intro():
        s.section('Cm | Cm | Ab | Ab | Fm | Fm | G | G',
                  'g5.12 | c6.6 g5.6 | ab5.12 | c6.6 ab5.6 |'
                  'f5.6 ab5.6 | c6.6 f6.6 | d6.12 | b5.2 d6.2 g6.2 f6.2 d6.2 b5.2',
                  lead=[('pad', 0, 0.9)], lead_vel=96,
                  arp='up', bass='long', timp=True, fill=False)

    def body():
        s.section('Cm | Cm | Bb | Bb | Ab | Ab | G | G |'
                  'Cm | Cm | Bb | Bb | Ab | Fm | G | G',
                  'c5.4 d5.2 eb5.4 g5.2 | g5.6 eb5.4 g5.2 | f5.4 g5.2 f5.4 d5.2 |'
                  'd5.6 bb4.4 d5.2 | eb5.4 f5.2 eb5.4 c5.2 | ab4.6 c5.4 eb5.2 |'
                  'd5.4 eb5.2 d5.4 b4.2 | d5.6 g5.2 b5.2 d6.2 |'
                  'c6.4 d6.2 eb6.4 g6.2 | g6.6 eb6.4 c6.2 | f6.4 g6.2 f6.4 d6.2 |'
                  'bb5.6 d6.4 f6.2 | eb6.4 d6.2 c6.4 ab5.2 | f5.4 ab5.2 c6.4 f6.2 |'
                  'd6.6 b5.6 | g5.2 b5.2 d6.2 g6.6',
                  lead=[('vn', 0, 1.0), ('tp', 0, 0.85)],
                  drums='68', bass='68', gtr='chug', pad='sus', arp='up')
        s.section('Fm | Fm | Bb | Bb | Eb | Eb | Ab | Ab |'
                  'Fm | Fm | G | G | Cm | Bb | Ab | G',
                  'ab5.6 c6.6 | f6.4 eb6.2 c6.4 ab5.2 | g5.6 bb5.6 |'
                  'eb6.4 d6.2 bb5.4 g5.2 | bb5.6 eb6.6 | g6.4 f6.2 eb6.4 bb5.2 |'
                  'c6.6 eb6.6 | ab6.4 g6.2 eb6.4 c6.2 | f6.4 eb6.2 c6.2 ab5.2 c6.2 |'
                  'f6.6 ab6.6 | d6.4 eb6.2 d6.4 b5.2 | g5.2 b5.2 d6.2 g6.2 f6.2 d6.2 |'
                  'eb6.6 c6.6 | d6.6 bb5.6 | c6.6 ab5.4 c6.2 | b5.6 g5.2 b5.2 d6.2',
                  lead=[('vn', 0, 1.0), ('tp', -12, 0.9)],
                  drums='68drive', bass='68', gtr='power', pad='sus', arp='fast',
                  stabs='change', timp=True)
        s.section('Ab | Bb | Gm | Cm | Ab | Bb | Cm | Cm |'
                  'Ab | Bb | Gm | Cm | Fm | Fm | G | G',
                  'c6.6 eb6.6 | f6.6 d6.4 f6.2 | g6.6 d6.4 bb5.2 | eb6.8 d6.2 c6.2 |'
                  'c6.6 eb6.6 | f6.6 d6.4 f6.2 | g6.12 | -.6 eb6.2 f6.2 g6.2 |'
                  'ab6.6 g6.4 eb6.2 | f6.6 d6.4 bb5.2 | g6.6 f6.4 d6.2 |'
                  'eb6.6 d6.4 c6.2 | f6.4 eb6.2 c6.4 ab5.2 | c6.4 ab5.2 f5.4 ab5.2 |'
                  'g5.4 b5.2 d6.4 g6.2 | f6.2 d6.2 b5.2 g5.2 b5.2 d6.2',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0)],
                  drums='68double', bass='68', gtr='chug', pad='sus', arp='fast',
                  stabs='sync', timp=True)
    return s, intro, body, 8


# ---------------------------------------------------------------------------
# 4. Requiem of the End -- A minor last battle with a D major "hope" theme
# ---------------------------------------------------------------------------
def requiem_of_the_end():
    s = Song('Requiem of the End', 176, 16, 'a b c d e f g', {
        'vn': (0, STRINGS, 114, 58), 'tp': (1, TRUMPET, 104, 72),
        'gtr': (2, DIST, 60, 34), 'bass': (3, PICKBASS, 114, 64),
        'pad': (4, STRINGS, 70, 86), 'arp': (5, PIANO, 100, 44),
        'stab': (6, BRASS, 86, 78), 'timp': (7, TIMPANI, 108, 64),
        'org': (8, CHURCHORGAN, 96, 64), 'choir': (10, CHOIR, 72, 64),
        'drums': (9, 0, 112, 64)})

    def intro():
        s.section('Am | F | Dm | E',
                  'e5.8 a5.8 | c6.12 a5.4 | f5.8 d6.8 | b5.12 g#5.4',
                  lead=[('org', 0, 1.0), ('org', -12, 0.9)], lead_vel=98,
                  pad='sus', bass='long', timp=True, fill=False)
        s.section('E | E',
                  'e5.1 e5.1 g#5.1 e5.1 b5.1 e5.1 g#5.1 e5.1 '
                  'e5.1 e5.1 g#5.1 e5.1 b5.1 e5.1 g#5.1 e5.1 |'
                  'e4.1 f4.1 g#4.1 a4.1 b4.1 c5.1 d5.1 e5.1 '
                  'f5.1 g#5.1 a5.1 b5.1 c6.1 d6.1 e6.2',
                  lead=[('vn', 0, 1.0), ('vn', -12, 0.9)],
                  hits='x..x..x.x..x..x.', timp=True)

    def body():
        a_chords = 'Am | Em | F | C | Dm | Am | B7 | E'
        a = ('a5.6 e5.2 a5.2 b5.2 c6.4 | b5.8 g5.4 e5.4 | a5.6 f5.2 a5.2 c6.2 f6.4 |'
             'e6.8 c6.4 g5.4 | f5.2 a5.2 d6.6 e6.2 f6.4 | e6.6 c6.2 a5.8 |'
             'f#5.4 b5.4 d#6.4 f#6.4 | e6.10 r.2 e6.2 g#6.2')
        s.section(a_chords, a, lead=[('tp', -12, 1.0), ('vn', 0, 0.8)],
                  drums='drive', bass='16', gtr='chug', pad='stacc', stabs='change')
        s.section(a_chords, a, lead=[('vn', 0, 1.0), ('tp', -12, 1.0)],
                  drums='dbeat', bass='16', gtr='chug', pad='sus', arp='up',
                  stabs='sync')
        s.section('F | G | Em | Am | F | G | A | A7',
                  'c6.6 a5.2 f5.4 c6.4 | d6.6 b5.2 g5.4 d6.4 | e6.6 b5.2 g5.4 b5.4 |'
                  'c6.3 b5.3 a5.10 | f6.6 c6.2 a5.4 c6.4 | g6.6 d6.2 b5.4 d6.4 |'
                  'e6.8 c#6.4 e6.4 | a5.2 c#6.2 e6.2 a6.2 g6.2 e6.2 c#6.2 a5.2',
                  lead=[('vn', 0, 1.0), ('org', -12, 0.8)],
                  drums='half', bass='8oct', gtr='power', pad='sus', arp='wave',
                  timp=True)
        s.section('Dm | Bb | C | F A | Dm | Bb | C | D',
                  'd6.6 a5.2 d6.2 e6.2 f6.4 | f6.6 d6.2 bb5.8 |'
                  'e6.6 c6.2 e6.2 f6.2 g6.4 | f6.8 e6.4 c#6.4 |'
                  'd6.3 e6.3 f6.2 a6.6 g6.2 | f6.6 d6.2 bb5.4 d6.4 |'
                  'g6.6 e6.2 c6.4 e6.4 | f#6.12 d6.2 f#6.2',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0)],
                  drums='double', bass='16', gtr='chug', pad='sus', stabs='sync',
                  timp=True)
        s.section('G | A | F#m | Bm | G | A | D | E',
                  'b5.4 d6.4 g6.6 f#6.2 | e6.8 c#6.4 a5.4 | a5.4 c#6.4 f#6.6 e6.2 |'
                  'd6.8 b5.4 f#5.4 | b5.4 d6.4 g6.6 a6.2 | a6.6 g6.2 e6.4 c#6.4 |'
                  'f#6.8 d6.4 a5.4 | e6.4 g#5.4 b5.4 e6.2 g#6.2',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0), ('org', -12, 0.7)],
                  drums='dbeat', bass='8oct', gtr='power', pad='sus', arp='up',
                  stabs='change', timp=True)
    return s, intro, body, 4


SONGS = [
    ('01_blade_of_fate', blade_of_fate),
    ('02_crimson_roar', crimson_roar),
    ('03_throne_of_abyss', throne_of_abyss),
    ('04_requiem_of_the_end', requiem_of_the_end),
]
