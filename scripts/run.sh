#!/bin/zsh
S=$WORKDIR; O="$OUTDIR"
run() { m=$1; c=$2; i=$3
  if [ $c = bare ]; then d=$S/empty; else d=$S; fi
  (cd $d && agy -p "$(cat $S/prompt-$c.txt)" --model $m --sandbox > "$O/$m-$c-$i.md" 2> "$O/$m-$c-$i.err"; echo "$m $c $i exit=$?" >> "$O/status.log") }
for m in gemini-4-neon-medium claude-opus-5-5-medium; do for c in bare workflow; do for i in 1 2 3; do run $m $c $i & done; done; done
wait; echo ALLDONE >> "$O/status.log"
