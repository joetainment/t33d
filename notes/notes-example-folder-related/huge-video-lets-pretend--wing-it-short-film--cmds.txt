

Commands used to quickly make the smaller short version of the movie:


python -m pip install --user -U yt_dlp

python -m yt_dlp -S +size,+br https://youtu.be/u9lj-c29dxI

ffmpeg -i "WING IT! - Blender Open Movie [u9lj-c29dxI].mkv" -an wing-it.mkv

ffmpeg -i  wing-it.mkv  -vf "scale=trunc(iw/4)*2:trunc(ih/4)*2" -an -ss 00:01:30.00 -to 00:01:40.00 huge-video-lets-pretend--wing-it-short-film.webm