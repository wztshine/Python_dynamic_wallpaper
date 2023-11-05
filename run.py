import atexit
import ctypes
import pathlib
from time import sleep
import winsound
import json
import psutil
import win32api
import win32process
from win32api import GetSystemMetrics
from win32con import SM_CXSCREEN, SM_CYSCREEN
from win32process import CreateProcess, CREATE_NO_WINDOW, STARTUPINFO

import VideoWallpaper

# 限制 UI 缩放
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

if __name__ == "__main__":
    # 获得屏幕分辨率
    screen_width = GetSystemMetrics(SM_CXSCREEN)
    screen_height = GetSystemMetrics(SM_CYSCREEN)

    with open("config.json", "r", encoding='utf-8') as f:
        CONFIG = json.load(f)
    video_path = pathlib.PurePath(CONFIG["video_path"])
    ffplay_path = CONFIG["ffplay_path"]
    # 播放设置
    cmdline = f"-fs -x {screen_width} -y {screen_height} -loop 0 \"{str(video_path)}\" {CONFIG['ffplay_cmd_config']}"
    # 创建播放器进程(无窗口)
    CreateProcess(ffplay_path, cmdline, None, None, 0, CREATE_NO_WINDOW, None, None, STARTUPINFO())
    while True:
        # 查找播放器窗口
        player_window_handel = VideoWallpaper.find_window_by_name(video_path.stem)[0]
        if player_window_handel != 0:  # 找到播放器窗口
            # 视频窗口窗口原点会不在00，sleep可以解决
            sleep(0.1)
            break
        sleep(.1)
    # 启动视频壁纸
    VideoWallpaper.RunVideoWallpaper(player_window_handel)


    def kill_ffplay(signal_type=None):
        print(signal_type)
        print("Kill ffplay to stop playing video.")
        winsound.Beep(800, 100)
        _, pid = win32process.GetWindowThreadProcessId(player_window_handel)
        p = psutil.Process(pid)
        p.kill()


    atexit.register(kill_ffplay)
    win32api.SetConsoleCtrlHandler(kill_ffplay, True)
    while True:
        input("")
