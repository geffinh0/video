import hashlib
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "tts-state.json"
PAUSE = "<short pause>"

STYLE = (
    "Narrador de documentário de história, jovem e envolvente, ritmo natural, "
    "clareza nos nomes e datas"
)
STYLE_TENSE = STYLE + ", um pouco mais tenso e dramático"
TENSE_SCENES = {5, 6}


def load_env():
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    return {
        "model": os.environ.get("GEMINI_TTS_MODEL", "gemini-3.8-flash-tts"),
        "voice": os.environ.get("GEMINI_VOICE", "Kore"),
        "rpm": int(os.environ.get("GEMINI_RPM", "3")),
        "rpd": int(os.environ.get("GEMINI_RPD", "10")),
        "has_key": bool(os.environ.get("GEMINI_API_KEY")),
    }


def pronuncia(text: str) -> str:
    p = ROOT / "src/data/pronuncia.json"
    mapping = json.loads(p.read_text()) if p.exists() else {}
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


def load_script():
    return json.loads((ROOT / "src/data/script.json").read_text())["scenes"]


def make_blocks():
    """Agrupa parágrafos da mesma cena em blocos de ~800-1100 caracteres."""
    blocks = []
    for sc in load_script():
        cur, cur_len, start = [], 0, 0
        paras = sc["paragraphs"]
        for i, p in enumerate(paras):
            if cur and cur_len + len(p) > 1100 and cur_len >= 500:
                blocks.append((sc["id"], start, cur))
                cur, cur_len, start = [], 0, i
            cur.append(p)
            cur_len += len(p) + 1
            if cur_len >= 800:
                blocks.append((sc["id"], start, cur))
                cur, cur_len, start = [], 0, i + 1
        if cur:
            if blocks and blocks[-1][0] == sc["id"] and cur_len < 350:
                sid, s, prev = blocks[-1]
                blocks[-1] = (sid, s, prev + cur)
            else:
                blocks.append((sc["id"], start, cur))
    out = []
    for n, (sid, s, paras) in enumerate(blocks, 1):
        out.append({
            "id": f"b{n:02d}",
            "scene": sid,
            "firstParagraph": s,
            "paragraphs": paras,
            "text": f"\n\n{PAUSE}\n\n".join(pronuncia(p) for p in paras),
            "style": STYLE_TENSE if sid in TENSE_SCENES else STYLE,
        })
    return out


def block_hash(text, voice, style, model):
    return hashlib.sha256("\x00".join([text, voice, style, model]).encode()).hexdigest()[:16]


# --- estado / cota -------------------------------------------------------
def pacific_day():
    return datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")


def load_state():
    if STATE.exists():
        s = json.loads(STATE.read_text())
    else:
        s = {}
    if s.get("day") != pacific_day():
        s["day"], s["count"] = pacific_day(), 0
    s.setdefault("last_request", 0)
    s.setdefault("done", {})
    return s


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False))


class Limiter:
    def __init__(self, cfg):
        self.cfg = cfg
        self.state = load_state()

    @property
    def remaining(self):
        return max(0, self.cfg["rpd"] - 1 - self.state["count"])  # margem de 1

    def wait_turn(self):
        gap = 60.0 / self.cfg["rpm"] + 1  # 21 s com 3 RPM
        wait = self.state["last_request"] + gap - time.time()
        if wait > 0:
            print(f"  aguardando {wait:.0f}s (limite por minuto)...", flush=True)
            time.sleep(wait)

    def register(self):
        self.state["count"] += 1
        self.state["last_request"] = time.time()
        save_state(self.state)


from tts_provider import QuotaError, TransientError  # noqa: E402

LIMIT_MSG = "limite diário atingido; rode `npm run tts` amanhã"


def call_with_retry(limiter, fn, *args):
    for attempt in range(3):  # 1 tentativa + no máximo 2 repetições
        if limiter.remaining <= 0:
            raise QuotaError(LIMIT_MSG)
        limiter.wait_turn()
        limiter.register()
        try:
            return fn(*args)
        except QuotaError:
            raise
        except TransientError as e:
            print(f"  erro temporário ({e}); tentativa {attempt + 1}/3", flush=True)
            if attempt == 2:
                raise
