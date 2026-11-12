"""Build MIDI + MP3 for every song: intro, loop x2, then a faded tail.

Needs: pip install mido; fluidsynth + a GM soundfont; ffmpeg.
"""
import os
import subprocess
import sys

from songs import SONGS as S1
from songs2 import SONGS as S2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = os.environ.get('SF2', '/usr/share/sounds/sf2/FluidR3_GM.sf2')


def build(name, factory):
    song, intro, body, tail_bars = factory()
    intro()
    loop_start = song.pos
    body()
    loop_end = song.pos
    body()
    body()
    cut = loop_end + (loop_end - loop_start) + tail_bars * song.bar
    os.makedirs(os.path.join(ROOT, 'midi'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'mp3'), exist_ok=True)
    mid = os.path.join(ROOT, 'midi', name + '.mid')
    song.write(mid, cut=cut)
    info = (name, song.title, song.bpm, song.seconds(loop_start),
            song.seconds(loop_end), song.seconds(cut))
    if '--midi-only' in sys.argv:
        return info
    wav = os.path.join(ROOT, 'mp3', name + '.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.7', '-r', '44100', '-F', wav, SF2, mid],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total = song.seconds(cut)
    fade = song.seconds(tail_bars * song.bar)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-t', '%.3f' % total,
                    '-af', 'afade=t=out:st=%.3f:d=%.3f,loudnorm=I=-14:TP=-1.0:LRA=9'
                    % (total - fade, fade),
                    '-ar', '44100', '-b:a', '192k', os.path.join(ROOT, 'mp3', name + '.mp3')],
                   check=True)
    os.remove(wav)
    return info


if __name__ == '__main__':
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for name, factory in S1 + S2:
        if only and not any(name.startswith(o) for o in only):
            continue
        n, title, bpm, ls, le, total = build(name, factory)
        print('%-24s %-22s bpm=%d loop=%.2fs..%.2fs total=%.1fs' % (n, title, bpm, ls, le, total))
