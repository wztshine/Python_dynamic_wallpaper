# VideoWallpaper  
A demo of video wallpaper for python3. Clone from: [myd510](https://github.com/myd510/VideoWallpaper)

## USE  
1. run`pip install -r requirements.txt`to install the library  
2. Edit `config.json`
3. Execute `run.py`

## BUGS  

When use `win+tab` shortcut, it will appear the original wallpaper.

## NOTES  
This project uses the GPL3.0 open source license 

## THANKS  
https://www.codeproject.com/Articles/856020/Draw-Behind-Desktop-Icons-in-Windows-plus 

## 原理
当向 Program Manager 这个 windows 窗口发送消息 "0x52C" 后，该窗口会出现两个 workerW 窗口(本质是将壁纸设成 ”幻灯片放映“ 类似的操作)。

一个 workerW 窗口用来呈现桌面图标，另一个 workerW 窗口用来呈现静态壁纸。这样我们就可以将任意动态壁纸程序设置成 Program Manager 窗口子窗口，并隐藏掉静态壁纸的 workerW 窗口，就能实现自定义动态壁纸了。

