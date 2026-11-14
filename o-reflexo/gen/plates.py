"""Gera as imagens-base (plates) de cada plano. Retomável: pula o que já existe.
Uso: python3 gen/plates.py [nome ...]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sdxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/assets/plates"
WOMAN = "young woman, shoulder-length straight dark brown hair, center part, light freckles, oversized faded gray hoodie"
CCTV = ("cctv security camera still, high angle from upper ceiling corner, wide angle lens, small old bathroom at night, "
        "white square tiles, sink with large wall mirror on the right wall, door ajar on the left, dim fluorescent light, grainy, low quality")
PHONE = "amateur phone camera photo, dim bathroom at night, single warm bulb, grainy, slightly blurry, realistic, candid"

PLATES = {
    # nome: (prompt, w, h, seed, init, strength)
    "cctv_empty": (f"{CCTV}, empty room, nobody", 1344, 768, 21, None, 0),
    "s02_a": (f"{WOMAN}, side profile very close to the camera at left edge, looking at her own reflection in a bathroom mirror, her face reflection clearly visible in the mirror at right, {PHONE}", 1344, 768, 31, None, 0),
    "s02_b": (f"{WOMAN}, side profile very close to the camera at left edge, looking at her own reflection in a bathroom mirror, her face reflection clearly visible in the mirror at right, {PHONE}", 1344, 768, 32, None, 0),
    "s02_c": (f"{WOMAN}, side profile very close to the camera at left edge, looking at her own reflection in a bathroom mirror, her face reflection clearly visible in the mirror at right, {PHONE}", 1344, 768, 33, None, 0),
    "s04": (f"extreme close-up of a bathroom mirror, reflection of a {WOMAN} face filling the frame, serious frightened expression, looking into the lens, smudges and water spots on the glass, {PHONE}", 1344, 768, 41, None, 0),
    "s05_a": (f"over the shoulder view from behind a {WOMAN}, standing in front of a fogged bathroom mirror, her face reflection visible in the steamy mirror looking at the camera, very dark, {PHONE}", 1344, 768, 51, None, 0),
    "s05_b": (f"over the shoulder view from behind a {WOMAN}, standing in front of a fogged bathroom mirror, her face reflection visible in the steamy mirror looking at the camera, very dark, {PHONE}", 1344, 768, 52, None, 0),
    "s05_floor": (f"phone dropped on a bathroom floor, extreme low angle across white floor tiles, shallow focus, sink cabinet and wall mirror far in the background, the face of a {WOMAN} reflected in the mirror staring at the camera, dark, {PHONE}", 1344, 768, 55, None, 0),
    "hand": ("macro photo of one open human hand only, palm facing the camera, five fingers spread, wrist with gray sleeve cuff at the bottom edge, hand centered, pure black background, soft dim light, realistic skin, hand model photo", 768, 1024, 62, None, 0),
}

# CCTV com a protagonista: inpainting sobre o plano vazio (enquadramento idêntico entre os quadros)
INPAINT = {
    "cctv_mirror": (f"a {WOMAN} standing at the sink seen from behind and above, facing the wall mirror, her face reflection visible in the mirror, cctv still, grainy", (680, 140, 990, 740), 22),
    "cctv_mirror2": (f"a {WOMAN} standing at the sink seen from behind and above, facing the wall mirror, her face reflection visible in the mirror, cctv still, grainy", (680, 140, 990, 740), 27),
    "cctv_enter": (f"a {WOMAN} stepping into the bathroom through the door, full body, cctv still, grainy", (960, 120, 1250, 768), 23),
    "cctv_walk": (f"a {WOMAN} walking across the bathroom toward the sink, full body, cctv still, grainy", (800, 200, 1100, 768), 25),
    "cctv_leave": (f"a {WOMAN} walking out through the door seen from behind, full body, cctv still, grainy", (960, 120, 1250, 768), 24),
}

if __name__ == "__main__":
    for n, (p, box, seed) in INPAINT.items():
        out = f"{OUT}/{n}.png"
        if not os.path.exists(out) and (not sys.argv[1:] or n in sys.argv[1:]): sdxl.inpaint(out, p, f"{OUT}/cctv_empty.png", box, seed=seed)
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(PLATES)
    for n in names:
        p, w, h, seed, init, st = PLATES[n]; out = f"{OUT}/{n}.png"
        if os.path.exists(out): continue
        if init and not os.path.exists(f"{OUT}/{init}.png"): print("SKIP (sem init)", n); continue
        sdxl.gen(out, p, w, h, steps=7 if not init else 8, seed=seed, init=f"{OUT}/{init}.png" if init else None, strength=st)
    print("PLATES DONE", flush=True)
