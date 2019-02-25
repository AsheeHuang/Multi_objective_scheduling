from flask import Flask, render_template
import os
import pandas
from settings import APP_STATIC
from ReadData import *
from NSGA import *

app = Flask(__name__)
data = []
x,y,z = [1],[1],[1]
color = []
data_path = "instances\\Normalized_data\\data_1_"
instances_num = None
@app.route("/")
def hello():
    global x,y,z
    return render_template("index.html",x = x,y = y,z = z, data = {})
@app.route("/index.html")
def index():
    return render_template("index.html",x = x,y = y,z = z,data = {})

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
    return render_template("index.html",x = x,y = y,z = z)
@app.route('/run')
def run() :
    global data_path,x,y,z,instances_num
    J = []
    ReadData(os.path.join(APP_STATIC, data_path + str(instances_num)),J)
    ga = NSGA(1000,0,J)
    ga.run()
    pareto = ga.nondominated_sort()[0] + ga.nondominated_sort()[1] + ga.nondominated_sort()[2]

    result = {}
    input = [[] for _ in range(2)]
    output = [[]]
    weight = []
    for point in pareto :
        input[0].append(point.obj[0])#weighted tardiness
        input[1].append(point.obj[1])#total_flow_time
        output[0].append(point.obj[2])#pieces
        weight.append(point.weights)
    res = (DEA_analysis(input, output))
    eff = [r['Efficiency'] for r in res]
    result["weight"] = weight
    result["Flow_time"] = input[1]
    result["Tardiness"] = input[0]
    result["Piece"] = output[0]
    result["DEA_score"] = eff
    return render_template("index.html",x = result["Tardiness"],y = result["Flow_time"],z = result["Piece"],color = result["DEA_score"],result = result)
#

if __name__ == "__main__" :
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(Debug = True)
