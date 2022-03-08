
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
from os import path

import uuid

import sys

import json

import socket
import threading
import time

code = ''
files = []

# fuck import
# получаем названия файлов с нужными объктами
file_objects = (open('objects/objects.list', 'r', encoding="utf-8").read()).split('\n') #
for i in range(len(file_objects)-1): #
    files.append([file_objects[i], 0])
    print('IMPORT: ' + file_objects[i])

# чтение файлов содержащих в себе классы
for i in range(len(files)): #
    file_objects = open('objects/' + files[i][0], 'r', encoding="utf-8") #
    code += file_objects.read() + '\n' #
    files[i][1] = len(code.split('\n')) #
    file_objects.close() #

print('STRING: '  +str(len(code.split('\n')))) #
exec(code) # запуск всего кода который мы прочитали из файлов
