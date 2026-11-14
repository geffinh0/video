"""Direção de atuação dos rostos: curvas por plano (tempo u em segundos desde o início da gravação do plano).
"real" = Clara; "refl" = o reflexo. Mesma aparência, comportamento divergente."""

def define(shot, k):
    bump, blinks, ease, hold, wobble, speech = (k[n] for n in ("bump", "blinks", "ease", "hold", "wobble", "speech"))

    # ---------------- S02 PRIMEIRA ANOMALIA (celular, 15 fps) ----------------
    RB = [1.2, 4.0, 8.0, 9.6, 13.2, 18.0, 23.5]            # piscadas de Clara
    FB = [1.2, 4.25, 8.45, 10.3, 13.95]                    # reflexo: atrasos crescentes, e depois para de piscar
    def s02_real(u):
        look = hold(u, [(11.4, 11.8, 0, 1), (13.4, 13.9, 1, 0)])          # olha o celular e volta
        return dict(blink=blinks(u, RB, 0.26), mouth=max(speech(u, "v_denovo", 5.4, 0.55), speech(u, "v_camera", 14.5, 0.5)),
                    gaze=(-14 * look, -4 * look), yaw=wobble(u, 1, 1.6) - 6 * look, pitch=wobble(u, 2, 1.2) - 3 * look, roll=wobble(u, 3, 0.8))
    def s02_refl(u):
        tilt = hold(u, [(19.8, 22.5, 0, 1), (23.4, 24.2, 1, 0)])           # inclina a cabeça sozinho
        stare = hold(u, [(25.4, 26.0, 0, 1)])                               # no fim, os olhos procuram a câmera
        return dict(blink=blinks(u, FB, 0.26), mouth=max(speech(u, "v_denovo", 5.4, 0.5), speech(u, "v_camera", 14.65, 0.45)),
                    gaze=(10 * stare, 2 * stare), yaw=-wobble(u, 1, 1.6), pitch=wobble(u, 2, 1.2), roll=-wobble(u, 3, 0.8) + 4 * tilt)
    shot("s02", "s02_comp", 15, 27, [dict(box=(540, 135, 840, 495), fn=s02_real), dict(box=(1080, 195, 1290, 405), fn=s02_refl)])

    # ---------------- S03 OBSERVAÇÃO (CCTV, 4 fps) ----------------
    # normal: Clara olha o espelho e o reflexo olha para ela. 6.3–11.25: ela olha a porta; o reflexo encara a câmera.
    def door(u): return hold(u, [(6.0, 6.6, 0, 1), (11.0, 11.5, 1, 0)])
    def s03_real(u):
        d = door(u); return dict(yaw=-22 * (1 - d) + wobble(u, 5, 1), gaze=(-10 * (1 - d), 0), blink=blinks(u, [2.5, 9.0, 16.0], 0.3))
    def s03_refl(u):
        a = hold(u, [(6.25, 6.5, 0, 1), (11.25, 11.5, 1, 0)])              # o reflexo vira um quadro depois
        return dict(yaw=16 * (1 - a), gaze=(12 * (1 - a), 0), pitch=-3 * a, blink=blinks(u, [2.5, 16.0], 0.3))
    shot("s03", "cctv_mirror2", 4, 22, [dict(box=(825, 205, 900, 330), fn=s03_real), dict(box=(685, 345, 765, 440), fn=s03_refl)])

    # ---------------- S04 O SORRISO (celular colado ao espelho, 15 fps) ----------------
    def s04_refl(u):
        sm = 1.0 * ease(u, 3.5, 11.0) + 0.3 * ease(u, 15.2, 16.4)
        fear = 1 - ease(u, 3.5, 8.0)
        return dict(smile=sm, brow=7 * fear, blink=blinks(u, [0.9, 2.4], 0.24), gaze=(wobble(u, 7, 2.5, 1.6) * fear, 0),
                    yaw=wobble(u, 8, 1.4), pitch=wobble(u, 9, 1.0), roll=1.5 * ease(u, 10, 12))
    shot("s04", "s04_comp", 15, 17, [dict(box=(330, 0, 1010, 760), fn=s04_refl)])

    # ---------------- S05 A GRAVAÇÃO FINAL: espelho (15 fps) ----------------
    def s05_refl(u):
        return dict(mouth=speech(u, "v_ouvindo", 3.5, 0.45), blink=blinks(u, [2.0], 0.3), roll=-5 * ease(u, 9.0, 12.5),
                    pitch=-2 * ease(u, 9.0, 12.5), smile=0.35 * ease(u, 17.0, 20.5), yaw=wobble(u, 11, 0.6) * (1 - ease(u, 6, 7)))
    shot("s05", "s05_a", 15, 21, [dict(box=(555, 220, 715, 460), fn=s05_refl)])

    # ---------------- S05 câmera caída: ela ao fundo vira e encara o celular (15 fps) ----------------
    def s05_floor(u):
        t = ease(u, 2.5, 5.0)
        return dict(yaw=-14 * t, pitch=7 * t, gaze=(-14 * t, 8 * t), blink=0.0)
    shot("s05_floor", "s05_floor", 15, 8, [dict(box=(790, 105, 880, 285), fn=s05_floor)])

    # ---------------- S06 ÚLTIMO REGISTRO (CCTV, 4 fps): o reflexo sozinho ----------------
    def s06_refl(u):
        return dict(smile=1.2 * ease(u, 6.0, 10.0), roll=2.5 * ease(u, 2, 5), pitch=-3, blink=0.0)
    shot("s06", "s06_comp", 4, 14, [dict(box=(685, 345, 765, 440), fn=s06_refl)])
