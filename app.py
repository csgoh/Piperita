from flask import Flask, render_template, request

from processpiper.text2diagram import render
import base64
import io

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    diagram = None
    if request.method == "POST":
        text = request.form["text"]
        diagram = generate_diagram(text)
    return render_template("index.html", diagram=diagram)


def generate_diagram(text):
    _, img = render(text)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")


if __name__ == "__main__":
    app.run(debug=True)
