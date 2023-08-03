import requests
import logging
logging.basicConfig(level=logging.INFO)


def init():
    files = {'cppipe': open('./test.cppipe', 'rb'), 'images': open('./images.csv', 'rb')}
    s3filepath = 'Marklein/Microglia_Morphology_Project/Frozen_C20s/Plate_1/'
    filename = 'A1_-1_1_1_Stitched[GFP 469,525]_001.tif'
    outfilepath = '/hummingbird/' + s3filepath
    geturl = 'http://54.84.62.214/init?bucket=cmat-thrust1&s3filepath=' + s3filepath + '&filename=' + filename + '&outfilepath=' + outfilepath
    # POST Request to /ctl with u as file1
    r = requests.get(geturl)

    r = requests.post('http://54.84.62.214/run?out=outfolder', files=files)

if __name__ == '__main__':
    init()