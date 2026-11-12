# bgms

オリジナルのボスバトルBGM集（90年代JRPGのバトル曲の語法で書いた自作曲）。

| # | 曲名 | キー / 拍子 / BPM | 特徴 | ループ区間 |
|---|------|------------------|------|-----------|
| 1 | 宿命の刃 (`01_blade_of_fate`) | Dm / 4/4 / 170 | トランペット＋ストリングス主旋律、16分ベース | 5.65s – 50.82s |
| 2 | 紅蓮の咆哮 (`02_crimson_roar`) | Em / 4/4 / 184 | ペダルリフ、ツインギター、ツーバス | 5.22s – 41.74s |
| 3 | 深淵の玉座 (`03_throne_of_abyss`) | Cm / 6/8 / 188 | オルガン＋チェンバロ、五度圏進行 | 7.66s – 53.62s |
| 4 | 終焉のレクイエム (`04_requiem_of_the_end`) | Am→Dm→D / 4/4 / 176 | ラスボス曲。終盤にニ長調の「希望」主題 | 8.18s – 62.73s |

- `mp3/` … イントロ → ループ2周 → フェードアウトの試聴用音源
- `midi/` … 同内容のMIDI（GM配列）
- `src/` … 生成スクリプト。旋律とコードは `src/songs.py` に手書き、伴奏は `src/engine.py` がコードから展開

## ビルド

```bash
pip install mido
apt-get install -y fluidsynth fluid-soundfont-gm ffmpeg
python3 src/make.py            # MIDI + MP3
python3 src/make.py --midi-only
```

## マインドフルネス用: 静かな水面 (`mp3/still_water.mp3`)

約6分のアンビエント曲。打楽器なし、ニ長調、サイン波系のパッドと柔らかいベル、呼吸のようなノイズだけで構成。
全体が11秒周期（5.5秒でふくらみ、5.5秒でしぼむ）でゆっくり揺れ、和音は2周期ごとに変わる。

```bash
pip install numpy
python3 src/mindful.py
```

### オルゴール版 (`mp3/still_water_orgel.mp3`)

約3分45秒、3/4拍子の子守唄ふう。1小節2.75秒で、4小節のフレーズが11秒の呼吸周期にあたる。
旋律とコードは手書き、櫛歯の音は加算合成。最後の8小節はゼンマイが切れるように遅くなる。

```bash
cd src && python3 orgel.py
```
