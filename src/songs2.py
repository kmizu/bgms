"""Second set: four original boss themes in a mid-90s SFC rock idiom --
slap-bass riffs, unison runs, orchestra hits, anticipated ("kui") melodies."""
from engine import Song

TRUMPET, STRINGS, BRASS, DIST, OVERDRIVE, SAW = 56, 48, 61, 30, 29, 81
PICKBASS, SLAPBASS, PIANO, HARPSI, ORCHHIT = 34, 36, 0, 6, 55
ROCKORGAN, CHURCHORGAN, CHOIR, TIMPANI = 18, 19, 52, 47


# ---------------------------------------------------------------------------
# 5. Warden of the Deep Gate -- G minor, opens on a solo slap-bass riff
# ---------------------------------------------------------------------------
def warden():
    s = Song('Warden of the Deep Gate', 162, 16, 'g a bb c d eb f', {
        'tp': (0, TRUMPET, 110, 56), 'vn': (1, STRINGS, 98, 72),
        'gtr': (2, OVERDRIVE, 66, 34), 'bass': (3, SLAPBASS, 118, 64),
        'pad': (4, STRINGS, 72, 86), 'arp': (5, PIANO, 92, 44),
        'stab': (6, BRASS, 86, 78), 'timp': (7, TIMPANI, 104, 64),
        'syn': (8, SAW, 62, 50), 'hit': (10, ORCHHIT, 84, 64),
        'drums': (9, 0, 112, 64)}, seed=5)
    riff = ('g1.2 g2.1 g1.1 r.1 g1.1 f2.1 g2.1 r.1 g1.1 bb1.1 c2.1 d2.2 f2.1 d2.1 |'
            'g1.2 g2.1 g1.1 r.1 g1.1 f2.1 g2.1 r.1 eb2.1 d2.1 c2.1 bb1.1 c2.1 d2.1 f2.1')

    def intro():
        s.section('Gm | Gm', lines=[(riff, [('bass', 0, 1.0)])],
                  drums='hat', fill=False, crash=False)
        s.section('Gm | Gm', lines=[(riff, [('bass', 0, 1.0), ('gtr', 12, 0.9)])],
                  drums='16beat', pad='sus', stabs='change')
        s.section('Gm | Eb F | Gm | Eb F',
                  'g5.6 d5.2 g5.2 a5.2 bb5.4 | bb5.6 g5.2 a5.6 c6.2 |'
                  'd6.6 bb5.2 d6.2 eb6.2 d6.4 | eb6.4 d6.2 bb5.2 c6.2 a5.2 f5.2 a5.2',
                  lead=[('tp', 0, 1.0), ('syn', 0, 0.8)],
                  drums='16beat', bass='16', gtr='power', pad='sus', stabs='change',
                  timp=True)

    a = ('d5.2 g5.4 a5.2 bb5.4 a5.2 g5.2 | d6.6 c6.2 bb5.4 a5.2 bb5.2 |'
         '-.6 g5.2 eb5.2 g5.2 bb5.2 c6.2 | -.6 a5.2 f5.4 a5.2 c6.2 |'
         'd6.2 g6.4 f6.2 d6.4 bb5.2 d6.2 | f6.6 d6.2 bb5.4 g5.2 bb5.2 |'
         '-.4 c6.2 bb5.2 g5.2 bb5.2 eb6.2 d6.2 | -.6 c6.2 a5.2 f#5.2 a5.2 d6.2')
    a_ch = 'Gm | Gm | Eb | F | Gm | Gm | Eb | D'

    def body():
        s.section(a_ch, a, lead=[('tp', 0, 1.0)],
                  drums='drive', bass='16', gtr='chug', pad='stacc', stabs='change')
        s.section(a_ch, a, lead=[('tp', 0, 1.0), ('syn', 0, 0.75), ('vn', 12, 0.6)],
                  drums='drive', bass='16', gtr='chug', pad='kizami', stabs='sync')
        s.section('Cm | D | Gm | Gm | Cm | F | Bb | D',
                  'eb5.8 g5.4 c6.4 | a5.6 f#5.2 d5.8 | bb5.3 a5.3 g5.2 d5.8 |'
                  'r.2 g5.2 a5.2 bb5.2 d6.4 bb5.4 | c6.8 eb6.4 g6.4 | f6.6 eb6.2 c6.4 a5.4 |'
                  'd6.3 c6.3 bb5.2 f5.4 bb5.4 |'
                  'a5.8 f#5.1 g5.1 a5.1 bb5.1 c6.1 d6.1 e6.1 f#6.1',
                  lead=[('vn', 0, 1.0), ('vn', 12, 0.7)],
                  drums='half', bass='8oct', gtr='power', pad='sus', arp='wave', timp=True)
        s.section('Gm | F | Eb | D | Gm | F | Eb F | G',
                  'g6.6 d6.2 bb5.2 d6.2 g6.4 | f6.6 c6.2 a5.2 c6.2 f6.4 |'
                  'eb6.4 g6.4 f6.2 eb6.2 d6.2 eb6.2 | d6.8 a5.2 d6.2 f#6.4 |'
                  'g6.6 d6.2 bb5.2 d6.2 g6.4 | a6.6 f6.2 c6.2 f6.2 a6.4 |'
                  'g6.4 eb6.2 g6.2 a6.4 f6.2 a6.2 | d6.4 g6.4 b6.8',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0), ('syn', -12, 0.8)],
                  drums='dbeat', bass='16', gtr='chug', pad='sus', stabs='sync', timp=True)
    return s, intro, body, 4


# ---------------------------------------------------------------------------
# 6. Scarlet Tempest -- B minor, unison 16th-note run, Andalusian verse
# ---------------------------------------------------------------------------
def scarlet_tempest():
    s = Song('Scarlet Tempest', 192, 16, 'b c# d e f# g a', {
        'ld': (0, DIST, 100, 54), 'ld2': (1, DIST, 84, 80),
        'gtr': (2, DIST, 70, 30), 'bass': (3, PICKBASS, 116, 64),
        'pad': (4, STRINGS, 74, 88), 'stab': (6, BRASS, 84, 76),
        'timp': (7, TIMPANI, 102, 64), 'tp': (8, TRUMPET, 100, 66),
        'hit': (10, ORCHHIT, 84, 64), 'vn': (11, STRINGS, 100, 44),
        'drums': (9, 0, 114, 64)}, seed=6)

    def run():
        s.section('Bm | F#',
                  'b4.1 c#5.1 d5.1 b4.1 c#5.1 d5.1 e5.1 c#5.1 '
                  'd5.1 e5.1 f#5.1 d5.1 e5.1 f#5.1 g5.1 e5.1 |'
                  'f#5.1 g5.1 a#5.1 f#5.1 g5.1 a#5.1 b5.1 g5.1 '
                  'a#5.1 b5.1 c#6.1 a#5.1 b5.1 c#6.1 d6.1 b5.1',
                  lead=[('ld', -12, 1.0), ('ld2', 0, 0.8), ('bass', -36, 1.0), ('vn', 0, 0.8)],
                  drums='four', pad='sus', fill=False)
        s.section('G A | Bm',
                  'd6.3 d6.3 d6.2 e6.2 e6.2 e6.4 | f#6.3 f#6.3 f#6.2 f#6.2 f#6.2 f#6.4',
                  lead=[('ld', -12, 1.0), ('ld2', -24, 0.9), ('vn', 0, 0.9)],
                  hits='x..x..x.x.x.x...', timp=True)

    a = ('f#5.4 b5.2 d6.6 c#6.2 b5.2 | c#6.4 a5.2 e5.6 a5.2 c#6.2 |'
         'd6.4 b5.2 g5.6 b5.2 d6.2 | c#6.6 a#5.2 f#5.4 a#5.2 c#6.2 |'
         'd6.4 f#6.2 f#6.6 e6.2 d6.2 | e6.4 c#6.2 a5.6 c#6.2 e6.2 |'
         'g6.4 f#6.2 d6.4 b5.2 d6.2 g6.2 | f#6.8 e6.2 c#6.2 a#5.2 c#6.2')
    a_ch = 'Bm | A | G | F# | Bm | A | G | F#'

    def body():
        s.section(a_ch, a, lead=[('ld', -12, 1.0)],
                  drums='dbeat', bass='16', gtr='chug', pad='sus')
        s.section(a_ch, a, lead=[('ld', -12, 1.0), ('tp', -12, 0.85)],
                  drums='dbeat', bass='16', gtr='chug', pad='kizami', stabs='change')
        s.section('Em | F#m | G | A | Em | F#m | G A | B',
                  'g5.6 e5.2 g5.4 b5.4 | a5.6 f#5.2 a5.4 c#6.4 | b5.6 g5.2 b5.4 d6.4 |'
                  'e6.8 c#6.4 a5.4 | g6.6 e6.2 b5.4 e6.4 | a6.6 f#6.2 c#6.4 f#6.4 |'
                  'd6.4 g6.4 e6.4 a6.4 | f#6.6 d#6.2 b5.2 d#6.2 f#6.2 b6.2',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0)],
                  drums='rock', bass='8oct', gtr='power', pad='stacc', timp=True)
        s.section('Bm | D | A | E | G | A | Bm | F#',
                  'b5.2 d6.2 f#6.8 e6.2 d6.2 | a6.6 f#6.2 d6.4 f#6.4 |'
                  'e6.2 c#6.2 e6.8 d6.2 c#6.2 | b5.6 e6.2 g#6.8 |'
                  'd6.2 g6.2 b6.8 a6.2 g6.2 | a6.6 e6.2 c#6.4 e6.4 |'
                  'f#6.3 e6.3 d6.2 c#6.3 d6.3 b5.2 | a#5.4 c#6.4 f#6.8',
                  lead=[('ld', -12, 1.0), ('ld2', 'third', 0.9), ('vn', 0, 0.6)],
                  harmony=-12,
                  drums='double', bass='16', gtr='chug', pad='sus', stabs='sync')
        run()
    return s, run, body, 4


# ---------------------------------------------------------------------------
# 7. Lord of the Black Keep -- F minor, heavy 16-beat groove, organ and brass
# ---------------------------------------------------------------------------
def black_keep():
    s = Song('Lord of the Black Keep', 140, 16, 'f g ab bb c db eb', {
        'tp': (0, TRUMPET, 108, 58), 'br': (1, BRASS, 92, 70),
        'gtr': (2, OVERDRIVE, 70, 32), 'bass': (3, SLAPBASS, 118, 64),
        'pad': (4, ROCKORGAN, 70, 90), 'arp': (5, HARPSI, 90, 42),
        'stab': (6, BRASS, 84, 78), 'timp': (7, TIMPANI, 104, 64),
        'vn': (8, STRINGS, 104, 46), 'hit': (10, ORCHHIT, 84, 64),
        'drums': (9, 0, 114, 64)}, seed=7)
    riff = ('f1.3 f1.1 r.2 ab1.2 bb1.3 bb1.1 r.2 c2.1 eb2.1 |'
            'f1.3 f1.1 r.2 ab1.2 bb1.2 b1.2 c2.2 eb2.1 c2.1')
    rv = [('bass', 0, 1.0), ('gtr', 12, 0.95), ('gtr', 19, 0.8)]

    def intro():
        s.section('Fm | Fm', lines=[(riff, rv)], drums='hat', fill=False)
        s.section('Fm | Fm', 'r.8 c5.2 eb5.2 f5.4 | ab5.6 g5.2 f5.2 eb5.2 c5.4',
                  lead=[('br', 0, 1.0), ('tp', 0, 0.9)],
                  lines=[(riff, rv)], drums='16beat', pad='sus')

    def body():
        s.section('Fm | Fm | Fm | Fm',
                  'c5.2 f5.2 r.1 ab5.3 g5.2 f5.2 r.2 eb5.2 | f5.6 r.2 c5.2 eb5.2 f5.2 ab5.2 |'
                  'bb5.2 ab5.2 r.1 f5.3 ab5.2 bb5.2 r.2 c6.2 | c6.8 r.2 bb5.2 ab5.2 g5.2',
                  lead=[('tp', 0, 1.0), ('br', 0, 0.8)],
                  lines=[(riff + '|' + riff, rv)], drums='16beat', pad='sus', fill=False)
        s.section('Db | Eb | Fm | C',
                  'ab5.6 f5.2 db5.4 f5.2 ab5.2 | bb5.6 g5.2 eb5.4 g5.2 bb5.2 |'
                  'c6.3 bb5.3 ab5.2 c6.3 eb6.3 f6.2 | e6.8 c6.2 g5.2 c6.2 e6.2',
                  lead=[('tp', 0, 1.0), ('br', 0, 0.8)],
                  drums='16beat', bass='16', gtr='power', pad='sus', stabs='sync')
        s.section('Bbm | Eb | Ab | Db | Bbm | C | Fm | C7',
                  'db6.6 bb5.2 f5.8 | g5.4 bb5.4 eb6.6 db6.2 | c6.6 ab5.2 eb5.8 |'
                  'f5.4 ab5.4 db6.6 c6.2 | bb5.3 c6.3 db6.2 f6.6 eb6.2 | e6.6 c6.2 g5.4 c6.4 |'
                  'ab5.3 g5.3 f5.2 c6.8 | r.2 c6.2 e6.2 g6.2 bb6.2 g6.2 e6.2 c6.2',
                  lead=[('vn', 0, 1.0), ('vn', -12, 0.8)],
                  drums='half', bass='8oct', gtr='power', pad='sus', arp='up', timp=True)
        s.section('Db | Eb | Fm | Fm | Db | Eb | C | C',
                  'f6.6 db6.2 ab5.4 db6.4 | g6.6 eb6.2 bb5.4 eb6.4 |'
                  'ab6.8 g6.2 f6.2 eb6.2 f6.2 | c6.10 r.2 c6.2 eb6.2 |'
                  'f6.6 ab6.2 ab6.4 f6.4 | g6.6 bb6.2 bb6.4 g6.4 |'
                  'g6.3 e6.3 c6.2 e6.3 g6.3 c6.2 | e6.8 r.8',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0), ('br', -12, 0.85)],
                  drums='drive', bass='16', gtr='chug', pad='sus', stabs='sync', timp=True)
    return s, intro, body, 4


# ---------------------------------------------------------------------------
# 8. The Last Dawn -- F# minor final battle, closing each loop in F# major
# ---------------------------------------------------------------------------
def last_dawn():
    s = Song('The Last Dawn', 178, 16, 'f# g# a b c# d e', {
        'vn': (0, STRINGS, 114, 58), 'tp': (1, TRUMPET, 104, 72),
        'gtr': (2, DIST, 62, 34), 'bass': (3, PICKBASS, 114, 64),
        'pad': (4, STRINGS, 70, 86), 'arp': (5, PIANO, 100, 44),
        'stab': (6, BRASS, 86, 78), 'timp': (7, TIMPANI, 108, 64),
        'org': (8, CHURCHORGAN, 96, 64), 'choir': (10, CHOIR, 70, 64),
        'hit': (11, ORCHHIT, 80, 64), 'drums': (9, 0, 112, 64)}, seed=8)

    def intro():
        s.section('F#m | D | Bm | C#',
                  'c#5.8 f#5.8 | a5.12 f#5.4 | d5.8 b5.8 | g#5.12 f5.4',
                  lead=[('org', 0, 1.0), ('org', -12, 0.9)], lead_vel=98,
                  pad='sus', bass='long', timp=True, fill=False)
        s.section('C# | C#',
                  'c#5.1 g#5.1 c#6.1 g#5.1 c#5.1 g#5.1 c#6.1 g#5.1 '
                  'c#5.1 g#5.1 c#6.1 g#5.1 c#5.1 g#5.1 c#6.1 g#5.1 |'
                  'c#5.1 d5.1 f5.1 f#5.1 g#5.1 a5.1 b5.1 c#6.1 '
                  'd6.1 f6.1 f#6.1 g#6.1 a6.1 g#6.1 f#6.1 f6.1',
                  lead=[('vn', 0, 1.0), ('vn', -12, 0.9), ('arp', 0, 0.8)],
                  hits='x..x..x.x..x..x.', timp=True)

    a = ('c#6.6 a5.2 f#5.4 a5.2 c#6.2 | d6.4 f#6.4 e6.2 d6.2 a5.4 |'
         'e6.6 b5.2 g#5.4 b5.2 e6.2 | e6.3 d6.3 c#6.10 |'
         'f#6.6 d6.2 a5.4 d6.2 f#6.2 | g#6.4 e6.4 b5.2 e6.2 g#6.4 |'
         'a6.6 g#6.2 f#6.4 c#6.4 | f6.8 c#6.2 f6.2 g#6.4')
    a_ch = 'F#m | D | E | C#m | D | E | F#m | C#'

    def body():
        s.section(a_ch, a, lead=[('tp', -12, 1.0), ('vn', 0, 0.8)],
                  drums='drive', bass='16', gtr='chug', pad='stacc', stabs='change')
        s.section(a_ch, a, lead=[('vn', 0, 1.0), ('tp', -12, 1.0)],
                  drums='dbeat', bass='16', gtr='chug', pad='sus', arp='up', stabs='sync')
        s.section('A | E | F#m | C#m | D | A | Bm | C#',
                  'c#6.8 e6.4 a6.4 | g#6.6 e6.2 b5.8 | a5.8 c#6.4 f#6.4 | e6.6 c#6.2 g#5.8 |'
                  'f#5.4 a5.4 d6.6 e6.2 | c#6.6 a5.2 e5.4 a5.4 |'
                  'b5.3 c#6.3 d6.2 f#6.6 e6.2 | f6.8 g#5.2 c#6.2 f6.2 g#6.2',
                  lead=[('vn', 0, 1.0), ('org', -12, 0.8)],
                  drums='half', bass='8oct', gtr='power', pad='sus', arp='wave', timp=True)
        s.section('D | E | C#m | F#m | D | E | F# | F#',
                  'a6.6 f#6.2 f#6.2 e6.2 f#6.4 | g#6.6 e6.2 e6.2 f#6.2 g#6.4 |'
                  'g#6.4 e6.2 c#6.2 e6.4 g#6.4 | a6.10 r.2 f#6.2 a6.2 |'
                  'a6.6 f#6.2 d6.2 f#6.2 a6.4 | b6.6 g#6.2 e6.2 g#6.2 b6.4 |'
                  'a#6.8 f#6.4 c#6.4 | a#5.2 c#6.2 f#6.2 a#6.2 f#6.8',
                  lead=[('vn', 0, 1.0), ('tp', -12, 1.0), ('org', -12, 0.7)],
                  drums='double', bass='16', gtr='chug', pad='sus', stabs='sync', timp=True)
        s.section('F#m | F#m | C# | C#', 'c#6.16 | -.16 | f6.16 | -.8 g#6.8',
                  lead=[('tp', -12, 1.0), ('org', -12, 0.8)],
                  drums='dbeat', bass='gallop', gtr='chug', pad='kizami', timp=True)
    return s, intro, body, 4


SONGS = [
    ('05_warden_of_the_deep_gate', warden),
    ('06_scarlet_tempest', scarlet_tempest),
    ('07_lord_of_the_black_keep', black_keep),
    ('08_the_last_dawn', last_dawn),
]
