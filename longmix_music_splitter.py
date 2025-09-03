#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =========================================================
# LongMix Music Splitter for Mac
# Author : Alchemist YOHEY
# Version: 1.2.2
#
# 仕様:
#  - 出力: 44.1kHz / AAC / Stereo（.m4a, ipodコンテナ）
#  - 目標 200MB 未満（下限 112kbps、上限 384kbps）
#  - 分割: 2時間未満は単一、2時間以上は「90分間隔」で可変パート分割
#          各ターゲット付近(±45s)で無音を優先、無ければキッカリ
#  - 分割時は *_part1.m4a, *_part2.m4a, ... と連番
#    さらに title に (Part i)、disc/track に i/N を付与（元タグは継承）
#  - 入出力はスクリプトと同階層の input/ と output/
# =========================================================

APP_NAME  = "LongMix Music Splitter for Mac"
AUTHOR    = "Alchemist YOHEY"
VERSION   = "v1.2.2"   # ← 以後はここだけ更新

import subprocess, json, re, math
from pathlib import Path
from typing import Optional, List, Tuple

# ======= パラメータ =======
TARGET_MAX_MB    = 190
TARGET_MAX_BYTES = TARGET_MAX_MB * 1024 * 1024
MIN_BITRATE_K    = 112
MAX_BITRATE_K    = 384
SPLIT_CUTOFF_SEC = 2 * 60 * 60       # 2時間
CHUNK_SEC        = 90 * 60           # 90分

SILENCE_NOISE_DB   = -35
SILENCE_MIN_DUR    = 0.20
SILENCE_WINDOW_SEC = 45

# ======= 入出力 =======
SCRIPT_DIR = Path(__file__).resolve().parent
IN_DIR     = SCRIPT_DIR / "input"
OUT_DIR    = SCRIPT_DIR / "output"
EXTS = {".mp3",".m4a",".aac",".wav",".aiff",".aif",".flac",".alac",".ogg",".oga",".mka"}

# ======= Util =======
def run(cmd: list) -> str:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")

def ffprobe(path: Path) -> dict:
    out = run(["ffprobe","-v","error","-print_format","json","-show_format","-show_streams",str(path)])
    return json.loads(out)

def get_duration_sec(meta: dict) -> float:
    f = meta.get("format", {})
    if "duration" in f:
        try: return float(f["duration"])
        except: pass
    for s in meta.get("streams", []):
        d = s.get("duration")
        if d:
            try: return float(d)
            except: pass
    return 0.0

def get_source_kbps(meta: dict) -> Optional[int]:
    for s in meta.get("streams", []):
        if s.get("codec_type") == "audio":
            br = s.get("bit_rate")
            if br:
                try: return max(1, int(int(br)/1000))
                except: pass
    br = meta.get("format", {}).get("bit_rate")
    if br:
        try: return max(1, int(int(br)/1000))
        except: pass
    return None

def has_attached_pic(meta: dict) -> bool:
    for s in meta.get("streams", []):
        if s.get("codec_type")=="video" and s.get("disposition",{}).get("attached_pic")==1:
            return True
    return False

def get_tag(meta: dict, key: str) -> Optional[str]:
    f = meta.get("format", {})
    tags = f.get("tags", {}) if isinstance(f.get("tags"), dict) else {}
    val = tags.get(key)
    if val: return str(val)
    return None

def safe_name(name: str) -> str:
    bad='\\/:*?"<>|'
    return "".join(c for c in name if c not in bad).strip()

def kbps_for_target(dur_sec: float, target_bytes: int) -> int:
    if dur_sec <= 0: return MIN_BITRATE_K
    kbps = int((target_bytes*8)/dur_sec/1000) - 8
    return max(MIN_BITRATE_K, kbps)

def choose_kbps(dur_sec: float, target_bytes: int, src_kbps: Optional[int]) -> int:
    target_k = kbps_for_target(dur_sec, target_bytes)
    upper    = MAX_BITRATE_K
    if src_kbps:
        upper = min(upper, max(MIN_BITRATE_K, src_kbps))
    return max(MIN_BITRATE_K, min(target_k, upper))

# ======= エンコード =======
def encode_segment(
    infile: Path,
    start: float,
    length: float,
    outfile: Path,
    kbps: int,
    copy_pic: bool,
    title_override: Optional[str] = None,
    disc_value: Optional[str] = None,
    track_value: Optional[str] = None,
):
    """
    - 44.1kHz / AAC / Stereo / ipod(m4a)
    - -map_metadata 0 で元タグを継承
    - title/track/disc が指定された場合のみ上書き
    """
    outfile.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg","-y",
        "-ss", str(start),
        "-i",  str(infile),
        "-t",  str(length),
        "-map_metadata","0",
        "-map","0:a:0",
        "-c:a","aac","-b:a",f"{kbps}k",
        "-ar","44100","-ac","2",
        "-af","aresample=resampler=soxr",
        "-movflags","+faststart",
        "-f","ipod",
    ]
    if title_override:
        cmd += ["-metadata", f"title={title_override}"]
    if disc_value:
        cmd += ["-metadata", f"disc={disc_value}"]
    if track_value:
        cmd += ["-metadata", f"track={track_value}"]
    if copy_pic:
        cmd += ["-map","0:v:0?","-c:v","copy","-disposition:v:0","attached_pic"]

    cmd.append(str(outfile))
    subprocess.check_call(cmd)

def ensure_under_target(
    infile: Path, start: float, length: float, outfile: Path, kbps_now: int, copy_pic: bool,
    title_override: Optional[str], disc_value: Optional[str], track_value: Optional[str]
) -> int:
    size = outfile.stat().st_size
    if size <= TARGET_MAX_BYTES:
        return kbps_now
    ratio = TARGET_MAX_BYTES / size
    kbps2 = max(MIN_BITRATE_K, int(kbps_now * ratio) - 8)
    tmp   = outfile.with_name(outfile.stem + ".tmp" + outfile.suffix)
    encode_segment(infile, start, length, tmp, kbps2, copy_pic, title_override, disc_value, track_value)
    tmp.replace(outfile)
    return kbps2

# ======= 無音検出 =======
_s_start = re.compile(r"silence_start:\s*([0-9.]+)")
_s_end   = re.compile(r"silence_end:\s*([0-9.]+)")

def detect_silence_near(infile: Path, target_sec: float, window_sec: float) -> Optional[float]:
    """指定秒の±window内で最も近い無音開始/終了位置を返す"""
    try:
        out = run([
            "ffmpeg","-hide_banner","-nostats",
            "-i", str(infile),
            "-af", f"silencedetect=noise={SILENCE_NOISE_DB}dB:d={SILENCE_MIN_DUR}",
            "-f","null","-"
        ])
    except subprocess.CalledProcessError as e:
        out = e.output.decode("utf-8") if isinstance(e.output, bytes) else str(e.output)

    starts = [float(m.group(1)) for m in _s_start.finditer(out)]
    ends   = [float(m.group(1)) for m in _s_end.finditer(out)]
    cand: List[Tuple[float, float]] = []
    for t in starts + ends:
        if abs(t - target_sec) <= window_sec:
            cand.append((abs(t - target_sec), t))
    if not cand:
        return None
    cand.sort(key=lambda x: x[0])
    return cand[0][1]

def compute_splits(dur: float, infile: Path) -> List[float]:
    """
    総尺 dur に対して、90分・180分・…の各ターゲットで無音を探し、
    見つかればその秒、無ければターゲット秒で分割点を返す（終端は含めない）。
    返り値は昇順の分割点（秒）。
    """
    if dur <= SPLIT_CUTOFF_SEC:
        return []  # 分割不要

    splits: List[float] = []
    n_parts = math.ceil(dur / CHUNK_SEC)   # 目安のパート数
    for k in range(1, n_parts):            # dur 未満の位置だけ
        target = k * CHUNK_SEC
        if target >= dur - 1.0:
            break
        s = detect_silence_near(infile, target, SILENCE_WINDOW_SEC) or target
        if splits and abs(s - splits[-1]) < 1.0:
            continue
        splits.append(max(1.0, min(s, dur-1.0)))
    return sorted(splits)

# ======= メイン処理 =======
def process_file(src: Path):
    try:
        meta = ffprobe(src)
        dur  = get_duration_sec(meta)
        if dur <= 0:
            print(f"[SKIP] 長さ不明: {src}"); return

        base        = safe_name(src.stem)
        src_kbps    = get_source_kbps(meta)
        pic         = has_attached_pic(meta)
        orig_title  = get_tag(meta, "title") or base

        # 分割点計算
        splits = compute_splits(dur, src)  # [] なら単一
        cuts   = [0.0] + splits + [dur]

        total_parts = len(cuts) - 1
        if total_parts == 1:
            # 単一ファイル：ファイル名/タグ上書きなし
            length = cuts[1] - cuts[0]
            kbps   = choose_kbps(length, TARGET_MAX_BYTES, src_kbps)
            out    = OUT_DIR / f"{base}.m4a"
            encode_segment(src, cuts[0], length, out, kbps, pic,
                           title_override=None, disc_value=None, track_value=None)
            kbps   = ensure_under_target(src, cuts[0], length, out, kbps, pic,
                                         title_override=None, disc_value=None, track_value=None)
            print(f"[OK] {out}  {kbps}kbps  {out.stat().st_size/1024/1024:.1f}MB  ({length/60:.1f}分)")
        else:
            # 複数パート
            for i in range(total_parts):
                start  = cuts[i]
                end    = cuts[i+1]
                length = max(1.0, end - start)

                kbps   = choose_kbps(length, TARGET_MAX_BYTES, src_kbps)
                part_i = i + 1
                out    = OUT_DIR / f"{base}_part{part_i}.m4a"

                title_i = f"{orig_title} (Part {part_i})"
                disc_i  = f"{part_i}/{total_parts}"
                track_i = f"{part_i}/{total_parts}"

                encode_segment(src, start, length, out, kbps, pic,
                               title_override=title_i, disc_value=disc_i, track_value=track_i)
                kbps   = ensure_under_target(src, start, length, out, kbps, pic,
                                             title_override=title_i, disc_value=disc_i, track_value=track_i)
                print(f"  [P{part_i}] {out}  {kbps}kbps  {out.stat().st_size/1024/1024:.1f}MB  ({length/60:.1f}分)")

    except subprocess.CalledProcessError as e:
        print(f"[FFMPEG ERROR] {src}\n{e}")
    except Exception as e:
        print(f"[ERROR] {src}\n{e}")

def check_fftools() -> bool:
    try:
        subprocess.check_call(["ffmpeg","-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["ffprobe","-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def main():
    print(f"=== {APP_NAME} by {AUTHOR} ===")
    print(f"{APP_NAME} {VERSION}  by {AUTHOR}\n")

    if not check_fftools():
        print("[NG] ffmpeg / ffprobe が見つかりません。")
        print("     Homebrew があれば:  brew install ffmpeg")
        print("     （配布版は run.command から自動導入できます）\n")
        return

    IN_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] 入力フォルダ: {IN_DIR}")
    print(f"[INFO] 出力フォルダ: {OUT_DIR}")

    files = [p for p in IN_DIR.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    if not files:
        print("[INFO] input/ に音源を入れてから再実行してください。"); return
    for f in files:
        print(f"\n[PROCESS] {f}")
        process_file(f)

if __name__ == "__main__":
    main()