# -*- coding:utf-8 -*-
from pynput.keyboard import Listener, Key
import pyautogui as pag

coords = []
path = 'coords.txt'

def handleRelease(key):
    print('Released: {}'.format(key))

    if key == Key.insert:
        print('Insert is pressed')
        x, y = pag.position()
        coords.append([x, y])
    if key == Key.enter:
        # print('Enter is pressed')
        print(coords)
        with open(path, 'w') as f:
            f.write(str(coords))
        return False
    elif key == Key.esc:
        # print('Esc is pressed')
        # print(coords)
        return False

def save_click_position():
    with Listener(on_release=handleRelease) as listener:
        listener.join()

if __name__ == '__main__':
    save_click_position()