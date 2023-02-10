from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import logging
from flask import jsonify
import subprocess
import boto3
import s3fs

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


# For example, http://localhost/init?bucket=bucketname&filepath=filepathinbucket
@app.route('/init', methods=['GET'])
def init():
    bucket = request.args.get('bucket')
    filepath = request.args.get('filepath')

    # read dataframe
    s3 = boto3.client('s3')
    tags = s3.head_object(Bucket=bucket, Key=filepath)
    print(tags['ResponseMetadata']['HTTPHeaders']['etag'])
    s3.download_file(bucket, filepath, filepath)

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
