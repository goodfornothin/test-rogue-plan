# Rogue Bachata logo loops

Three looping animations of the Rogue Bachata RB logo in hot pink and electric blue, made to sit on top of dark club footage.

| File | Look |
|---|---|
| `RogueBachata_Logo_Loop_v1_Neon_1080x1920_60s_black.mp4` | Neon-tube RB with pink/blue colour rolling across it. Sparks race round the tubes, letters flicker now and then, and a chrome shine sweeps across every 10s. |
| `RogueBachata_Logo_Loop_v2_Lightshow_1080x1920_60s_black.mp4` | Liquid pink/cyan fill with god-rays bursting from behind the logo and rising glitter. Club lasers run through four 15s scenes: fan, scissors, corner beams and a spinning sunburst. |
| `RogueBachata_Logo_Loop_v3_Duet_1080x1920_60s_black.mp4` | A pink partner and a blue partner orbit each other like a bachata turn. Every 7.5s they snap together into a white-hot hit with shockwave rings and a quick glitch. |

- 1080×1920 (9:16), 30 fps, H.264 MP4, exactly 60 s.
- **Seamless loop:** the last frame flows straight into the first, so you can repeat the clip back-to-back for as long as you need.
- **Pure black background (0,0,0).** Put the clip on an overlay layer above your club video and set the blend mode to **Screen** (Lighten or Add work too). The black disappears and only the light stays. Don't use Color Burn or Linear Burn: they darken the video instead.
- Timings are built on 128 BPM (16 beats = 7.5 s), so the hits fall on a steady grid you can line up with the track.

## Re-rendering

```
pip install opencv-python-headless numpy
python3 render_logo_loops.py            # all three
python3 render_logo_loops.py v2         # just one
python3 render_logo_loops.py v1 --preview 0 12.5   # PNG stills at given seconds
```

The source art is `images/Rogue Bachata Logo _transparent_.png`.
