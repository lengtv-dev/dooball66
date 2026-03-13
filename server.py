from flask import Flask,request,Response
import requests

app = Flask(__name__)

@app.route("/proxy")
def proxy():

    url=request.args.get("url")

    r=requests.get(url,stream=True)

    return Response(
        r.iter_content(1024),
        content_type=r.headers.get("content-type")
    )

@app.route("/m3u")
def m3u():

    return open("playlist.m3u").read()

@app.route("/json")
def json_playlist():

    return open("playlist.json").read()

app.run(host="0.0.0.0",port=8000)