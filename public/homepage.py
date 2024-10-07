from flask import Flask, redirect, url_for, render_template

app = Flask("__main__")

@app.route("/")
def homehtml():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()