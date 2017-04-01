from flask import render_template, request
from .youdown import downloadWorker
from . import app


def download_helper(link, email):
    helper = downloadWorker(link, email)
    helper.start()


@app.route('/')
def front():
    return render_template("index.html")


@app.route('/download', methods=['GET', 'POST'])
def downpage():
    if request.method == 'POST':
        link = request.form['link']
        email = request.form['email']
        download_helper(link, email)
        return render_template("download.html",
                               link=link,
                               email=email)
    else:
        return "How'd you get here? You might want to go back"
