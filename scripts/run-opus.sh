#!/bin/zsh
S=$WORKDIR; O="$OUTDIR"
for c in bare workflow; do for i in 1 2 3; do
  if [ $c = bare ]; then d=$S/empty; T=(--tools ""); else d=$S; T=(--tools "Read,Grep,Glob" --allowedTools "Read,Grep,Glob"); fi
  ( cd $d && claude -p "$(cat $S/prompt-$c.txt)" --model claude-opus-5-5 --effort medium "${T[@]}" --strict-mcp-config --disable-slash-commands --setting-sources "" > "$O/opus-5-5-medium-cc-$c-$i.md" 2> "$O/opus-5-5-medium-cc-$c-$i.err"; echo "opus-cc $c $i exit=$?" >> "$O/status.log" ) &
done; done; wait; echo OPUSDONE >> "$O/status.log"
