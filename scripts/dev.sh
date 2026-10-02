#!/usr/bin/env bash
# Local dev loop for the two Fidesa sites.
#
#   ./scripts/dev.sh start     build, then serve UK on :8080 and EN on :8081
#   ./scripts/dev.sh stop      stop both servers
#   ./scripts/dev.sh restart   stop, rebuild, start
#   ./scripts/dev.sh build     rebuild CSS + blog, leave servers running
#   ./scripts/dev.sh status    show what is running
#   ./scripts/dev.sh logs      tail both server logs
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="$ROOT/.dev"
UK_PORT=8080
EN_PORT=8081
PY=python3

mkdir -p "$STATE"
cd "$ROOT"

build() {
  "$PY" scripts/build_static.py
  "$PY" scripts/build_blog.py
}

start_one() {
  local site="$1" port="$2"
  if [ -f "$STATE/$site.pid" ] && kill -0 "$(cat "$STATE/$site.pid")" 2>/dev/null; then
    echo "$site-site already running (pid $(cat "$STATE/$site.pid"))"
    return
  fi
  nohup "$PY" scripts/dev_server.py --site "$site" --port "$port" \
    >"$STATE/$site.log" 2>&1 &
  echo $! >"$STATE/$site.pid"
  sleep 0.4
  echo "$site-site -> http://localhost:$port/"
}

stop_one() {
  local site="$1"
  if [ -f "$STATE/$site.pid" ]; then
    kill "$(cat "$STATE/$site.pid")" 2>/dev/null || true
    rm -f "$STATE/$site.pid"
    echo "$site-site stopped"
  fi
}

case "${1:-start}" in
  start)
    build
    start_one uk "$UK_PORT"
    start_one en "$EN_PORT"
    ;;
  stop)
    stop_one uk
    stop_one en
    ;;
  restart)
    stop_one uk; stop_one en
    build
    start_one uk "$UK_PORT"
    start_one en "$EN_PORT"
    ;;
  build)
    build
    ;;
  status)
    for site in uk en; do
      if [ -f "$STATE/$site.pid" ] && kill -0 "$(cat "$STATE/$site.pid")" 2>/dev/null; then
        echo "$site-site: running (pid $(cat "$STATE/$site.pid"))"
      else
        echo "$site-site: stopped"
      fi
    done
    ;;
  logs)
    tail -n 40 -f "$STATE"/uk.log "$STATE"/en.log
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|build|status|logs}" >&2
    exit 1
    ;;
esac
