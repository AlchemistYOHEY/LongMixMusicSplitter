#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="$DIR/longmix_music_splitter.py"

echo "=== LongMix Music Splitter for Mac by Alchemist YOHEY ==="

need_ff() { ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; }

install_brew() {
  echo "[INFO] Homebrew をインストールします"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [ -x /opt/homebrew/bin/brew ]; then
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [ -x /usr/local/bin/brew ]; then
    echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/usr/local/bin/brew shellenv)"
  fi
}

install_ffmpeg() {
  if ! command -v brew >/dev/null 2>&1; then
    echo "[WARN] Homebrew がありません。インストールしますか？ (y/N)"
    read ans
    if [[ "$ans" == [yY] ]]; then
      install_brew
    else
      echo "[NG] ffmpeg を入れるには Homebrew が必要です。終了します。"
      read -n 1 -s "?キーを押すと閉じます…"
      exit 1
    fi
  fi
  echo "[INFO] ffmpeg をインストールします…"
  brew install ffmpeg
}

if need_ff; then
  echo "[INFO] ffmpeg / ffprobe が見つかりません。導入しますか？ (y/N)"
  read ans
  if [[ "$ans" == [yY] ]]; then
    install_ffmpeg
  else
    echo "[NG] ffmpeg が無いと実行できません。"
    read -n 1 -s "?キーを押すと閉じます…"
    exit 1
  fi
fi

/usr/bin/env python3 "$PY"

echo
read -n 1 -s "?完了。キーを押すと閉じます…"
