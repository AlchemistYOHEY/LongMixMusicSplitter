LongMix Music Splitter for Mac  by Alchemist YOHEY
---------------------------------

【概要】
Apple iCloudミュージックの要件:
- 1ファイル 200MB 未満
- ビットレート 96kbps 以上
- 推奨: AAC / 44.1kHz / ステレオ

この要件を満たさない長時間音源（パーティー用ミックス等）は iCloud にアップされず、
iPhoneやMacに同期されません。本ツールはこの要件を満たすように音声ファイルを
自動で変換・分割するために作りました。

⚠️ 注意: 本ツールは **Mac専用** です。Windowsでは動作しません。  
※本プロジェクトは **Apple Inc. とは一切関係がなく、承認・提携・支援を受けていません**。  
「Apple」「iCloud」「iPhone」「Mac」は Apple Inc. の商標です。記載は説明目的のみです。

---------------------------------
【フォルダ構成】
- input/ …… 音源を入れるフォルダ
- longmix_music_splitter.py …… 本体スクリプト
- output/ …… 変換結果が書き出されるフォルダ
- README.txt …… この説明
- run.command …… 起動用（ダブルクリック）

---------------------------------
【使い方】
1) run.command をダブルクリック → ターミナルが起動します。  
   初回で Gatekeeper で止まる場合は「右クリック > 開く」で許可。

2) ffmpeg / ffprobe が無い場合、質問が出ます:  
   「導入しますか？ (y/N)」  
     - y + Enter → Homebrew と ffmpeg を自動導入  
     - N → 終了（手動で `brew install ffmpeg` が必要）

3) input フォルダに音源を入れて run.command を再実行 → output に .m4a が生成。

---------------------------------
【仕様】
- 出力: AAC .m4a / 44.1kHz / ステレオ
- サイズ: 自動で 200MB 未満（下限112kbps）
- 分割: 2時間未満は単一、2時間以上は 約90分間隔で可変パート分割
        （目標付近の無音を優先、無ければキッカリ分割）
- メタデータ/アートワーク保持（可能な範囲）
- 分割時はファイル名に _part1/_part2/...、titleに (Part i)、disc/track に i/N を付与

---------------------------------
【既存ツールとの比較】
- Magic Cutter: 無音検出で自動分割は可能だが、iCloudミュージックのサイズ/フォーマット制限に最適化されていない。  
- Audacity: 高機能なオーディオエディタ。手動で分割できるが、ユーザーの手間が多くフォーマット調整も必要。  
- Mp3splt: 無音検出対応のCLIベース分割ツール。ただし iCloud 用の制約を考慮した機能はない。  
- LongMix Music Splitter for Mac: iCloud対応ファイル（200MB未満、AAC/44.1kHz/ステレオ）を自動生成。
  約90分付近の無音で自動分割し、メタデータも保持。

---------------------------------
【実行の流れ】
- ダブルクリック → ターミナルでログ表示
- ffmpegが無ければ y/N プロンプト → yで自動インストール
- 変換ログが流れ、終了時に「キーを押すと閉じます…」
- input/ → output/ で完結（Mac専用）

---------------------------------
Author: Alchemist YOHEY


==============================
English Explanation
==============================

LongMix Music Splitter for Mac  by Alchemist YOHEY
---------------------------------

[Overview]  
Apple iCloud Music requirements:  
- File size under 200MB  
- Bitrate above 96kbps  
- Recommended: AAC / 44.1kHz / stereo  

If an audio file (e.g., a long party mix) does not meet these requirements, it won’t upload to iCloud and thus won’t sync to iPhone or Mac.  
This tool automatically converts and splits audio to meet those requirements.

⚠️ Note: This tool is **Mac only**; it will not run on Windows.  
Disclaimer: **This project is not affiliated with, endorsed by, or sponsored by Apple Inc.**  
“Apple”, “iCloud”, “iPhone”, and “Mac” are trademarks of Apple Inc., used here for descriptive purposes only.

---------------------------------
[Folder Structure]
- input/ …… put audio files here
- longmix_music_splitter.py …… main script
- output/ …… converted files appear here
- README.txt …… this document
- run.command …… launcher (double-click)

---------------------------------
[Usage]
1) Double-click run.command → Terminal opens.  
   If blocked by Gatekeeper on first launch, use “Right click > Open” to allow.

2) If ffmpeg / ffprobe are missing, you’ll be prompted:  
   “Install now? (y/N)”  
     - y + Enter → Automatically installs Homebrew and ffmpeg  
     - N → Exit (you’ll need `brew install ffmpeg` manually)

3) Put audio into input/ and run again → .m4a files appear in output/.

---------------------------------
[Features]
- Output: AAC .m4a / 44.1kHz / stereo  
- Size: Automatically kept under 200MB (minimum 112kbps)  
- Splitting: Single file if <2h; if ≥2h, split into ~90min parts, preferring nearby silence, else split exactly.  
- Metadata/cover art preserved when possible  
- When split, filenames use _part1/_part2/…, titles append “(Part i)”, and disc/track are set to i/N.

---------------------------------
[Comparison with existing tools]
- Magic Cutter: Auto-splits using silence detection, but not optimized for iCloud Music size/format restrictions.  
- Audacity: Powerful editor; manual splitting possible but requires user effort and format adjustments.  
- Mp3splt: CLI-based splitter with silence detection; no built-in support for iCloud constraints.  
- LongMix Music Splitter for Mac: Specifically designed to create iCloud-compatible files (<200MB, AAC/44.1kHz/stereo), auto-splitting near 90min silence with metadata preserved.

---------------------------------
[Flow]
- Double-click → Terminal shows logs  
- If ffmpeg is missing, prompt y/N → y installs automatically  
- Logs stream; at the end “Press any key to close…”  
- input/ → output/ workflow (Mac only)

---------------------------------
Author: Alchemist YOHEY
