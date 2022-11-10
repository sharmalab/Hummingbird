from flask import Flask, request
import subprocess
import logging
from flask import jsonify
from werkzeug.utils import secure_filename

TRIMMED_LOGS = False

# Logs in a preferred format.
if TRIMMED_LOGS:
    logging.basicConfig(level=logging.INFO, format='%(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# For example, http://localhost:8090/?out=/path/where/the/output/goes
@app.route('/', methods=['POST'])
def init():
    cppipein = request.files['in']
    cppipein.save(secure_filename(cppipein.filename))
    out = request.args.get('out')
    logging.info("Input cppipe: %s , Output: %s", cppipein, out)
    scr = "cellprofiler -c -r -p" + cppipein.filename + "-o" + out
    subprocess.call(scr, shell=True)
    resp = jsonify(success=True)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
