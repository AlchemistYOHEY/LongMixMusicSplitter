# LongMix Music Splitter for Mac  
by Alchemist YOHEY  
**Version: v1.2.2**

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Platform: macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)
![Language: Python3](https://img.shields.io/badge/Language-Python3-blue.svg)

---

## 概要
Apple iCloudミュージックの要件:
- 1ファイル 200MB 未満
- ビットレート 96kbps 以上
- 推奨: AAC / 44.1kHz / ステレオ

この要件を満たさない長時間音源（パーティー用ミックス等）は iCloud にアップされず、iPhoneやMacに同期されません。本ツールはこの要件を満たすように音声ファイルを**自動で変換・分割**します。

> 注意: 本ツールは **Mac専用**（Windows不可）。  
> 免責: 本プロジェクトは **Apple Inc. と無関係**（非提携・非承認・非支援）。  
> “Apple”“iCloud”“iPhone”“Mac” は Apple Inc. の商標（説明目的の記載）。

---

## フォルダ構成
- `input/` : 音源を入れるフォルダ  
- `longmix_music_splitter.py` : 本体スクリプト  
- `output/` : 変換結果の出力先  
- `README.txt` : 配布zip用テキスト版  
- `README.md` : GitHub表示用（このファイル）  
- `run.command` : 起動用（ダブルクリック）  

---

## 使い方
1. **`run.command` をダブルクリック** → ターミナルが起動。

   ### 初回起動時の注意（Gatekeeper）
   未署名のため初回は「開けませんでした」と警告される場合あり。  
   許可手順:
   a)  > システム設定 > プライバシーとセキュリティ  
   b) 画面下部の「“run.command” は開けませんでした」→ **[このまま開く]**  
   c) 確認ダイアログで **[開く]**  
   → 2回目以降は通常のダブルクリックで起動可。

2. **ffmpeg / ffprobe が無い場合はプロンプト**  
   「導入しますか？ (y/N)」  
   - `y` + Enter → Homebrew と ffmpeg を自動導入  
   - `N` → 終了（手動で `brew install ffmpeg` が必要）

3. **`input/` に音源を入れて `run.command` を再実行** → `output/` に `.m4a` が生成。

---

## 仕様
- 出力: AAC `.m4a` / 44.1kHz / ステレオ  
- サイズ: 自動で 200MB 未満（下限 112 kbps）  
- 分割:
  - 2時間未満 → 単一ファイル  
  - 2時間以上 → 約90分ごと（近傍の無音を優先、無ければ強制分割）  
- メタデータ/アートワーク保持（可能な範囲）  
- 分割時: ファイル名 `_part1/_part2/...`、タイトルに `(Part i)`、`disc/track = i/N`

---

## 既存ツールとの比較
- **Magic Cutter**: 無音分割は可能だが、iCloudのサイズ/フォーマット制約に最適化されていない。  
- **Audacity**: 高機能だが手動操作と形式調整が必要。  
- **Mp3splt**: CLIで無音分割可。ただし iCloud 制約の自動調整なし。  
- **LongMix Music Splitter for Mac**: iCloud向け（<200MB, AAC/44.1kHz/ステレオ）を自動生成。約90分付近の無音で自動分割、メタ保持。

---

## ダウンロード
👉 **最新リリース**: https://github.com/AlchemistYOHEY/LongMixMusicSplitter/releases/latest

---

## 謝辞
このツールのコード生成には **ChatGPT** を活用しました。  
要件定義・調整・テストは **Alchemist YOHEY** が実施。

---

# English

## Overview
Apple iCloud Music requirements:
- File size under 200MB
- Bitrate above 96kbps
- Recommended: AAC / 44.1kHz / stereo

If a long mix doesn’t meet these, it won’t upload to iCloud and won’t sync to iPhone/Mac. This tool **automatically converts and splits** audio to meet the requirements.

> Note: **macOS only**.  
> Disclaimer: **Not affiliated with Apple Inc.**  
> “Apple”, “iCloud”, “iPhone”, and “Mac” are trademarks of Apple Inc., used for descriptive purposes only.

---

## Folder Structure
- `input/` : put audio files here  
- `longmix_music_splitter.py` : main script  
- `output/` : converted files appear here  
- `README.txt` : plain text for end users  
- `README.md` : this Markdown  
- `run.command` : launcher (double-click)  

---

## Usage
1. **Double-click `run.command`** → Terminal opens.

   ### Gatekeeper warning on first launch
   Since the app is unsigned, macOS may show “can’t be opened”.  
   Allow it:
   a)  > System Settings > Privacy & Security  
   b) At the bottom, “run.command was blocked” → **Open Anyway**  
   c) In the confirmation dialog, **Open**  
   → From the second run onwards, double-click works normally.

2. **If ffmpeg / ffprobe are missing**  
   Prompt: “Install now? (y/N)”  
   - `y` + Enter → Installs Homebrew and ffmpeg automatically  
   - `N` → Exit (manual `brew install ffmpeg` required)

3. **Put audio into `input/` and run again** → `.m4a` files appear in `output/`.

---

## Features
- Output: AAC `.m4a` / 44.1kHz / stereo  
- Size: kept under 200MB automatically (min 112 kbps)  
- Splitting:
  - <2h → single file  
  - ≥2h → ~90min parts (prefer nearby silence; else hard split)  
- Metadata/cover art preserved when possible  
- When split: filenames `_part1/_part2/...`, titles “(Part i)”, `disc/track = i/N`

---

## Comparison with existing tools
- **Magic Cutter**: Auto-splits with silence detection, but not optimized for iCloud size/format limits.  
- **Audacity**: Powerful editor; manual splitting/format tweaks required.  
- **Mp3splt**: CLI splitter with silence detection; no iCloud-specific constraints handling.  
- **LongMix Music Splitter for Mac**: Produces iCloud-ready files (<200MB, AAC/44.1kHz/stereo), auto-splits near ~90min silence, preserves metadata.

---

## Download
👉 **Latest release**: https://github.com/AlchemistYOHEY/LongMixMusicSplitter/releases/latest

---

## Acknowledgement
Developed with the help of **ChatGPT**.  
Requirements, adjustments, and testing by **Alchemist YOHEY**.
