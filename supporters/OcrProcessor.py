# -*- coding:utf-8 -*-

##@@@@========================================================================
##@@@@ Libraries

##@@@-------------------------------------------------------------------------
##@@@ Basic Libraries
import sys, os
import math

##@@@-------------------------------------------------------------------------
##@@@ Installed(conda/pip) Libraries
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pyautogui as pag
import pytesseract

class OcrProcessor:
    def __init__(self, source=None, target=None, box=[0, 0, 1920, 1080]):
        self.source = source
        self.target = target
        self.box = box