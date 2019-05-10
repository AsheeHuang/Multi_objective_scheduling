from flask import Flask, render_template, request
import os
import pandas
from settings import APP_STATIC
from ReadData import *
from NSGA import *
from DEA import DEA_analysis

app = Flask(__name__)
data = []
x,y,z = [1],[1],[1]
color = []
result = {}
problem_set, instance_num = None, None
data_path = "instances\\Exp_data2\\data_"
@app.route("/")
def hello():
    global result
    return render_template("index.html",result = result, data = {})
@app.route("/index.html")
def index():
    global result
    return render_template("index.html",result = result,data = {})

@app.route("/charts.html")
def charts() :
    return render_template("charts.html")
@app.route("/tables.html")
def tables() :
    data = read_file()
    return render_template("tables.html",data = data)

def read_file() :
    global data,data_path,problem_set, instance_num
    df = pandas.read_csv(os.path.join(APP_STATIC, data_path + str(problem_set) + "_"+str(instance_num)+".csv"))
    data = [{} for i in range(len(df))]
    for i in range(len(df)) :
        data[i]["Index"] = i
        data[i]["Processing_Time"] = df["p"][i]
        data[i]["Release_Time"] = df["r"][i]
        data[i]["Pieces"] = df["w"][i]
        data[i]["Priority"] = df["v"][i]
        data[i]["Temperature"] = df["T"][i]
        data[i]["Duedate"] = df["d"][i]
    return data

@app.route('/run', methods=['POST','GET'])
def run() :
    global data_path, problem_set, instance_num
    if request.method == 'POST':
        print(request.form, flush=True)
        return
    else:
        instance = request.args.get('instance')
        if instance == "" :
            return render_template("index.html",x = x,y = y,z = z)
    J = []
    problem_set = instance[:1]
    instance_num = instance[1:]
    ReadData(os.path.join(APP_STATIC, data_path + problem_set + "_"+instance_num),J)
    ga = NSGA(500,3,Job_set = J,common_due_date=120)
    ga.run()
    pareto = [item for sublist in ga.nondominated_sort() for item in sublist]
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
    return render_template("index.html",result = result)
#

if __name__ == "__main__" :
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.debug = True
    app.run(Debug = True)
