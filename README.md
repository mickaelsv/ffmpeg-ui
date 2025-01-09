# ffmpeg ui 

![Python Version](https://img.shields.io/badge/Python-Required-blue) ![FFmpeg Version](https://img.shields.io/badge/FFmpeg-Required-blue) ![ffmpeg-python Version](https://img.shields.io/badge/ffmpeg--python-Required-blue) ![Tkinter Version](https://img.shields.io/badge/Tkinter-Required-blue)

## Overview

I made a simple UI to use FFMPEG commands that I use a lot.

The goal is to re encode videos, compress videos, or convert videos to audios.

## Setup

You first need to have [ffmpeg](https://www.ffmpeg.org/) installed on your computer. (If you are using linux it can be installed with apt/pacman or whatever, on windows you need to ensure ffmpeg is correctly added to path after installing)

You need to install the two libraries by running this command in the project folder :
`pip install -r requirements.txt`
which only installs ffmpeg-python (so you can just run `pip install ffmpeg-python`)

## Usage

Just run the python program with `python3 main.py`

With this program you can :
- Re-encode video to H.265 or HEVC (and also compressing them)
- Convert MP4 to MP3
- Compress an MP3

The complete details are in the code