import requests
import logging
logging.basicConfig(level=logging.INFO)


def init():
    files = {'cppipe': open('./test.cppipe', 'rb'), 'images': open('./images.csv', 'rb')}

    # POST Request to /ctl with u as file1
    r = requests.get('http://44.213.64.225//init?bucket=cmat-thrust1&filepath=Marklein/Microglia_Morphology_Project/Frozen_C20s/Plate_1,"A1_-1_1_1_Stitched[GFP 469,525]_001.tif')

    r = requests.post('http://44.213.64.225/run?out=outfolder', files=files)

if __name__ == '__main__':
    init()