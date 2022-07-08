Install spleeter with
`pip install spleeter`
(You might need to install `ffmpeg` and `libsndfile` first. If so, either create
a conda environment as described [here](https://github.com/deezer/spleeter) or (what I did
) install `libsndfile` from terminal with `apt-get`).

Adapt the path variables in the `separator.py` file.

[optional] Also adapt the other variables depending on how many splits you want and which backend STFT.

Run `separator.py`.