# convert mkvs to mp4 for web streaming

for f in */*.mkv
do
	f2=$(basename -- "$f" .mkv)
	dir=$(dirname "$f")
	if [ -f "${dir}/${f2}.mp4" ]; then
		echo SKIPPING: $f
	else
		echo CONVERTING: $f
    
		ffmpeg \
			-hide_banner -nostats -y -loglevel panic \
			-i "$f" \
			-tune zerolatency \
			-movflags +faststart \
			-c:v libx264 \
			-c:a aac \
			"${f}-out.mp4"

		echo COMPLETE
	fi
done
