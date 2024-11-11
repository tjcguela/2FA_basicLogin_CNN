'''Face Recog'''
from imutils.video import VideoStream
import itertools
import imutils
import time
import cv2
import face_recognition
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

'''System'''
import sys
import os
from threading import Thread