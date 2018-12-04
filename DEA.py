from gurobipy import *

def DEA_analysis(input,output) :
    n = len(output)
    m = len(input)
    R = len(input[0])


    res = [{"Efficiency" : None ,'u' : [], 'v' : []} for i in range(R)]

    for k in range(R) :

        model = Model()
        model.setParam('OutputFlag', False)

        u = model.addVars(n, vtype=GRB.CONTINUOUS, name='u')
        v = model.addVars(m, vtype=GRB.CONTINUOUS, name='v')

        obj = LinExpr()


        for j in range(n) :
            obj += u[j] * output[j][k]
        model.setObjective(obj,GRB.MAXIMIZE)


        #set constrants
        c1 = LinExpr()
        for i in range(m) :
            c1 += v[i] * input[i][k]
        model.addConstr(c1 == 1, name = 'c1')


        for r in range(R) :
            c2 = LinExpr()
            for j in range(n) :

                c2 += u[j] * output[j][r]
            for i in range(m) :
                c2 -= v[i] * input[i][r]
            model.addConstr(c2 <= 0, name = 'c2')

        model.optimize()

        res[k]['Efficiency'] = model.objVal
        for i in range(n) :
            res[k]['u'].append(u[i].x)
        for j in range(m) :
            res[k]['v'].append(v[j].x)
    return res




if __name__ == "__main__" :
    input = [[1,2,4,6,9,5,4,10,8]]
    output = [[1,4,6,7,8,3,1,7,4]]

    res = (DEA_analysis(input,output))
    for r in res :
        print(r)

