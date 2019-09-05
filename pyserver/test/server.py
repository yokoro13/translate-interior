from flask import Flask, request, make_response
from PIL import Image, ImageOps
import io
from trans_interior import TransInterior
import time
import numpy as np

app = Flask(__name__)


@app.route("/", methods=["GET"])
def do_get():
    print("GEt")
    return "Hey!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


@app.route("/", methods=["POST"])
def do_post():
    if request.method == "POST":
        start = time.time()

        image_bytes = request.files["post_data"]    # flask.request.data
        data = image_bytes.read()
        image_bytes = request.files["post_label"]  # flask.request.data

        label = image_bytes.read().decode("ascii")
        label = label.split(" ")
        label = label[:len(label)-1]
        translation.set_target_labels(label)

        image = Image.open(io.BytesIO(data))

        image = ImageOps.flip(image)

        # 処理
        image = translation.trans_interior(image)
        # image = translation.do_segme ntation(image)
        # image = translation.do_translation(image, "white_floor")

        image = ImageOps.flip(image)
        buf = io.BytesIO()

        image.save(buf, "JPEG")

        print("serer: {}".format(time.time() - start))
        response = make_response(buf.getvalue())
        response.headers["Content-type"] = "Image"

        return response


if __name__ == '__main__':
    translation = TransInterior()
    c_trg = [1, 0, 0, 0, 0, 0]
    translation.set_target_labels([0])
    labels = ["black_floor", "red_brick_wall", "white_floor", "white_wall", "wood_floor", "wood_wall"]
    app.debug = True
    app.run()