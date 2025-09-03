LongMix Music Splitter for Mac  by Alchemist YOHEY
---------------------------------

【概要】
Apple iCloudミュージックの要件:
- 1ファイル 200MB 未満
- ビットレート 96kbps 以上
- 推奨: AAC / 44.1kHz / ステレオ

この要件を満たさない長時間音源（パーティー用ミックス等）は iCloud にアップされず、
iPhoneやMacに同期されません。本ツールはこの要件を満たすように音声ファイルを
自動で変換・分割します。

※本ツールは Mac専用。Apple Inc. とは無関係（非提携・非承認・非支援）。
“Apple”“iCloud”“iPhone”“Mac” は Apple Inc. の商標（説明目的の記載）。

---------------------------------
【フォルダ構成】
- input/ …… 音源を入れる
- longmix_music_splitter.py …… 本体スクリプト
- output/ …… 変換結果の出力先
- README.txt …… この説明
- run.command …… 起動用（ダブルクリック）

---------------------------------
【使い方】
1) run.command をダブルクリック → ターミナル起動
   ＜初回起動時（Gatekeeper）＞
   未署名のため「開けませんでした」と出る場合:
   a)  > システム設定 > プライバシーとセキュリティ
   b) 画面下部「“run.command” は開けませんでした」→［このまま開く］
   c) 確認ダイアログで［開く］ → 2回目以降は通常起動可

2) ffmpeg / ffprobe が無い場合、プロンプト:
   「導入しますか？ (y/N)」
     - y + Enter → Homebrew と ffmpeg を自動導入
     - N → 終了（手動で `brew install ffmpeg` が必要）

3) input に音源を入れて run.command を再実行 → output に .m4a 生成

---------------------------------
【仕様】
- 出力: AAC .m4a / 44.1kHz / ステレオ
- サイズ: 自動で 200MB 未満（下限112kbps）
- 分割: 2時間未満=単一、2時間以上=約90分単位（無音優先、無ければ強制）
- メタデータ/アートワーク保持（可能な範囲）
- 分割時: _part1/_part2/... 付与、title に (Part i)、disc/track に i/N

---------------------------------
【比較】
- Magic Cutter: 無音分割可だが iCloud 制約に最適化なし
- Audacity: 強力だが手動操作と形式調整が必要
- Mp3splt: CLIで無音分割可。iCloud向け自動調整なし
- LongMix Music Splitter for Mac: iCloud向け(<200MB, AAC/44.1kHz/ステレオ)を自動生成、約90分無音で分割、メタ保持

---------------------------------
【ダウンロード（最新版）】
https://github.com/AlchemistYOHEY/LongMixMusicSplitter/releases/latest

---------------------------------
【謝辞】
このツールのコード生成には ChatGPT を活用しました。
要件定義・調整・テストは Alchemist YOHEY が実施。

==============================
English
==============================

[Overview]
- iCloud limits: <200MB / >96kbps / recommended AAC 44.1kHz stereo
- This tool auto-converts/splits long mixes to meet those limits
- macOS only. Not affiliated with Apple Inc. (“Apple”, “iCloud”, “iPhone”, “Mac” are trademarks)

[Folder Structure]
- input/ : put audio files here
- longmix_music_splitter.py : main script
- output/ : converted files
- README.txt : this document
- run.command : launcher

[Usage]
1) Double-click run.command (Terminal opens)
   First run (Gatekeeper):
   a)  > System Settings > Privacy & Security
   b) “run.command was blocked” → Open Anyway
   c) Confirm: Open → next runs work normally
2) If ffmpeg/ffprobe are missing: “Install now? (y/N)”
   - y: auto-install Homebrew + ffmpeg
   - N: exit (manual `brew install ffmpeg`)
3) Put audio into input/ → run again → .m4a in output/

[Features]
- AAC .m4a / 44.1kHz / stereo
- Under 200MB automatically (min 112kbps)
- Split: <2h single / ≥2h ~90min (prefer silence, else hard split)
- Preserve metadata/cover art when possible
- When split: _part1/_part2/…, title “(Part i)”, disc/track i/N

[Download]
https://github.com/AlchemistYOHEY/LongMixMusicSplitter/releases/latest

[Acknowledgement]
Developed with the help of ChatGPT. Adjustments/testing by Alchemist YOHEY.
