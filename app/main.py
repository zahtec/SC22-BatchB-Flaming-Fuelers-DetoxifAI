from flask import Flask, request, send_from_directory, make_response
from werkzeug.utils import secure_filename
from flask import send_from_directory
from json import dumps
from db import db
import torch
import os

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

model = torch.hub.load("ultralytics/yolov5", "custom",
                       path='best.pt', force_reload=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']


@app.route('/', methods=['POST'])
def post():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if file and allowed_file(file.filename):
        path = os.path.join('./static/uploads', filename)
        file.save(path)
        results = model(path, size=416)
        if len(results.pandas().xyxy) > 0:
            results.print()
            results.save(save_dir='./static/images')

            def and_syntax(alist):
                if len(alist) == 1:
                    alist = "".join(alist)
                    return alist
                elif len(alist) == 2:
                    alist = " and ".join(alist)
                    return alist
                elif len(alist) > 2:
                    alist[-1] = "and " + alist[-1]
                    alist = ", ".join(alist)
                    return alist
                else:
                    return

            confidences = list(results.pandas().xyxy[0]['confidence'])
            # confidences: rounding and changing to percent, putting in function
            format_confidences = []
            for percent in confidences:
                format_confidences.append(str(round(percent*100)) + '%')
            format_confidences = and_syntax(format_confidences)

            labels = list(results.pandas().xyxy[0]['name'])
            # labels: sorting and capitalizing, putting into function
            labels = set(labels)
            labels = and_syntax(labels)
            print(labels)
            res = make_response(dumps(db[labels].update(
                {'upload': f'images/{filename}', 'confidence': format_confidences})), 200)
            res.headers['Content-Type'] = 'application/json'
            return res
        else:
            return make_response('NotFound', 200)
    else:
        return make_response('Invalid file type or missing file', 400)


@app.route('/images/<path>')
def images(path):
    return send_from_directory('./static/images', path)


@app.route('/', methods=['GET'])
def home():
    return send_from_directory('./static', 'index.html')


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc14.ai-camp.dev'
    print(f'Try to open\n\n    https://{website_url}' + '\n\n')
    app.run(host='localhost', port=port, debug=True)
