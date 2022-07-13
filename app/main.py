from flask import Flask, request, send_from_directory, make_response, send_from_directory
from werkzeug.utils import secure_filename
from url_utils import get_base_url
from random import randint
from json import dumps
from db import db
import torch
import os

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
app = Flask(__name__)
base_url = get_base_url(port)

app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

model = torch.hub.load("ultralytics/yolov5", "custom",
                       path='best.pt', force_reload=True)


@app.route(f'{base_url}', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        file = request.files['file']
        print("*\nFile Name:", file.filename)
        split = secure_filename(file.filename).split('.')
        filename = f'{split[0]}_{randint(1000, 9999)}.{split[1]}'
        path = os.path.join('./static/uploads', filename)
        print(path)
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
            is_confident = False
            for percent in confidences:
                if percent > 0.6:
                    is_confident = True
                format_confidences.append(str(round(percent * 100)) + '%')
            if not is_confident:
                return make_response('', 300)

            labels = list(set(list(results.pandas().xyxy[0]['name'])))
            # labels: sorting and capitalizing, putting into function

            if not labels:
                return make_response('', 300)

            split = filename.split('.')

            ret = db[labels if type(labels) is str else labels[0]]
            ret.update(
                {'upload': f'images/{split[0]}.jpg', 'confidence': format_confidences[0]})

            res = make_response(dumps(ret), 200)
            res.headers['Content-Type'] = 'application/json'
            return res
        else:
            return make_response('', 300)
    else:
        with open(f'./static/home/home.html', 'r') as f:
            return make_response(f.read(), 200)


@app.route(f'{base_url}/images/<path>')
def images(path):
    return send_from_directory('./static/images', path)


@app.route(f'{base_url}/<path>')
def path_test(path):
    return send_from_directory('./static/home', path)


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc14.ai-camp.dev'
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
