from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# respond with "index.html" contents
@app.route("/")
def homehtml():
    return render_template("index.html")

# if "filename" exists respond with contents of "filename"
# else respond with 404 not found
#
# possibly simplify this by only serving one image?
#
@app.route("image/<filename>")
def route_image(filename):
    return render_template(filename)

# respond with "style.css" contents
@app.route("style.css")
def route_css():
    pass

# respond with "index.js" contents
@app.route("index.js")
def route_js():
    pass
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)