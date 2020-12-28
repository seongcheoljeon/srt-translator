# srt-translator
This is a script that converts subtitle files(*.srt) to Google Translate.

![test_run](test_run.gif)
![picture](result.png)

---

### Pre-setup
Python3
```shell script
pip3 install -r requirements.txt
```

```shell script
python main.py --rootdir=<srt directory path> --lang-source=[source language] --lang-target=[target language]
# or
python main.py --rootdir=<srt directory path> -ls [source language] -lt [target language]
# ex) converts English subtitles to Korean subtitles.
python main.py --rootdir=c:/test -ls en -lt ko
```
