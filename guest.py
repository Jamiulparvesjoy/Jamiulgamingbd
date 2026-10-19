# gen.py — A R A F A T PREMIUM GEN [OB55]
# Pipeline: register → grant → MajorRegister → MajorLogin → ChooseRegion
#           → ChooseNewbieChoice → GetLoginData → ClaimMaxim → SetMaxim
# Theme: 🔥 SUPER LAVA + BLOOD 🔥
# Devs: A R A F A T | Channel: @arafatcodex

import hmac, hashlib, requests, string, random, json, time, os, sys, signal, threading, re, subprocess, importlib, codecs, base64
from datetime import datetime, timezone, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings; warnings.filterwarnings("ignore")
sys.path.append(os.getcwd())

# ═════════════════════════════════════════════════════════════════════════════
#  DEBUG  (OFF)
# ═════════════════════════════════════════════════════════════════════════════
DEBUG_MODE, DEBUG_VERBOSE_MODE = False, False

DEBUG         = os.environ.get("JAMIUL_DEBUG",         "1" if DEBUG_MODE else "0") != "0"
DEBUG_VERBOSE = os.environ.get("JAMIUL_DEBUG_VERBOSE", "1" if DEBUG_VERBOSE_MODE else "0") == "1"
_DEBUG_LOCK = threading.Lock()
import traceback as _tb
def dbg(tag, msg, exc=None, verbose_only=False):
    if not DEBUG: return
    if verbose_only and not DEBUG_VERBOSE: return
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    with _DEBUG_LOCK:
        try:
            sys.stderr.write(f"\033[38;5;202m[DBG {ts}] [{tag}]\033[0m {msg}\n")
            if exc is not None:
                _tb.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
            sys.stderr.flush()
        except Exception: pass
def dbg_exc(tag, exc):
    if DEBUG: dbg(tag, f"EXC {type(exc).__name__}: {exc}", exc=exc)

# ═════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════
FFMCONNECT_HOST    = "ffmconnect.ppmainecoonghj.com"
LOGIN_HOST         = "loginbp.ppmainecoonghj.com"
CLIENT_HOST        = "clientbp.ppmainecoonghj.com"
REGISTER_URL       = f"https://{FFMCONNECT_HOST}/api/v2/oauth/guest:register"
GRANT_URL          = f"https://{FFMCONNECT_HOST}/api/v2/oauth/guest/token:grant"
MAJOR_REGISTER_URL = f"https://{LOGIN_HOST}/MajorRegister"
MAJOR_LOGIN_URL    = f"https://{LOGIN_HOST}/MajorLogin"
CHOOSE_REGION_URL  = f"https://{LOGIN_HOST}/ChooseRegion"
CHOOSE_NEWBIE_URL  = f"https://{LOGIN_HOST}/ChooseNewbieChoice"
GET_LOGIN_DATA_URL = f"https://{CLIENT_HOST}/GetLoginData"

CLAIM_AVATAR_URL   = f"https://{CLIENT_HOST}/ClaimAvatarProficiencyAward"
SET_AVATAR_URL     = f"https://{CLIENT_HOST}/ChooseHeadPic"

CLAIM_XGA          = "1790074935"
SET_XGA            = "1790075041"

AVATAR_ID          = 902000030
CLAIM_BODY_HEX     = "F77E251D0B8C6860D2B99B0E287DE7FD"
SET_BODY_HEX       = "635439645789CC67F60E4E7209B791C3"
ALREADY_MARKER     = b"PROFILE_PROFICIENCY_AWARD_CLAIMED"

CHOOSE_NEWBIE_XGA      = "1791524202"
CHOOSE_NEWBIE_BODY_HEX = "3CE3A025334E4E014643A74B16ADB058"

OB55_MSDK_UA       = "GarenaMSDK/4.0.44(SM-S9160 ;Android 9;en;US;app 1.132.1 2019121229;)"
OB55_UNITY_UA      = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"
OB55_UNITY_VER     = "2018.4.12f1"
OB55_RELEASE_VER   = "OB55"
OB55_GAME_VER      = "1.132.4"
OB55_GAME_VER_REG  = "1.132.8"
OB55_CLIENT_VC     = "2019121229"
OB55_CLIENT_ID     = 100067
OB55_CLIENT_SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
OB55_SIG_MD5       = "7428b253defc164018c604a1ebbfebdf"
OB55_DEVICE_TOKEN  = "KqsHT+PFj/2sTPjf+unI9C5rnnStUzOFVqOADw9TI8tgL2bTnmzrBM/dEzyqy4BtAVua+w9mgLRIMrjXa67/qXm0pz5uQWsxC6sd8Um7OmMNHRmy"

AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
NICK_XOR_KEY = b"1e5898ccb8dfdd921f9bdea848768b64a201"

_OB55_DEVICE_BLOB_RAW = "474752450101010072020000143ad264a15bd06e1a30b7b9cb9ec1cf52f8b67f65377bfda1fe2229427fba9b762441d693fdda53018b84ca00f8bb41906de55db0d0110e657a94059a7c701c38aa9dc339d0a4089dec0f57ff3f12908f4cf8120e2377a1b4c92a196288a91c5e31b149571a53bf74b0615bbc8b7ddd65964421b1eb4a21d3a13f48c39d548100f62c291e6804342971e26891687d5b26ac96dbe1183092cf04ea505f932aa4f9736a24e80bbbe5163e17cb0cd53380b875509d83423a13652fb84661e0715c2be05c37eacb2c61b2a649d92dd86e0b91468f4f65b15cf8a6b9f7c74285dfc7032af0c1043314957211b033093125b06c42723385f0d5ba69f8166bb3d1ea4cba0e0a43f7214569140624ddfe3a5baa3982ad268afb609260051fd2bbe57a10e416be21cb2bed1eae86faef6ea111a164ba5d26e6a92c045874e1acdfbb3324373425fb799da26e23a7a526c1a3d137568ac8b8e9f0629ea434f3dbd39d74fb352218c350647c1f3a43ee2163648a7a3c4ece4db81c755ce82b5457bab2fbbff9060661d7ba08fc7b66d9dd86d51015d53bec8801c7964f13dbd353305272791f10ed21b23624c1810279b52279a703f0613316877635ce90605383d269c71aea7165b3c8a6b80c4ea5137c43d38aec7144771308b04a80fa9def7382e95ee1e67a350d847c988b80bd57d21ee870a03188b3f11691b3772471be7924c0a4e33e672cd94ac3a981b7122d11084c486cfa51dfc18427365ee3fcd864c21b4a404cf24737c8424c7e1d19b19f9a4dadc855c7cef5c916fbc1a92c064758b88235f244781da67e98fff8f505dfa5bb0ea75d6d0dfd2bdce1ef7d63497ce1e05a42d3a94f1f55303e31cd6e8cd84e3eb51582f6145a3cb966d859db755c2c1293afb05c3f1ea599f553b0a8c6c9ba6a782fa6bd9ab38bdf882d3d00"
OB55_DEVICE_BLOB = bytes.fromhex(re.sub(r'[^0-9a-fA-F]', '', _OB55_DEVICE_BLOB_RAW))

BD_TZ = timezone(timedelta(hours=6))
def bd_now_str(): return datetime.now(BD_TZ).strftime('%Y-%m-%d %H:%M:%S')

REGION_LANG = {"ME":"ar","IND":"hi","ID":"id","VN":"vi","TH":"th","BD":"bn",
               "PK":"ur","TW":"zh","CIS":"ru","SAC":"es","BR":"pt","EU":"en","US":"en","OTHER":"en"}

# ═════════════════════════════════════════════════════════════════════════════
#  NICKNAME
# ═════════════════════════════════════════════════════════════════════════════
_EXP_DIGITS = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}
MAX_NICK_LEN = 12

def generate_nick(prefix):
    prefix = (prefix or "JAMIUL").strip()[:MAX_NICK_LEN]
    remaining = MAX_NICK_LEN - len(prefix)
    if remaining <= 0: return prefix
    digits = ''.join(str(random.randint(0, 9)) for _ in range(remaining))
    return f"{prefix}{''.join(_EXP_DIGITS[d] for d in digits)}"

# ═════════════════════════════════════════════════════════════════════════════
#  PROTOBUF + AES
# ═════════════════════════════════════════════════════════════════════════════
def _enc_var(n):
    if n < 0: return b''
    out = []
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        out.append(b)
        if not n: break
    return bytes(out)

def _proto_field(fn, v):
    if isinstance(v, dict):
        nn = _build_proto(v)
        return _enc_var((fn << 3) | 2) + _enc_var(len(nn)) + nn
    if isinstance(v, bool): return _enc_var((fn << 3) | 0) + _enc_var(1 if v else 0)
    if isinstance(v, int):  return _enc_var((fn << 3) | 0) + _enc_var(v)
    if isinstance(v, (str, bytes)):
        b = v.encode() if isinstance(v, str) else v
        return _enc_var((fn << 3) | 2) + _enc_var(len(b)) + b
    return b''

def _build_proto(f):
    return b''.join(_proto_field(k, v) for k, v in f.items())

def aes_encrypt(data: bytes) -> bytes:
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(data, AES.block_size))

def _rv(data, pos):
    r = 0; s = 0
    while pos < len(data):
        b = data[pos]; r |= (b & 0x7F) << s; pos += 1
        if not (b & 0x80): return r, pos
        s += 7
        if s > 63: break
    return None, pos

def decode_message(data):
    result = {}; pos = 0; n = len(data)
    while pos < n:
        try:
            tag, pos = _rv(data, pos)
            if tag is None: break
            fn = tag >> 3; wt = tag & 7
            if fn == 0: break
            if wt == 0:
                v, pos = _rv(data, pos); result[fn] = v
            elif wt == 1:
                if pos + 8 > n: break
                result[fn] = int.from_bytes(data[pos:pos+8], 'little'); pos += 8
            elif wt == 2:
                sz, pos = _rv(data, pos)
                if sz is None or pos + sz > n: break
                raw = data[pos:pos+sz]; pos += sz
                try:
                    nested, _ = decode_message(raw)
                    if nested and all(isinstance(k, int) for k in nested.keys()): result[fn] = nested
                    else: result[fn] = raw
                except Exception: result[fn] = raw
            elif wt == 5:
                if pos + 4 > n: break
                result[fn] = int.from_bytes(data[pos:pos+4], 'little'); pos += 4
            else: break
        except Exception: break
    return result, None

def _find_account_id(fields, depth=0):
    if depth > 6 or not isinstance(fields, dict): return None
    for key in (3, 1, 2):
        v = fields.get(key)
        if isinstance(v, int) and 100_000_000 <= v <= 999_999_999_999: return v
    for v in fields.values():
        if isinstance(v, dict):
            r = _find_account_id(v, depth + 1)
            if r: return r
    return None

def keystream_encode(oid):
    ks = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
          0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
    e = "".join(chr(ord(oid[i]) ^ ks[i % len(ks)]) for i in range(len(oid)))
    return codecs.decode(''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in e),
                         'unicode_escape').encode('latin1')

# ═════════════════════════════════════════════════════════════════════════════
#  JWT + NICKNAME DECODE
# ═════════════════════════════════════════════════════════════════════════════
def _parse_jwt_from_pb(data):
    n = len(data)
    for j in range(n - 3):
        if data[j] != 0x42: continue
        ln = 0; sh = 0; p = j + 1
        while p < n:
            b = data[p]; p += 1
            ln |= (b & 0x7f) << sh
            if not (b & 0x80): break
            sh += 7
            if sh > 21: break
        if ln < 100 or ln > 5000: continue
        if p + ln > n: continue
        if data[p:p+3] == b'eyJ':
            return data[p:p+ln].decode('utf-8', errors='ignore')
    return None

def decode_jwt_payload(jwt):
    try:
        parts = jwt.split('.')
        if len(parts) != 3: return {}
        p = parts[1]; p += '=' * ((4 - len(p) % 4) % 4)
        return json.loads(base64.urlsafe_b64decode(p))
    except Exception: return {}

def decode_nickname(encoded_b64):
    try:
        raw = base64.b64decode(encoded_b64)
        dec = bytearray()
        for i, b in enumerate(raw):
            dec.append(b ^ NICK_XOR_KEY[i % len(NICK_XOR_KEY)])
        return dec.decode('utf-8', errors='replace').strip('\x00')
    except Exception as e:
        return f"[DECODE_ERROR: {e}]"

# ═════════════════════════════════════════════════════════════════════════════
#  LAVA + BLOOD THEME
# ═════════════════════════════════════════════════════════════════════════════
C_ = "\033[38;5;202m"
G_ = "\033[38;5;226m"
R_ = "\033[38;5;160m"
Y_ = "\033[38;5;208m"
W_ = "\033[38;5;223m"
B_ = "\033[1m"
S_ = "\033[0m"

def clear(): os.system('clear' if os.name=='posix' else 'cls')
def draw_line(): print(f"{C_}{'═'*56}{S_}")
def clean_ansi(t):
    for c in (C_,G_,R_,Y_,W_,B_,S_): t = t.replace(c,'')
    return t

def print_box(lines):
    if not lines: return
    lines = [l for l in lines if l.strip()]
    if not lines: return
    ml = max(len(clean_ansi(l)) for l in lines)
    print(f"{C_}╔{'═'*(ml+2)}╗{S_}")
    print(f"{C_}║{S_} {lines[0]}{' '*(ml-len(clean_ansi(lines[0])))} {C_}║{S_}")
    if len(lines) > 1:
        print(f"{C_}╠{'═'*(ml+2)}╣{S_}")
        for l in lines[1:]:
            print(f"{C_}║{S_} {l}{' '*(ml-len(clean_ansi(l)))} {C_}║{S_}")
    print(f"{C_}╚{'═'*(ml+2)}╝{S_}")

def banner():
    clear()
    print(f"""{C_}{B_}
 █████╗ ██████╗  █████╗ ███████╗ █████╗ ████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
███████║██████╔╝███████║█████╗  ███████║   ██║   
██╔══██║██╔══██╗██╔══██║██╔══╝  ██╔══██║   ██║   
██║  ██║██║  ██║██║  ██║██║     ██║  ██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝  {S_}""")
    draw_line()
    print_box([f"{Y_}{B_}      🔥 A R A F A T PREMIUM GEN  [OB55] 🔥{S_}"])
    draw_line()

# ═════════════════════════════════════════════════════════════════════════════
#  FOLDERS
# ═════════════════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(BASE_DIR, "JAMIUL_GEN")
SAVED_FOLDER = os.path.join(BASE_FOLDER, "SAVED")
for d in [BASE_FOLDER, SAVED_FOLDER]: os.makedirs(d, exist_ok=True)

FILE_LOCKS = {}
def get_lock(f):
    if f not in FILE_LOCKS: FILE_LOCKS[f] = threading.Lock()
    return FILE_LOCKS[f]

# ═════════════════════════════════════════════════════════════════════════════
#  HELPERS / SIGNALS
# ═════════════════════════════════════════════════════════════════════════════
def install_requirements():
    for pkg in ['requests', 'urllib3', 'pycryptodome']:
        try:
            if pkg == 'pycryptodome': import Crypto  # noqa
            else: importlib.import_module(pkg)
        except ImportError:
            try: subprocess.check_call([sys.executable,'-m','pip','install',pkg,'--quiet'])
            except Exception: return False
    return True

EXIT = False
def safe_exit(sig=None, fr=None):
    global EXIT; EXIT = True
    print(f"\n{G_}🔥 Goodbye!{S_}"); sys.exit(0)
signal.signal(signal.SIGINT, safe_exit)
signal.signal(signal.SIGTERM, safe_exit)

def gen_password(prefix):
    return f"{prefix}_{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))}"
def sha256_upper(pw): return hashlib.sha256(pw.encode()).hexdigest().upper()

# ═════════════════════════════════════════════════════════════════════════════
#  SESSION
# ═════════════════════════════════════════════════════════════════════════════
_GLOBAL_SESSION = None
SESSION_LOCK = threading.Lock()
def get_session():
    global _GLOBAL_SESSION
    if _GLOBAL_SESSION is None:
        with SESSION_LOCK:
            if _GLOBAL_SESSION is None:
                s = requests.Session(); s.verify = False
                s.mount('https://', requests.adapters.HTTPAdapter(
                    pool_connections=500, pool_maxsize=1000, max_retries=0, pool_block=False))
                _GLOBAL_SESSION = s
    return _GLOBAL_SESSION

PRINT_LOCK = threading.Lock()
RATE_LOCK = threading.Lock()
LAST_REGISTER_TS = [0.0]
REGISTER_MIN_GAP = 1.0

# ═════════════════════════════════════════════════════════════════════════════
#  PIPELINE STEPS
# ═════════════════════════════════════════════════════════════════════════════
def _pace_register():
    with RATE_LOCK:
        now = time.time()
        wait = REGISTER_MIN_GAP - (now - LAST_REGISTER_TS[0])
        if wait > 0: time.sleep(wait)
        LAST_REGISTER_TS[0] = time.time()

def register_guest(pw, s):
    _pace_register()
    body = json.dumps({"app_id": OB55_CLIENT_ID, "client_type": 2,
                       "password": pw, "source": 2}, separators=(',',':'))
    sig = hmac.new(OB55_CLIENT_SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
    try:
        r = s.post(REGISTER_URL,
                   headers={"Accept":"application/json","Accept-Encoding":"gzip",
                            "Connection":"Keep-Alive",
                            "Content-Type":"application/json; charset=utf-8",
                            "User-Agent":OB55_MSDK_UA,
                            "Authorization":f"Signature {sig}"},
                   data=body, timeout=25, verify=False)
        if r.status_code == 429: time.sleep(4 + random.uniform(0, 3)); return None
        if r.status_code != 200: return None
        j = r.json()
        return j["data"].get("uid") if j.get("code") == 0 else None
    except Exception as e:
        dbg_exc("register", e); return None

def grant_guest(uid, pw, s):
    for pw_val, label in [(pw, "plain"), (sha256_upper(pw), "sha256")]:
        try:
            body = json.dumps({"client_id": OB55_CLIENT_ID, "client_secret": OB55_CLIENT_SECRET,
                               "client_type": 2, "device_id": "", "password": pw_val,
                               "response_type": "token", "uid": int(uid)}, separators=(',',':'))
            r = s.post(GRANT_URL,
                       headers={"Accept":"application/json","Accept-Encoding":"gzip",
                                "Connection":"Keep-Alive",
                                "Content-Type":"application/json; charset=utf-8",
                                "User-Agent":OB55_MSDK_UA},
                       data=body, timeout=25, verify=False)
            if r.status_code != 200: continue
            j = r.json()
            if j.get("code") != 0: continue
            d = j.get("data", {}) or {}
            if d.get("open_id") and d.get("access_token"):
                return {"open_id": d["open_id"], "access_token": d["access_token"],
                        "refresh_token": d.get("refresh_token",""),
                        "expiry_time": d.get("expiry_time",0),
                        "token_type": d.get("token_type","Bearer")}
        except Exception as e:
            dbg_exc(f"grant/{label}", e)
    return None

def major_register(at, oid, region, name, lang, s):
    headers = {"Accept":"*/*","Accept-Encoding":"deflate, gzip","Authorization":"Bearer",
               "Content-Type":"application/x-www-form-urlencoded","Host":LOGIN_HOST,
               "ReleaseVersion":OB55_RELEASE_VER,"User-Agent":OB55_UNITY_UA,
               "X-GA":"v1 1","X-GA-SV":str(int(time.time())),
               "X-Unity-Version":OB55_UNITY_VER}
    prefix = ''.join(c for c in name if c not in '⁰¹²³⁴⁵⁶⁷⁸⁹') or "JAMIUL"

    def _attempt(cand):
        payload = {1: cand, 2: at, 3: oid, 5: 102000007, 6: 4, 7: 1, 13: 1,
                   14: keystream_encode(oid), 15: lang, 16: 1,
                   20: OB55_GAME_VER_REG, 21: 1, 22: OB55_DEVICE_BLOB}
        body = aes_encrypt(_build_proto(payload))
        r = s.post(MAJOR_REGISTER_URL, headers=headers, data=body, timeout=25, verify=False)
        resp = r.content or b""
        if r.status_code != 200 or not resp: return None, resp, {}
        fields, _ = decode_message(resp)
        return _find_account_id(fields), resp, fields

    tried = set(); queue = [name] + [generate_nick(prefix) for _ in range(10)]
    last_resp = None
    for cand in queue:
        if EXIT: return None, name, last_resp
        if cand in tried: continue
        tried.add(cand)
        aid, last_resp, fields = _attempt(cand)
        if aid:
            return str(aid), cand, last_resp
        sug = fields.get(9)
        if isinstance(sug, bytes):
            try:
                s_str = sug.decode('utf-8', errors='ignore').strip()
                if s_str and s_str not in tried and s_str.isprintable():
                    tried.add(s_str)
                    a2, r2, _ = _attempt(s_str)
                    if a2:
                        return str(a2), s_str, r2
                    last_resp = r2 or last_resp
            except Exception: pass
    return None, name, last_resp

def _build_major_login_payload(uid, region, at, oid, lang):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return _build_proto({
        3: now, 4: "free fire", 5: 4, 7: OB55_GAME_VER,
        8: "Android OS 13 / API-33 (TKQ1.221114.001/V14.0.7.0.TGEINXM)",
        9: "Handheld", 10: "Vi India", 11: "CarrierDataNetwork",
        12: 1650, 13: 720, 14: "320",
        15: "ARM64 FP ASIMD AES | 4800 | 8", 16: 5652,
        17: "Adreno (TM) 610", 18: "OpenGL ES 3.2 V@0502.41",
        19: "Google|c6c902a0-850c-4758-a75f-67851f122f07",
        20: "42.111.9.117", 21: lang, 22: oid, 23: "4", 24: "Handheld",
        25: {6: 4, 8: 0}, 29: at, 30: 1,
        41: "Vi India", 42: "4G", 57: OB55_SIG_MD5,
        60: 104713, 61: 45770, 62: 1309, 63: 45898,
        64: 104713, 65: 45898, 66: 104713,
        73: 1, 76: 102000007, 78: 3, 79: 2, 81: "64",
        83: OB55_CLIENT_VC, 86: "OpenGLES2", 87: 4095, 88: 1,
        92: 6634, 93: "android", 94: OB55_DEVICE_TOKEN,
        95: 1, 97: 1, 98: 0, 99: "4", 100: "4",
    })

try:
    from MajorLoginRes_pb2 import MajorLoginRes as _PB_MLR
except Exception:
    _PB_MLR = None

def _parse_major_login_response(resp):
    if _PB_MLR is not None:
        try:
            _m = _PB_MLR()
            _m.ParseFromString(resp)
            if _m.token.startswith("eyJ"):
                return {"account_uid": _m.account_uid, "region": _m.region, "token": _m.token,
                        "url": _m.url, "timestamp": _m.timestamp, "key": _m.key, "iv": _m.iv}
        except Exception:
            pass
    fields, _ = decode_message(resp)
    tok = fields.get(8)
    if isinstance(tok, bytes) and tok[:3] == b'eyJ':
        return {"account_uid": fields.get(1, 0),
                "region": fields.get(2, b'').decode('utf-8', errors='ignore') if isinstance(fields.get(2), bytes) else '',
                "token": tok.decode('utf-8', errors='ignore'),
                "url": fields.get(10, b'').decode('utf-8', errors='ignore') if isinstance(fields.get(10), bytes) else '',
                "timestamp": fields.get(21, 0),
                "key": fields.get(22, b''), "iv": fields.get(23, b'')}
    jwt = _parse_jwt_from_pb(resp)
    if jwt:
        return {"account_uid": fields.get(1, 0), "region": "", "token": jwt,
                "url": "", "timestamp": 0, "key": b'', "iv": b''}
    return None

def major_login(aid, uid, region, at, oid, lang, s):
    plain = _build_major_login_payload(uid, region, at, oid, lang)
    aes_body = aes_encrypt(plain)
    headers = {"Accept":"*/*","Accept-Encoding":"deflate, gzip","Authorization":"Bearer",
               "Content-Type":"application/x-www-form-urlencoded","Host":LOGIN_HOST,
               "ReleaseVersion":OB55_RELEASE_VER,"User-Agent":OB55_UNITY_UA,
               "X-GA":"v1 1","X-GA-SV":str(int(time.time())),
               "X-Unity-Version":OB55_UNITY_VER}
    for label, body in (("aes", aes_body), ("plain", plain)):
        try:
            r = s.post(MAJOR_LOGIN_URL, headers=headers, data=body, timeout=25, verify=False)
            resp = r.content or b""
            if r.status_code != 200 or len(resp) < 40: continue
            parsed = _parse_major_login_response(resp)
            if not parsed or not parsed.get("token"): continue
            jwt = parsed["token"]
            pl = decode_jwt_payload(jwt)
            nick = decode_nickname(pl.get("nickname", "")) if pl.get("nickname") else ""
            return {"account_id": parsed.get("account_uid") or pl.get("account_id"),
                    "jwt_token": jwt, "nickname": nick,
                    "nickname_encoded": pl.get("nickname", ""),
                    "payload": pl, "server_url": parsed.get("url", "")}
        except Exception as e:
            dbg_exc(f"major_login/{label}", e)
    return None

def choose_region(jwt, region, s):
    try:
        rc = "RU" if region.upper() == "CIS" else region.upper()
        payload = aes_encrypt(_build_proto({1: rc}))
        h = {"User-Agent": OB55_UNITY_UA, "Connection": "Keep-Alive",
             "Accept-Encoding": "gzip",
             "Content-Type": "application/x-www-form-urlencoded",
             "Expect": "100-continue",
             "Authorization": f"Bearer {jwt}",
             "X-Unity-Version": OB55_UNITY_VER,
             "X-GA": "v1 1", "X-GA-SV": str(int(time.time())),
             "ReleaseVersion": OB55_RELEASE_VER, "Host": LOGIN_HOST}
        r = s.post(CHOOSE_REGION_URL, data=payload, headers=h, timeout=25, verify=False)
        body_txt = (r.content or b"").decode('utf-8', errors='ignore').strip()
        if r.status_code == 200: return True, "OK"
        if r.status_code == 400 and "REGION" in body_txt.upper(): return True, "ALREADY_BOUND"
        return False, body_txt or f"HTTP {r.status_code}"
    except Exception as e:
        dbg_exc("choose_region", e); return False, f"EXC {e}"

def choose_newbie_choice(jwt, s):
    try:
        body = bytes.fromhex(CHOOSE_NEWBIE_BODY_HEX)
        h = {
            "Accept": "*/*", "Accept-Encoding": "deflate, gzip",
            "Authorization": f"Bearer {jwt}",
            "Content-Length": "16",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": LOGIN_HOST,
            "ReleaseVersion": OB55_RELEASE_VER,
            "User-Agent": OB55_UNITY_UA,
            "X-GA": "v1 1",
            "X-GA-SV": CHOOSE_NEWBIE_XGA,
            "X-Unity-Version": OB55_UNITY_VER,
        }
        r = s.post(CHOOSE_NEWBIE_URL, headers=h, data=body, timeout=25, verify=False)
        return r.status_code == 200
    except Exception as e:
        dbg_exc("choose_newbie", e); return False

def get_login_data(jwt, at, oid, region, s):
    try:
        lang = REGION_LANG.get(region.upper(), "en")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fields = {1: oid, 2: at, 3: now, 4: "free fire", 5: 4, 7: OB55_GAME_VER,
                  8: "Android OS 13 / API-33 (TKQ1.221114.001/V14.0.7.0.TGEINXM)",
                  9: "Handheld", 10: "Vi India", 11: "CarrierDataNetwork",
                  12: 1650, 13: 720, 14: "320",
                  15: "ARM64 FP ASIMD AES | 4800 | 8", 16: 5652,
                  17: "Adreno (TM) 610", 18: "OpenGL ES 3.2 V@0502.41",
                  19: "Google|c6c902a0-850c-4758-a75f-67851f122f07",
                  20: "42.111.9.117", 21: lang, 22: oid, 23: "4", 24: "Handheld",
                  25: "Xiaomi 220333QBI", 26: region.upper(), 29: at, 30: 1,
                  41: "Vi India", 42: "4G", 57: OB55_SIG_MD5,
                  60: 104713, 61: 45770, 62: 1309, 64: 45898, 65: 104713,
                  66: 45898, 67: 104713, 73: 1, 76: 1, 78: 3, 79: 2,
                  81: "64", 83: OB55_CLIENT_VC, 86: "OpenGLES2", 87: 4095, 88: 4,
                  90: "Dhaka", 91: "DL", 92: 6634, 93: "android",
                  94: OB55_DEVICE_TOKEN, 95: 111207,
                  96: '{"cur_rate":null,"support_etc2":false}',
                  97: 1, 99: "4", 100: "4", 102: "4b004346025b0f0632",
                  103: 1, 107: OB55_SIG_MD5}
        payload = aes_encrypt(_build_proto(fields))
        h = {"Expect": "100-continue", "Authorization": f"Bearer {jwt}",
             "X-Unity-Version": OB55_UNITY_VER, "X-GA": "v1 1",
             "X-GA-SV": str(int(time.time())),
             "ReleaseVersion": OB55_RELEASE_VER,
             "Content-Type": "application/x-www-form-urlencoded",
             "User-Agent": OB55_UNITY_UA, "Host": CLIENT_HOST,
             "Connection": "close", "Accept-Encoding": "gzip, deflate, br"}
        r = s.post(GET_LOGIN_DATA_URL, headers=h, data=payload, timeout=20, verify=False)
        return r.status_code == 200
    except Exception as e:
        dbg_exc("get_login_data", e); return False

def _maxim_headers(jwt, xga):
    return {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": f"Bearer {jwt}",
        "Content-Length": "16",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": CLIENT_HOST,
        "ReleaseVersion": OB55_RELEASE_VER,
        "User-Agent": OB55_UNITY_UA,
        "X-GA": "v1 1",
        "X-GA-SV": xga,
        "X-Unity-Version": OB55_UNITY_VER,
    }

def claim_maxim(jwt, s, retries=3):
    body = bytes.fromhex(CLAIM_BODY_HEX)
    for attempt in range(retries):
        try:
            r = s.post(CLAIM_AVATAR_URL, headers=_maxim_headers(jwt, CLAIM_XGA),
                       data=body, timeout=25, verify=False)
            if r.status_code == 200: return "ok"
            if ALREADY_MARKER in (r.content or b""): return "already"
            try:
                plain = unpad(AES.new(AES_KEY, AES.MODE_CBC, AES_IV).decrypt(r.content), AES.block_size)
                if ALREADY_MARKER in plain: return "already"
            except Exception: pass
            if r.status_code == 404:
                time.sleep(1.5 + attempt); continue
            return f"err:HTTP {r.status_code}"
        except Exception as e:
            dbg_exc(f"maxim_claim/try{attempt+1}", e); time.sleep(1.0 + attempt)
    return "err:all_retries_failed"

def set_maxim(jwt, s, retries=3):
    body = bytes.fromhex(SET_BODY_HEX)
    for attempt in range(retries):
        try:
            r = s.post(SET_AVATAR_URL, headers=_maxim_headers(jwt, SET_XGA),
                       data=body, timeout=25, verify=False)
            if r.status_code == 200: return "ok"
            if r.status_code in (400, 404):
                time.sleep(1.5 + attempt); continue
            return f"err:HTTP {r.status_code}"
        except Exception as e:
            dbg_exc(f"maxim_set/try{attempt+1}", e); time.sleep(1.0 + attempt)
    return "err:all_retries_failed"

# ═════════════════════════════════════════════════════════════════════════════
#  ACCOUNT CREATION
# ═════════════════════════════════════════════════════════════════════════════
def create_account(pw_prefix, nick_prefix, region, tid, do_maxim=True):
    if EXIT: return None
    s = get_session()
    for attempt in range(3):
        if EXIT: return None
        pw = gen_password(pw_prefix)
        uid = register_guest(pw, s)
        if not uid: time.sleep(1.5); continue
        g = grant_guest(uid, pw, s)
        if not g: time.sleep(1.5); continue

        lang = REGION_LANG.get(region.upper(), "en")
        nick_req = generate_nick(nick_prefix)

        aid, final_name, reg_resp = major_register(g["access_token"], g["open_id"], region, nick_req, lang, s)

        lr = None; jwt = ""; nick = "N/A"
        chosen = False; region_note = ""
        sealed = False; newbie_ok = False
        maxim_claim = "skipped"; maxim_set = "skipped"

        if aid:
            lr = major_login(aid, uid, region, at=g["access_token"], oid=g["open_id"], lang=lang, s=s)
            if lr and lr.get("jwt_token"):
                jwt = lr["jwt_token"]; nick = lr.get("nickname", "") or "N/A"

                chosen, region_note = choose_region(jwt, region, s)
                time.sleep(0.3)

                newbie_ok = choose_newbie_choice(jwt, s)
                time.sleep(0.3)

                sealed = get_login_data(jwt, g["access_token"], g["open_id"], region, s)
                time.sleep(1.0)

                if do_maxim:
                    maxim_claim = claim_maxim(jwt, s)
                    time.sleep(0.5)
                    maxim_set = set_maxim(jwt, s)

        is_success = bool(aid and jwt)
        return {
            "uid": uid, "password": pw,
            "account_id": aid or "N/A",
            "name": final_name or nick_req,
            "nickname": nick, "region": region,
            "open_id": g["open_id"], "access_token": g["access_token"],
            "refresh_token": g["refresh_token"], "expiry_time": g["expiry_time"],
            "token_type": g["token_type"], "jwt_token": jwt,
            "region_bound": chosen, "region_note": region_note,
            "sealed": sealed, "newbie_choice": newbie_ok,
            "maxim_claim": maxim_claim, "maxim_set": maxim_set,
            "maxim_avatar_id": AVATAR_ID,
            "status": "SUCCESS" if is_success else ("PARTIAL" if aid else "NO_ACCOUNT_ID"),
            "date_created": bd_now_str(), "thread_id": tid,
        }
    return None

# ═════════════════════════════════════════════════════════════════════════════
#  MERGE SAVE
# ═════════════════════════════════════════════════════════════════════════════
def save_merge_json(path, entry, key='uid'):
    if not entry or key not in entry: return False, 0
    full_path = path if os.path.isabs(path) else os.path.join(SAVED_FOLDER, path)
    with get_lock(full_path):
        existing = []
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f: existing = json.load(f)
                if not isinstance(existing, list): existing = []
            except Exception: existing = []
        seen = {}; order = []
        for e in existing:
            if isinstance(e, dict) and key in e:
                if e[key] not in seen: order.append(e[key])
                seen[e[key]] = e
        is_new = entry[key] not in seen
        if is_new: order.append(entry[key])
        seen[entry[key]] = entry
        out = [seen[k] for k in order]
        tmp = full_path + '.tmp'
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(out, f, indent=2, ensure_ascii=False)
            os.replace(tmp, full_path)
        except Exception as e:
            dbg_exc("save_merge", e); return False, len(out)
        return is_new, len(out)

# ═════════════════════════════════════════════════════════════════════════════
#  RUNTIME
# ═════════════════════════════════════════════════════════════════════════════
LOCK = threading.Lock()
OK = 0
NEXT_TO_PRINT = 1
DO_MAXIM = True
FAILED = [0]
ATTEMPTS = [0]

def generate_one(pw_prefix, nick_prefix, region, total, tid, main_file, detail_file):
    global OK, NEXT_TO_PRINT
    if EXIT: return
    with LOCK:
        if OK >= total: return
        if ATTEMPTS[0] <= 0: return
        ATTEMPTS[0] -= 1
    time.sleep(random.uniform(0.3, 1.0))
    res = create_account(pw_prefix, nick_prefix, region, tid, do_maxim=DO_MAXIM)
    if not res:
        with LOCK: FAILED[0] += 1
        print(f"[GUEST] FAILED attempt: account create hoy nai (network/region check korun)", flush=True)
        return
    with LOCK:
        if OK >= total: return
        OK += 1; cur = OK
    while cur != NEXT_TO_PRINT:
        if EXIT: return
        time.sleep(0.05)
    save_merge_json(main_file,   {"uid": res["uid"], "password": res["password"]}, key='uid')
    save_merge_json(detail_file, res, key='uid')
    with PRINT_LOCK:
        print(f"[GUEST] CREATED {cur}/{total} uid={res['uid']} account_id={res['account_id']} region={res['region']} status={res['status']} region_bound={res.get('region_bound')}", flush=True)
        NEXT_TO_PRINT += 1

def _worker(pw_prefix, nick_prefix, region, total, tid, main_file, detail_file):
    time.sleep(tid * 0.4)
    while not EXIT:
        with LOCK:
            if OK >= total: break
            if ATTEMPTS[0] <= 0: break
        try: generate_one(pw_prefix, nick_prefix, region, total, tid, main_file, detail_file)
        except Exception as e:
            dbg_exc(f"worker/tid={tid}", e); time.sleep(1.5)

# ═════════════════════════════════════════════════════════════════════════════
#  GEN FLOW
# ═════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════
#  CLI ENTRY  (main.py / web dashboard theke call hoy; terminal menu nai)
# ═════════════════════════════════════════════════════════════════════════════
VALID_REGIONS = ["BD", "IND", "ID", "SG", "PK", "ME", "BR", "NA", "TH", "VN", "MY", "PH", "TW", "CIS", "SAC"]

def cli_main(argv=None):
    import argparse
    global ATTEMPTS, DO_MAXIM, OK, NEXT_TO_PRINT, EXIT
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="JAMIUL guest account generator")
    ap.add_argument("--region", required=True)
    ap.add_argument("--name", default="JAMIUL", help="account nickname prefix")
    ap.add_argument("--count", type=int, default=4, help="1-12")
    ap.add_argument("--accounts-file", default=os.path.join(here, "accounts.json"))
    ap.add_argument("--password-prefix", default="JAMIUL")
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--no-maxim", action="store_true")
    a = ap.parse_args(argv)

    region = a.region.strip().upper()
    if region not in VALID_REGIONS:
        print(f"[GUEST] FAILED invalid region: {region}", flush=True)
        return 2
    count = max(1, min(12, a.count))
    name = "".join(ch for ch in a.name if ch.isalnum() or ch == "_")[:12] or "JAMIUL"
    pw_prefix = "".join(ch for ch in a.password_prefix if ch.isalnum() or ch == "_")[:12] or "JAMIUL"
    main_file = os.path.abspath(a.accounts_file)
    detail_file = os.path.join(here, "guest_details.json")

    DO_MAXIM = not a.no_maxim
    OK = 0
    NEXT_TO_PRINT = 1
    ATTEMPTS[0] = count * 4
    FAILED[0] = 0
    print(f"[GUEST] start: {count} x {region} | name {name} | file {main_file}", flush=True)

    n_threads = max(1, min(4, a.threads))
    ths = [threading.Thread(target=_worker, args=(pw_prefix, name, region, count, i + 1, main_file, detail_file),
                            daemon=True) for i in range(n_threads)]
    for t in ths:
        t.start()
    try:
        for t in ths:
            while t.is_alive():
                t.join(timeout=1.0)
    except KeyboardInterrupt:
        EXIT = True
        print("[GUEST] stopped by user", flush=True)
    print(f"[GUEST] DONE created={OK} requested={count}", flush=True)
    return 0 if OK else 1

if __name__ == "__main__":
    try:
        sys.exit(cli_main())
    except KeyboardInterrupt:
        print("[GUEST] stopped", flush=True)
        sys.exit(1)
