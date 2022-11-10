import requests
import logging
logging.basicConfig(level=logging.INFO)


def init():
    files = {'file1': open('./test.cppipe', 'rb')}

    # POST Request to /ctl with u as file1
    r = requests.post('http://localhost:9090/run?out=outfolder', files=files)

if __name__ == '__main__':
    init()