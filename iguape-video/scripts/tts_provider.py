"""Provedor de TTS (Gemini). Troque este arquivo para usar outro provedor.

synthesize(text, voice, style, model) -> bytes de um WAV (24 kHz, mono, 16 bits).
"""
import base64
import io
import os
import wave


class QuotaError(Exception):
    """Cota esgotada (RESOURCE_EXHAUSTED / 429)."""


class TransientError(Exception):
    """Erro temporário; vale tentar de novo."""


def _wrap_pcm(pcm: bytes) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(pcm)
    return buf.getvalue()


def synthesize_elevenlabs(text: str, voice_id: str, model: str) -> bytes:
    import json
    import subprocess
    import urllib.error
    import urllib.request

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": model, "language_code": "pt"}).encode(),
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"},
    )
    try:
        mp3 = urllib.request.urlopen(req, timeout=120).read()
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        if e.code == 429 or "quota_exceeded" in body:
            raise QuotaError(f"{e.code}: {body}") from None
        if e.code >= 500:
            raise TransientError(f"{e.code}: {body}") from None
        raise RuntimeError(f"{e.code}: {body}") from None
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-ar", "24000", "-ac", "1", "-f", "wav", "pipe:1"],
                       input=mp3, capture_output=True, check=True)
    return r.stdout


def synthesize(text: str, voice: str, style: str, model: str) -> bytes:
    if os.environ.get("TTS_PROVIDER") == "elevenlabs":
        return synthesize_elevenlabs(text, voice, model)
    from google import genai

    # A chave é passada explicitamente; nunca é impressa nem registrada.
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    try:
        interaction = client.interactions.create(
            model=model,
            input=[
                {
                    "type": "user_input",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                            "annotations": [{"type": "speech_metadata", "style": style}],
                        }
                    ],
                }
            ],
            response_format={"type": "audio"},
            generation_config={"speech_config": [{"voice": voice}]},
        )
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
            raise QuotaError(msg[:300]) from None
        if any(c in msg for c in ("500", "502", "503", "504", "UNAVAILABLE", "DEADLINE", "timed out")):
            raise TransientError(msg[:300]) from None
        raise RuntimeError(msg[:500]) from None

    data = interaction.output_audio.data
    raw = base64.b64decode(data) if isinstance(data, str) else bytes(data)
    return raw if raw[:4] == b"RIFF" else _wrap_pcm(raw)
