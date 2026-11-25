#!/bin/zsh
# Asks one question in a fresh, isolated Claude Code session with a released kit bundle.
# usage: run.sh <kit-dir> <work-root> <name> <prompt> [resume-session-id]
#   kit-dir:  e.g. git archive v0.13.0-preview.2 .claude-plugin plugin.json skills | tar -x -C <kit-dir>
#   work-root: an empty folder outside any Git repository; each question gets <work-root>/<name>
# User settings, plugins and MCP servers are not loaded, so personal output styles cannot leak in.
set -u
KIT=$1; ROOT=$2; name=$3; prompt=$4; resume=${5:-}
dir=$ROOT/$name; mkdir -p $dir; cd $dir
turn=1; [ -n "$resume" ] && turn=2
args=(-p "$prompt" --plugin-dir $KIT --setting-sources project,local --strict-mcp-config --effort high
      --allowedTools "Skill WebSearch WebFetch Read Glob Grep Bash(python3:*)"
      --disallowedTools "Write Edit NotebookEdit" --output-format stream-json --verbose)
[ -n "$resume" ] && args+=(--resume $resume)
claude "${args[@]}" > $dir/turn$turn.jsonl 2> $dir/turn$turn.err
echo "$name turn$turn exit=$?"
