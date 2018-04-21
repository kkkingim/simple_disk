# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import make_response
from flask import request
import os
import random
import json

app = Flask(__name__)
rootdir = ''
app.secret_key = 'dfbufhnweiknxviowenflxcknalsdnasdasc'

def colorfulfont(s):
    l = [i for i in "1234567890ABCDEF"]
    return "".join(["<font style='color:#" + random.choice(l) + random.choice(l) + random.choice(l) + "'>"+ i +"</font>" for i in s])

def colorfulstring(s):
    l = [i for i in "1234567890ABCDEF"]
    color = '#' + "".join([random.choice(l)for x in range(6) ])
    return "<font style='color:%s'>%s</font>" % (color, s)


def getfiletext(ddd):
    if not os.path.exists(rootdir + ddd):
        l = [s for s in "1234567890ABCDEF"]
        return "<h1>" + "".join(["<font style='color:#" + random.choice(l) + random.choice(l) + random.choice(l) + "'>"+ i +"</a>" for i in "Path Not Exists"])  + "</h1>"

    for p, d, f in os.walk(rootdir + ddd):
        if ddd == "":
            con = '<h2 style="color:#009900">/</h2>'
        else:
            dsp = ddd.split("/")[1:]
            s = "<a href='?'>HOME</a>"
            i = 1
            for ss in dsp:
                pth = ""
                for x in range(i):
                    pth += "/" + dsp[x]
                i += 1
                s += "/<a style='color:#090;text-decoration:underline;' href='%s'>%s</a>" % ("?p=" + pth, ss)

            con = '<h2 style="color:#009900">%s</h2>' % (s)

        con += '</br>' +colorfulfont( '-' * 10 + 'DIRS-' + '-' * 10) + '</br>'
        for fname in d:
            if fname[0] == '.':
                continue
            try:
                fname = fname.decode('utf-8', 'ignore')
            except:
                pass
            pa = ddd + '/' + fname
            con += '<li><input type="checkbox" name="delitem" value="%s" style="margin: 0px 10px;"><a href="?p=%s">%s</a></li>' % (pa, pa, colorfulstring(fname))
        con += '</br>' +colorfulfont( '-' * 10 + 'FILES' + '-' * 10 )+ '</br>'
        for fname in f:
            if fname[0] == '.':
                continue
            try:
                fname = fname.decode('utf-8', 'ignore')
            except:
                pass
            con += '<li><input type="checkbox" name="delitem" value="%s" style="margin: 0px 10px;"><a href="?p=%s&f=%s">%s</a></li>' % (ddd + os.path.sep + fname, ddd, fname, colorfulstring(fname))
        return con

@app.route('/disk')
def disk():
    f = request.values.get("f","")
    p = request.values.get("p","")

    if '..' in p:
        con = getfiletext("Error")
        resp = make_response(render_template('index.html', cc=con, di="Error"))
        return resp
    #is file
    if f != "" and p != "":
        ddd = rootdir + p + os.path.sep + f
        if os.path.isfile(ddd):
            return send_from_directory(rootdir + p,f,as_attachment=True)
    # is path
    if f == "" and p != "":
        con = getfiletext(p)
        resp = make_response(render_template('index.html', cc=con, di=p))
        return resp

    con = getfiletext("")
    resp = make_response(render_template('index.html', cc=con, di="/"))
    return resp

@app.route('/diskact', methods=["POST"])
def diskact():
    delitems = request.values.get("delitem","")
    if delitems != "":
        delitems = json.loads(delitems)
        for p in delitems:
            p = rootdir + p
            if os.path.exists(p):
                if os.path.isdir(p):
                    os.rmdir(p)
                else:
                    os.remove(p)
                print "del: "+ p
        ed = delitems[0].rfind("/")
        upp = delitems[0][:ed]
        return getfiletext(upp)
    return "error"

@app.route("/diskupload", methods=["POST"])
def diskupload():
    uf = request.files['file']
    p = request.values.get("p","")
    if uf:
        uf.save(rootdir + p + os.path.sep + uf.filename)
        return "Upload Successed"


if __name__ == '__main__':
    rootdir = './disk'
    app.run(debug=True, host='0.0.0.0')
