#!/usr/bin/env bash
# Classroom runner: pick a session, pick a script, run it.
#
#   ./run.sh                      menu: session -> script -> provider
#   ./run.sh 01                   menu of session-01's scripts
#   ./run.sh 01 2                 run session-01's 2nd script
#   ./run.sh 01 01_first_call.py  run it by name
#   ./run.sh 01 all               run every script of session-01 in order
#   ./run.sh 01 test              offline tests for session-01
#   ./run.sh check                setup check (Python, venv, packages, keys, one live call); ./run.sh 03 check for session-03
#   ./run.sh -l                   list sessions and their scripts
#
# Options (before or after the session): -f / --fake  offline, no key (PROVIDER=fake)
#                                        -p NAME      provider: nvidia | gemini | openai | anthropic | fake
#                                        -s / --serve start the web server at the end of an API script (SERVE=1)
# The session's .venv is created on first use (no make needed; bash 3.2+, so stock macOS works).
# Keys come from .env: one at the repo root serves every session (a session folder's own .env wins).
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1          # no __pycache__ folders in the session folders

PROV=""; ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    -f|--fake) PROV=fake ;;
    -s|--serve) export SERVE=1 ;;
    -p|--provider) PROV="${2:?provider name}"; shift ;;
    -l|--list) ARGS+=(--list) ;;
    -h|--help) sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) ARGS+=("$1") ;;
  esac; shift
done
set -- "${ARGS[@]+"${ARGS[@]}"}"

title() { head -1 "sessions/session-$1/README.md" 2>/dev/null | sed 's/^# *//'; }
scripts() { (cd "sessions/session-$1" && ls [0-9][0-9]_*.py 2>/dev/null) || true; }
sessions() { ls -d sessions/session-[0-9][0-9] | sed 's|sessions/session-||'; }

if [ "${1:-}" = "--list" ]; then
  for s in $(sessions); do echo "$s  $(title "$s")"; scripts "$s" | nl -w6 -s'  '; done; exit 0
fi

# --- session --------------------------------------------------------------------------------------------
[ "${1:-}" = check ] && set -- 01 check
S="${1:-}"
if [ -z "$S" ]; then
  LIST=(); while IFS= read -r l; do LIST+=("$l"); done < <(for s in $(sessions); do echo "$s  $(title "$s")"; done)
  PS3=$'\nSession number (Enter to show the list again): '
  select pick in "${LIST[@]}"; do [ -n "$pick" ] && { S="${pick%% *}"; break; }; done
fi
S=$(printf '%02d' "$((10#$S))")
DIR="sessions/session-$S"
[ -d "$DIR" ] || { echo "No $DIR. Try ./run.sh -l"; exit 1; }
setup() {  # the session's .venv
  echo "Setting up $DIR/.venv (first run only, about a minute)..."
  if [ -f "$DIR/Makefile" ] && grep -q '^install:' "$DIR/Makefile"; then make -s -C "$DIR" install
  else (cd "$DIR" && python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt); fi
}
[ -x "$DIR/.venv/bin/python" ] || setup
# generated input files (images, PDFs, audio are not in git): data/make_*.py create missing ones, silent otherwise
for g in "$DIR"/data/make_*.py; do [ -f "$g" ] && (cd "$DIR" && .venv/bin/python "data/${g##*/}"); done

FILES=(); while IFS= read -r l; do FILES+=("$l"); done < <(scripts "$S")
[ ${#FILES[@]} -gt 0 ] || { echo "$DIR has no numbered scripts."; exit 1; }

# --- script ---------------------------------------------------------------------------------------------
F="${2:-}"
if [ -z "$F" ]; then
  echo; echo "$(title "$S")"
  PS3=$'\nScript number: '
  select pick in "${FILES[@]}" "check (setup check)" "all (run every script)" "test (offline tests)" quit; do
    case "$pick" in "") continue ;; quit) exit 0 ;; check*) F=check ;; all*) F=all ;; test*) F=test ;; *) F="$pick" ;; esac; break
  done
  if [ -z "$PROV" ] && [ "$F" != test ] && [ "$F" != check ]; then
    PS3=$'\nProvider: '
    select pick in "default (from .env)" "fake (offline, no key)" nvidia gemini openai anthropic; do
      case "$pick" in "") continue ;; default*) ;; fake*) PROV=fake ;; *) PROV="$pick" ;; esac; break
    done
  fi
elif [[ "$F" =~ ^[0-9]+$ ]] && [ "$F" -ge 1 ] && [ "$F" -le ${#FILES[@]} ]; then
  F="${FILES[$((F-1))]}"
fi
[ -n "$PROV" ] && export PROVIDER="$PROV"

# --- run ------------------------------------------------------------------------------------------------
cd "$DIR"
run_one() {
  printf '\n\033[1m=== %s/%s%s ===\033[0m\n' "$DIR" "$1" "${PROVIDER:+  (PROVIDER=$PROVIDER)}"
  .venv/bin/python "$1"
}
case "$F" in
  check) .venv/bin/python ../session-01/00_check_setup.py ;;
  test) PROVIDER=fake .venv/bin/python -m pytest -q -p no:cacheprovider ;;
  all)  for f in "${FILES[@]}"; do run_one "$f"; done ;;
  *)    [ -f "$F" ] || { echo "No $DIR/$F. Scripts: ${FILES[*]}"; exit 1; }; run_one "$F" ;;
esac
