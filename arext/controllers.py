# Services to generate JSON for ARchi VR App Extensions

# Import flask dependencies
from flask import Flask
from flask import Blueprint, request, render_template, Response
import json, math, os

# Define the blueprint: 'arext', set its url prefix: app.url/arext
mod_arext = Blueprint('arext', __name__, url_prefix='/arext')
app = Flask(__name__)
app.register_blueprint(mod_arext)


# Set the route and accepted methods
# test routine to check server status
@app.route('/test', methods=['GET'])
def test():
    return Response("AR Extension Service is running.", status=201)

@app.route('/verified/', methods=['GET', 'POST'])
# Workflow extension sample: creates HTML page
def verified():
    response = {
        "id" : "com.verifiedspaces.claimdemo",
        "title" :  "Damage Claim",
        "orga" :  "Verified Spaces",
        "extensionId" : "com.verifiedspaces.workflow.claimdemo",
        "logoURL" : "https://YOUR_SERVER_ADDRESS/extension/vslogo.png",
        "validUntil" :  "2029-12-30"
    }
    docpath = '/data/www/ar/verifieddocs/'
    refs = {}
    if request.files.get("space"):
        jsonfile = request.files["space"]
        data = jsonfile.read()
        space = json.loads(data)
        datafilename = docpath + space['id'] + ".json"
        if os.path.exists(datafilename):
            os.remove(datafilename)
        jsonfile.stream.seek(0)
        jsonfile.save(datafilename)
        if request.files.get("svg"):
            svgfile = request.files["svg"]
            svgfilename = docpath + space['id'] + ".svg"
            if os.path.exists(svgfilename):
                os.remove(svgfilename)
            svgfile.save(svgfilename)
            refs['svg'] = space['id'] + ".svg"
        if request.files.get("web3D"):
            web3Dfile = request.files["web3D"]
            web3Dfilename = docpath + space['id'] + "3D.html"
            if os.path.exists(web3Dfilename):
                os.remove(web3Dfilename)
            web3Dfile.save(web3Dfilename)
            refs['web3D'] = space['id'] + "3D.html"
        if request.files.get("photo1"):
            photo1file = request.files["photo1"]
            photo1filename = docpath + space['id'] + "_1.jpeg"
            if os.path.exists(photo1filename):
                os.remove(photo1filename)
            photo1file.save(photo1filename)
            refs['photo1'] = space['id'] + "_1.jpeg"
        if request.files.get("photo2"):
            photo2file = request.files["photo2"]
            photo2filename = docpath + space['id'] + "_2.jpeg"
            if os.path.exists(photo2filename):
                os.remove(photo2filename)
            photo2file.save(photo2filename)
            refs['photo2'] = space['id'] + "_2.jpeg"
        html = render_template("claim.html", space = space, refs = refs)
        filename = docpath + space['id'] + ".html"
        if os.path.exists(filename):
            os.remove(filename)
        weburl = "https://YOUR_SERVER_ADDRESS/verifieddocs/" + space['id'] + ".html"
        htmlfile = open(filename, "w")
        htmlfile.write(html)
        htmlfile.close()
        response["webURL"] = weburl
    jsonResult = json.dumps(response)
    return Response(jsonResult, status=201, mimetype="application/json")

@mod_arext.route('/mecca/', methods=['GET', 'POST'])
# Service extension sample: creates an arrow that points towards Mecca
def mecca():
    if request.files.get("user"):
        file = request.files["user"]
        data = file.read()
        userloc = json.loads(data)
        #print(userloc)
        meccaLoc = (21.4224779, 39.8251832)
        usrLoc = (float(userloc['latitude']), float(userloc['longitude']))
        # flip to south dir for AR session ccoordinate system
        angle = str(calc_angle(usrLoc, meccaLoc) - 180.0)
        response = {}
        response["items"] = []
        response["items"].append({
            "id": "com.verifiedspaces.mecca",
            "type" : "Route",
            "subtype" : "Direction",
            "attributes" : "color:#F0E800;flat:1;",
            "vertices" : [
              [
                0.0,
                0.0,
                0.0
              ],
              [
                0.0,
                0.0,
                0.7
              ]
            ],
            "name" : "Mecca"
        })
        response["tasks"] = []
        response["tasks"].append({
            "do" : "add",
            "id": "net.metason.archi.mecca",
            "ahead" : "0.0 0.0 -0.75"
        })
        response["tasks"].append({
            "do" : "turn",
            "id" : "net.metason.archi.mecca",
            "to" : angle
        })
        jsonResult = json.dumps(response)
        return Response(jsonResult, status=201, mimetype="application/json")
    return panelResponse("Error im mecca()", "Oops. Not well gone.<br>JSON data missing.")

# --------------
# helper methods

# send error panel to AR app
def panelResponse(title, msg):
    errMsg = "<b>" + title + "</b><br>" + msg
    response = {}
    response["items"] = []
    response["items"].append({
        "id": "net.metason.archi.error",
	    "type" : "Spot",
        "subtype" : "Panel",
        "name" : "Error Panel",
        "vertices" : [
          [
            0.0,
            0.0,
            0.0
          ]
        ],
        "assetData" : errMsg,
	    "attributes" : "color:#FF4444; bgcolor:#333333DD; scale:1.0"
    })
    response["tasks"] = []
    response["tasks"].append({
	    "do" : "add",
        "id": "net.metason.archi.error",
	    "ahead" : "0.0 0.5 -1.0"
    })
    jsonResult = json.dumps(response)
    return Response(jsonResult, status=201, mimetype="application/json")

# calc angle in compass degrees between two lat/lon points versus north
def calc_angle(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])
    diffLong = math.radians(pointB[1] - pointA[1])
    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
    initial_bearing = math.degrees(math.atan2(x, y))
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing