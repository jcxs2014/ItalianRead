#!/bin/bash
# ItalianRead 本地预览脚本
# 用法：./serve.sh          启动预览（默认端口 8080）
#       ./serve.sh build    仅构建到 site/public/
#       ./serve.sh clean    清理构建产物

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_DIR="$SCRIPT_DIR/site"
QUARTZ_DIR="$SITE_DIR/quartz"
OUTPUT_DIR="$SITE_DIR/public"
CONTENT_DIR="$SITE_DIR/content"
PORT=8080

show_help() {
    echo "用法："
    echo "  ./serve.sh          启动预览服务器（端口 8080）"
    echo "  ./serve.sh build    仅构建静态文件到 site/public/"
    echo "  ./serve.sh clean    清理构建产物"
}

cmd_build() {
    echo "Building..."
    cd "$QUARTZ_DIR"
    npx quartz build -d ../content 2>&1 | tail -5
    echo "Done"
}

cmd_serve() {
    [ ! -d "$QUARTZ_DIR/node_modules" ] && echo "Installing deps..." && cd "$QUARTZ_DIR" && npm install 2>&1 | tail -3
    PID=$(lsof -ti :$PORT 2>/dev/null)
    [ -n "$PID" ] && echo "Port $PORT occupied, killing..." && kill $PID 2>/dev/null && sleep 1

    cd "$QUARTZ_DIR"
    echo "Building..."
    npx quartz build -d ../content 2>&1 | tail -3
    echo "http://localhost:$PORT"
    echo "Ctrl+C to stop"
    (sleep 2 && open "http://localhost:$PORT") &
    npx serve public -l "tcp://0.0.0.0:$PORT"
}

cmd_clean() {
    [ -d "$OUTPUT_DIR" ] && rm -rf "$OUTPUT_DIR" && echo "Cleaned" || echo "Nothing to clean"
}

case "${1:-}" in
    -h|--help) show_help ;;
    build)     cmd_build ;;
    clean)     cmd_clean ;;
    "")        cmd_serve ;;
    *)         echo "Unknown arg: $1"; show_help; exit 1 ;;
esac
