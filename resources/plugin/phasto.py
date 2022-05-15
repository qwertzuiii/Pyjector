import json
from os import system
import msvcrt as mv
import ctypes as cty
import webbrowser
import requests
import zipfile as zf

class clr:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    resc = "\u001b[0m"


def next_line(NUMBER):
    for i in range(NUMBER):
        print()

class os:
    def clear():
        system('cls')
    def one_input():
        return mv.getch()
    class window:
        def title(TITLE_OF_WINDOW):
            cty.windll.kernel32.SetConsoleTitleW(TITLE_OF_WINDOW)

class file:
    def read(FILENAME):
        return open(FILENAME, 'r').read()
    def read_bytes(FILENAME):
        return open(FILENAME, 'rb').read()
    def read_json(FILENAME_OF_JSON):
        return json.loads(open(FILENAME_OF_JSON, 'r').read())

    def write(FILENAME, TEXT_TO_WRITE):
        open(FILENAME, 'w').write(TEXT_TO_WRITE)
    def write_bytes(FILENAME, TEXT_TO_WRITE):
        open(FILENAME, 'wb').write(TEXT_TO_WRITE)

    def unzip(ZIPFILE, PATH):
        with zf.ZipFile(ZIPFILE) as mz:
            mz.extractall(PATH)

    def conv_json(TEXT_TO_CONVERT):
        return json.loads(TEXT_TO_CONVERT)

class web:
    def open(link):
        webbrowser.open(link)
    def getcontent(link, redirects=True):
        this = requests.get(link, allow_redirects=redirects)
        return this.content
