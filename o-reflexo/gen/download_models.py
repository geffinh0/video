"""Baixa os modelos abertos usados pelo filme (retomável). Pasta models/ é ignorada no git.
- SDXL 1.0 base (CreativeML OpenRAIL++-M), pesos fp16
- LCM-LoRA SDXL (OpenRAIL++-M) para 4-8 passos
- LivePortrait (MIT): só os módulos humanos + landmark.onnx (sem insightface)"""
import os
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from huggingface_hub import snapshot_download
M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
snapshot_download("stabilityai/stable-diffusion-xl-base-1.0", local_dir=f"{M}/sdxl",
    allow_patterns=["model_index.json", "scheduler/*", "tokenizer/*", "tokenizer_2/*",
                    "text_encoder/config.json", "text_encoder/model.fp16.safetensors",
                    "text_encoder_2/config.json", "text_encoder_2/model.fp16.safetensors",
                    "unet/config.json", "unet/diffusion_pytorch_model.fp16.safetensors",
                    "vae/config.json", "vae/diffusion_pytorch_model.fp16.safetensors"])
print("sdxl ok", flush=True)
snapshot_download("latent-consistency/lcm-lora-sdxl", local_dir=f"{M}/lcm-lora-sdxl")
print("lcm ok", flush=True)
snapshot_download("KwaiVGI/LivePortrait", local_dir=f"{M}/liveportrait",
    allow_patterns=["liveportrait/base_models/*", "liveportrait/retargeting_models/*", "liveportrait/landmark.onnx"])
print("liveportrait ok", flush=True)
