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


def synthesize(text: str, voice: str, style: str, model: str) -> bytes:
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
