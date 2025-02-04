# from pynput import keyboard
# import time
# import pyautogui
#
# # 全局变量，用于标记是否模拟按下 "z" 键
# simulate_z = False
#
# # 键盘按下事件回调函数
# def on_key_press(key):
#     global simulate_z
#
#     if key == keyboard.Key.f7:
#         if simulate_z:
#             simulate_z = False
#             print("停止模拟按下 'z' 键")
#         else:
#             simulate_z = True
#             print("开始模拟按下 'z' 键")
#
# # 键盘释放事件回调函数
# def on_key_release(key):
#     pass
#
# # 创建键盘监听器
# listener = keyboard.Listener(
#     on_press=on_key_press,
#     on_release=on_key_release)
# listener.start()
#
# # 模拟按下 "z" 键的函数
# def simulate_z_key():
#     while simulate_z:
#         # 模拟按下 "z" 键
#         pyautogui.press('z',presses=1)
#         pyautogui.press('left',presses=1)
#
#
# # 主程序循环
# while True:
#     if simulate_z:
#         simulate_z_key()
import time

import keyboard

# 模拟按下 "z" 键和方向键左键的函数
def simulate_z_and_left_key():
    flas = False
    while True:
        if keyboard.is_pressed('f7'):
            flas=~flas
            # print("开始模拟按下 'z' 键和方向键左键")
            # keyboard.press('z')

            # keyboard.press('left')
            # keyboard.release('left')
            time.sleep(0.1)
        if flas:
            # keyboard.press('z')
            keyboard.press('a')
            time.sleep(0.1)
            # keyboard.release('z')
            keyboard.release('a')

# 主程序循环
while True:
    simulate_z_and_left_key()
    
    
    
'''
zzz
zzzzzzzzzzzzaaaaaaa
zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
'''