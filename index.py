from flask import Flask, render_template
import os
import pandas
from settings import APP_STATIC
from ReadData import *

app = Flask(__name__)
data = []
x,y,z = [1],[1],[1]
data_path = "instances\\Normalized_data\\data_1_"
instances_num = None
@app.route("/")
def hello():
    global x,y,z
    return render_template("index.html",x = x,y = y,z = z,data = data)
@app.route("/index.html")
def index():
    return render_template("index.html",x = x,y = y,z = z,data = data)

@app.route("/charts.html")
def charts() :
    return render_template("charts.html")
@app.route("/tables.html")
def tables() :
    global data
    print(data,flush = True)
    return render_template("tables.html",data = data)
@app.route('/<num>')
def read_file(num) :
    global data,data_path,instances_num
    instances_num = num
    df = pandas.read_csv(os.path.join(APP_STATIC, data_path + num + ".csv"))
    data = [{} for i in range(len(df))]
    for i in range(len(df)) :
        data[i]["Index"] = i
        data[i]["Processing_Time"] = df["p"][i]
        data[i]["Release_Time"] = df["r"][i]
        data[i]["Pieces"] = df["w"][i]
        data[i]["Priority"] = df["v"][i]
        data[i]["Temperature"] = df["T"][i]
        data[i]["Duedate"] = df["d"][i]
    return render_template("index.html",x = x,y = y,z = z,data = data)
@app.route('/run')
def run() :
    global data_path,x,y,z,instances_num
    J = []
    print("Suss!",flush = True)
    ReadData(os.path.join(APP_STATIC, data_path + instances_num),J)
# #     ga = NSGA(100,5)
    return render_template("index.html",x = x,y = y,z = z,data = data)
#

if __name__ == "__main__" :
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(Debug = True)
