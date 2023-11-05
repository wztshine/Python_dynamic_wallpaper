import win32gui
from win32con import SW_HIDE, SMTO_ABORTIFHUNG
from win32gui import FindWindow, FindWindowEx, ShowWindow, SendMessageTimeout, SetParent, EnumWindows, GetWindowText


def _MyCallback(hwnd, extra):
    # 当前窗口中查找图标窗口
    icon_window = FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
    if icon_window:  # 当前窗口包含图标窗口
        # 查找静态壁纸窗口并保存
        extra[0] = FindWindowEx(None, hwnd, "WorkerW", None)


def RunVideoWallpaper(video_window_handle):  # 设置视频壁纸
    if video_window_handle:
        # 查找桌面窗口
        desktop_window_handle = FindWindow("Progman", "Program Manager")
        # 设置 video_window 为 desktop_window 的子窗口
        SetParent(video_window_handle, desktop_window_handle)
        # 核心语句，向 desktop_window 发送 0x52C 启用 Active Desktop
        SendMessageTimeout(desktop_window_handle, 0x52C, 0, 0, SMTO_ABORTIFHUNG, 500)
        # 因为有两个同类同名的WorkerW窗口，所以遍历所有顶层窗口
        workerw = [0]
        EnumWindows(_MyCallback, workerw)
        # 获取 video_window 的名称
        video_window_name = GetWindowText(video_window_handle)

        # 隐藏静态壁纸窗口
        ShowWindow(workerw[0], SW_HIDE)
        # 判断 video_window 是否是 desktop_window 的子窗口
        video_window_handle_2 = FindWindowEx(desktop_window_handle, None, "SDL_app", video_window_name)
        if video_window_handle_2 == 0:
            # 将 video_window 设置为 desktop_window 的子窗口
            SetParent(video_window_handle, desktop_window_handle)

def find_window_by_name(name: str) -> tuple[int, str]:
    """根据窗口名字关键字，获取窗口的句柄和标题全名。

    :param name: 窗口名字关键字
    :return: (句柄, 窗口标题)
    """
    all_windows = {}

    def callback(hd, arg):
        if win32gui.IsWindow(hd) and win32gui.IsWindowVisible(hd) and win32gui.IsWindowEnabled(hd):
            title = win32gui.GetWindowText(hd)
            if name in title:
                all_windows[hd] = title

    win32gui.EnumWindows(callback, 0)
    if all_windows:
        return list(all_windows.items())[0]
    return 0, ""
