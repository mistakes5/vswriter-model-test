#!/bin/zsh
S=$WORKDIR; O="$OUTDIR"; cd $S
for i in 1 2 3; do
 ( agy -p "$(cat prompt-nuanced.txt)" --model gemini-4-neon-medium --sandbox > "$O/gemini-4-neon-medium-nuanced-$i.md" 2>"$O/gemini-4-neon-medium-nuanced-$i.err"; echo "gem nuanced $i $?" >> "$O/status.log" ) &
 ( claude -p "$(cat prompt-nuanced.txt)" --model claude-opus-5-5 --effort medium --tools "Read,Grep,Glob" --allowedTools "Read,Grep,Glob" --strict-mcp-config --disable-slash-commands --setting-sources "" > "$O/opus-5-5-medium-cc-nuanced-$i.md" 2>"$O/opus-5-5-medium-cc-nuanced-$i.err"; echo "opus nuanced $i $?" >> "$O/status.log" ) &
done; wait; echo NUANCEDDONE >> "$O/status.log"
