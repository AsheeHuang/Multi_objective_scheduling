from Job import JOB
import pandas

# weight = [0.2,0.2,0.5,0.1]
def ReadData(path, J ):
    Read = open(path + ".csv", 'r')
    R2 = open(path + '_Mj.csv')
    R3 = open(path + '_Normal.csv')
    df = pandas.read_csv(path + ".csv")
    des = df.describe()
    # print()
    MIN_MAX = [[float('inf'), 0] for i in range(5)]
    Read.readline()
    i = 0
    k = 0
    for line in R3.readlines():
        line = line.strip().split(',')
        MIN_MAX[k][0] = float(line[0])
        MIN_MAX[k][1] = float(line[1])
        k += 1
    for line in Read.readlines():
        line = line.strip().split(',')
        j = JOB()
        j.index = i
        i += 1
        j.processing_time = int(line[0])
        j.release_date = int(line[1])
        j.pieces = int(line[2])
        j.weight = int(line[3])
        j.Temperature = int(line[4])
        j.due_date = int(float(line[5]))
        j.WP = j.pieces * j.weight / j.processing_time

        j.processing_time_n = (j.processing_time - des['p']["min"]) / (des['p']["max"] - des['p']["min"])
        j.pieces_n = (j.pieces - des['w']["min"]) / (des['w']["max"] - des['w']["min"])
        j.weight_n = (j.weight - des['v']["min"]) / (des['v']["max"] - des['v']["min"])
        j.due_date_n = (j.due_date - des['d']["min"]) / (des['d']["max"] - des['d']["min"])
        j.release_date_n = (j.release_date - des['r']["min"]) / (des['r']["max"] - des['r']["min"])



        J.append(j)
    # print(path)
    index = 0
    for line in R2.readlines():
        line = line.strip().split(',')
        for item in line:
            if item != '':
                J[index].Mj.append(int(item))
                J[index].Mj_n = (len(J[index].Mj) - MIN_MAX[3][0]) / (MIN_MAX[3][1] - MIN_MAX[3][0])
        #less priority is better
        # J[index].priority = cal_priority(J[index].processing_time_n, J[index].pieces_n , J[index].weight_n, J[index].Mj_n, weight)
        # print(J[index].processing_time_n, J[index].pieces_n, J[index].weight_n, J[index].Mj_n, len(J[index].Mj))
        # print(MIN_MAX[3][0],MIN_MAX[3][1])
        index += 1


# def cal_priority(p,w,v,m, weight) :
#     #less priority is better
#     #we want shorter processing time
#     #more piece
#     #more weight
#     #less flexible
#     return  p * weight[0] - w * weight[1] - v * weight[2] + m * weight[3]