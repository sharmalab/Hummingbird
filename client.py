import requests
import logging
logging.basicConfig(level=logging.INFO)


def init():
    files = {'cppipe': open('./test.cppipe', 'rb'), 'images': open('./images.csv', 'rb')}

    # POST Request to /ctl with u as file1
    r = requests.post('http://www.controlcore.org:9090/run?out=outfolder', files=files)

if __name__ == '__main__':
    init()