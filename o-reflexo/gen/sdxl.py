"""Geração de imagens com SDXL 1.0 + LCM-LoRA em CPU (modelos abertos, OpenRAIL++-M).
Uso: python3 gen/sdxl.py <saida.png> "<prompt>" [--w 1024 --h 1024 --steps 6 --seed 7 --init img.png --strength 0.5]
A protagonista tem uma descrição fixa (IDENT) que entra em todos os prompts de pessoa."""
import argparse, os, sys, time
import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, LCMScheduler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = f"{ROOT}/models"
IDENT = ("a 24 year old brazilian woman named Clara, shoulder-length straight dark brown hair with a center part, "
         "pale olive skin, light freckles across the nose, thin dark eyebrows, dark brown eyes, small mole under left eye, "
         "no makeup, tired eyes, wearing an oversized faded gray hoodie")
STYLE = ("candid amateur photo, natural skin texture, pores, imperfect, realistic, unflattering bathroom light, "
         "shot on a cheap phone, slight noise")
NEG = ("cartoon, 3d render, illustration, painting, doll, plastic skin, airbrushed, beauty filter, makeup, "
       "watermark, text, deformed, extra fingers, blurry face, cgi, glamour, model, studio lighting")

_pipe = {}
def pipe(img2img=False):
    k = "i2i" if img2img else "t2i"
    if k in _pipe: return _pipe[k]
    torch.set_num_threads(os.cpu_count())
    base = _pipe.get("t2i")
    if base is None:
        base = StableDiffusionXLPipeline.from_pretrained(f"{M}/sdxl", torch_dtype=torch.bfloat16, variant="fp16", use_safetensors=True)
        base.load_lora_weights(f"{M}/lcm-lora-sdxl"); base.fuse_lora()
        base.scheduler = LCMScheduler.from_config(base.scheduler.config)
        base.set_progress_bar_config(disable=True)
        _pipe["t2i"] = base
    if img2img:
        p = StableDiffusionXLImg2ImgPipeline(**base.components); p.set_progress_bar_config(disable=True); _pipe["i2i"] = p
    return _pipe[k]

def gen(out, prompt, w=1024, h=1024, steps=6, seed=7, guidance=1.5, init=None, strength=0.5, neg=NEG):
    t = time.time(); g = torch.Generator().manual_seed(seed)
    if init:
        from PIL import Image
        im = Image.open(init).convert("RGB").resize((w, h))
        r = pipe(True)(prompt=prompt, negative_prompt=neg, image=im, strength=strength, num_inference_steps=steps, guidance_scale=guidance, generator=g)
    else:
        r = pipe()(prompt=prompt, negative_prompt=neg, width=w, height=h, num_inference_steps=steps, guidance_scale=guidance, generator=g)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    r.images[0].save(out); print("GEN", out, round(time.time() - t, 1), "s", flush=True)

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("out"); a.add_argument("prompt")
    for k, v in (("w", 1024), ("h", 1024), ("steps", 6), ("seed", 7)): a.add_argument(f"--{k}", type=int, default=v)
    a.add_argument("--guidance", type=float, default=1.5); a.add_argument("--init"); a.add_argument("--strength", type=float, default=0.5)
    o = a.parse_args()
    gen(o.out, o.prompt.replace("{IDENT}", IDENT).replace("{STYLE}", STYLE), o.w, o.h, o.steps, o.seed, o.guidance, o.init, o.strength)
