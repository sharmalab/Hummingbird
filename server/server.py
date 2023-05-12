from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import logging
from flask import jsonify
import subprocess
import boto3
import os

TRIMMED_LOGS = False

# Logs in a preferred format.
if TRIMMED_LOGS:
    logging.basicConfig(level=logging.INFO, format='%(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

s3 = boto3.resource('s3')

@app.route('/')
def hello_world():
    return render_template('home.html')


# For example, http://localhost/init?bucket=bucketname&s3filepath=s3filepathinbucket&outfilepath=outfilepath
@app.route('/init', methods=['GET'])
def init():
    bucket = request.args.get('bucket')
    logging.info(bucket)
    s3filepath = request.args.get('s3filepath')
    logging.info(s3filepath)
    filename = request.args.get('filename')
    logging.info(filename)
    fulls3path = s3filepath + filename
    outfilepath = request.args.get('outfilepath')
    logging.info(outfilepath)
    s3 = boto3.client('s3')
    os.makedirs(outfilepath, mode=0o777, exist_ok=True)
    s3.download_file(bucket, fulls3path, outfilepath)

# For example, http://localhost/run?out=/path/where/the/output/goes&bucket=bucketname&filepath=filepathinbucket
@app.route('/run', methods=['POST'])
def run():
    cppipein = request.files['cppipe']
    images = request.files['images']
    cppipein.save(secure_filename(cppipein.filename))
    images.save(secure_filename(images.filename))
    out = request.args.get('out')

    logging.info("Input cppipe: %s, images: %s, Output: %s", cppipein, images, out)

    scr = "cellprofiler -c -r -p " + cppipein.filename + " -o " + out + " --data-file " + images.filename

    logging.info(scr)
    subprocess.call(scr, shell=True)
    resp = jsonify(success=True)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
