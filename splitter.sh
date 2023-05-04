cd /home/final/gtfs
tail -n +2 /home/final/gtfs/stop_times.txt | split -d --line-bytes=100M - stop_chunk_
cd ..