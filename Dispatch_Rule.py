import copy
from Machine import *
from heapq import *
from random import random

def Machine_Oriented(J,d ,weight = None, machine_rule =  lambda x : x.load ) :
    def normalize_transfer_time (transfer_time) :
        return (transfer_time - 0) / (15 - 0)

    machines = Machines(J)
    Pieces_Produced, count = 0,0
    weighted_tatal_lateness = 0
    total_flow_time = 0
    #job_assigned = [False for _ in range(len(J))] #initially unassigned
    while not machines.reach_deadline() : #does not reach deadline
        sel_m = machines.select_machine(machine_rule)
        if sel_m.avail == False : #no available machine
            break
        """"""
        job_rule = lambda x: x.processing_time_n * weight[0] - x.pieces_n * weight[1] - x.weight_n * weight[2] + x.due_date_n * weight[3] + x.release_date_n * weight[4] + normalize_transfer_time(x.transfer_time(sel_m.Temperature)) * weight[5] /2
        """"""
        sel_job = sel_m.select_job(job_rule)
        if sel_job : #there is an available job
            insert_success = sel_m.assign_job(sel_job,d)
            if insert_success :#if insert int this job does not reach deadline
                Pieces_Produced += sel_job.pieces
                weighted_tatal_lateness += max(0,sel_m.load - sel_job.due_date) * sel_job.weight
                total_flow_time += (sel_job.starting_time + sel_job.processing_time) - sel_job.release_date
                count += 1
                # print("sel job :", sel_job , " to " , sel_m.index, " load : ",sel_m.load, sel_m.avail)
    for j in J :
        if j.is_processed == False :
            total_flow_time += max(0,d - j.release_date)

    return weighted_tatal_lateness ,Pieces_Produced ,total_flow_time / len(J) , count
def prob_model(J,d, machine_rule =  lambda x : x.load ,prob = None ) :
    def normalize_transfer_time (transfer_time) :
        return (transfer_time - 0) / (15 - 0)

    machines = Machines(J)
    Pieces_Produced, count = 0,0
    prefix_prob = []
    prefix_prob.append(prob[0])
    for i in range(1,len(prob)) :
        prefix_prob.append(prefix_prob[i-1] + prob[i])
    # print(prefix_prob)
    #job_assigned = [False for _ in range(len(J))] #initially unassigned
    while not machines.reach_deadline() : #does not reach deadline
        sel_m = machines.select_machine(machine_rule)
        if sel_m.avail == False : #no available machine
            break
        """"""
        job_rule = None

        rand_num = random()
        if  0 <= rand_num < prob[0] :
            job_rule = lambda x : x.processing_time_n
        elif prob[0] <= rand_num < prob[1]:
            job_rule = lambda x : x.pieces_n
        elif prob[1] <= rand_num < prob[2] :
            job_rule = lambda x : x.weight_n
        else :
            job_rule = lambda x : normalize_transfer_time(x.transfer_time(sel_m.Temperature))
        """"""
        sel_job = sel_m.select_job(job_rule)
        if sel_job : #there is an available job
            insert_success = sel_m.assign_job(sel_job,d)
            if insert_success :#if insert int this job does not reach deadline
                Pieces_Produced += sel_job.pieces * math.sqrt(sel_job.weight)
                count += 1
                # print("sel job :", sel_job , " to " , sel_m.index, " load : ",sel_m.load, sel_m.avail)

    return Pieces_Produced / 25, count



def reach_deadline(MA):
    for i in MA:
        if i:
            return False
    return True

def Check_All_Done(Ji, J):
    for item in Ji:
        if J[item].is_processed == False:
            return False
    return True

def WP(J, d):
    J = sorted(J, key=lambda l: l.WP, reverse=True)
    Ji = [[] for i in range(26)]
    for k, j in enumerate(J):
        for i in j.Mj:
            Ji[i].append(k)
    print(Ji)
    Pieces_Produced = 0
    count = 0
    Machine_Avail = [True for i in range(26)]
    Machine_Avail.insert(0, False)
    Machine_Load = [[i, 0] for i in range(0, 26)]
    Machine_T = [100 for i in range(26)]
    BUILD_HEAP(Machine_Load)
    while len(Machine_Load) > 1:
        max = -1
        max_index = 0
        for j in Ji[Machine_Load[1][0]]:
            if not J[j].is_processed and J[j].WP > max:
                max = J[j].WP
                max_index = j

        if max != -1:
            J[max_index].is_processed = True
            setup = 5 + abs(Machine_T[Machine_Load[1][0]] - J[max_index].Temperature) * (0.1)
            setup = int(math.ceil(setup))
            Machine_T[Machine_Load[1][0]] = J[max_index].Temperature
            if Machine_Load[1][1] > J[max_index].release_date:
                ''''''
                if J[max_index].release_date>Machine_Load[1][1]:
                    Machine_Load[1][1]=J[max_index].release_date
                # Machine_Load[1][1] = max(J[max_index].release_date, int(Machine_Load[1][1]))
                # print(type(Machine_Load[1][1]))
                # print(type(J[max_index].release_date))
                ''''''
                Machine_Load[1][1] += setup + J[max_index].processing_time
            else:
                Machine_Load[1][1] = J[max_index].release_date + setup + J[max_index].processing_time
            J[max_index].Machine_Assigned = Machine_Load[1][0]
            J[max_index].starting_time = Machine_Load[1][1] - J[max_index].processing_time

            if J[max_index].starting_time + J[max_index].processing_time <= d:
                Pieces_Produced += J[max_index].pieces
                count += 1
            if Check_All_Done(Ji[Machine_Load[1][0]], J) or Machine_Load[1][1] >= d:
                del Machine_Load[1]
        else:
            del Machine_Load[1]
        BUILD_HEAP(Machine_Load)
    return Pieces_Produced/25, count

def FCFS(J, d):
    J = sorted(J, key=lambda l: l.release_date, reverse=False)
    Pieces_Produced = 0
    print()
    Machine_Avail = [True for i in range(25)]
    Machine_Avail.insert(0, False)
    Machine_Load = [0 for i in range(26)]
    ''''''
    Machine_T = [100 for i in range(26)]
    ''''''
    count = 0
    for k, j in enumerate(J):
        if reach_deadline(Machine_Avail):
            break
        min_machine_index = j.Mj[0]
        min_machine_load = Machine_Load[j.Mj[0]]
        for i in j.Mj:
            if Machine_Load[i] < min_machine_load and Machine_Avail[i] == True:
                min_machine_index = i
                min_machine_load = Machine_Load[i]
        j.Machine_Assigned = min_machine_index
        setup = 5 + abs(Machine_T[min_machine_index] - j.Temperature) * (0.1)
        setup = int(math.ceil(setup))
        Machine_T[min_machine_index] = j.Temperature
        ''''''
        Machine_Load[min_machine_index]=max(j.release_date,Machine_Load[min_machine_index])
        ''''''
        Machine_Load[min_machine_index] += setup + j.processing_time
        j.starting_time = Machine_Load[min_machine_index] - j.processing_time

        if Machine_Load[min_machine_index] >= d:
            Machine_Avail[min_machine_index] = False
        if j.starting_time + j.processing_time <= d:
            Pieces_Produced += j.pieces
            count += 1
    return Pieces_Produced / 25, count

def LFJFM(J, d):
    #J is Job_list with attribute
    J = sorted(J, key=lambda l: l.release_date, reverse=False)
    # print(len(J))
    #init
    t=0
    type(t)
    print("front",d)
    newt=0
    count=0
    count_on_time_job=0
    Pieces_Produced = 0
    Machine_Avail = [True for i in range(25)]
    Machine_Avail.insert(0, False)
    Machine_Load = [0 for i in range(26)]
    Machine_T = [100 for i in range(26)]
    # released_Job=[]

    #step 2 loop until all job scheduled

    while(len(J)>count and is_still_Avail(Machine_Load,d)):
        #step 2 check if any r_j < t


        # print("front of while ",t)
        if released_job_in_NS(J, t)==False:
        #step 3 t = min r_j
            t=find_min_r_j(J, t)
            # print("J[count].release_date ",t)
        #find LFJ
        min_Flexible_job_index=0
        # min_len_Mj=J[0].Mj

        #step 4 choose LFJ
        for k, j in enumerate(J):
            if J[min_Flexible_job_index].is_processed:
                min_Flexible_job_index=k
                continue

            if j.release_date<=t and count_LFJ_value(J[min_Flexible_job_index].Mj,Machine_Avail)<=count_LFJ_value(j.Mj,Machine_Avail) :
                if count_LFJ_value(J[min_Flexible_job_index].Mj,Machine_Avail)==count_LFJ_value(j.Mj,Machine_Avail) and J[min_Flexible_job_index].release_date<j.release_date:
                    min_Flexible_job_index = k
                else:
                    min_Flexible_job_index = k
        # print("r_j ",J[min_Flexible_job_index].release_date)
        #step 5 choose idle LFM
        idle_M=-1
        choosed_M=-1
        for k, i in enumerate(J[min_Flexible_job_index].Mj):
            if idle_M==-1 and  Machine_Load[i]<=t  :#Machine_Avail[i]
                idle_M=1
                choosed_M=i

            elif idle_M==1 and Machine_Load[i]<=t and count_LFM_value(J, d, i)<count_LFM_value(J, d, choosed_M):
                choosed_M=i
        #step 6 check and set time
        if idle_M==-1:
            newt=min_M_Load(Machine_Load,J[min_Flexible_job_index])
            t= newt
            continue
        else:
            ''''''
            J[min_Flexible_job_index].Machine_Assigned = choosed_M
            setup = 5 + abs(Machine_T[choosed_M] - J[min_Flexible_job_index].Temperature) * (0.1)
            setup=int(math.ceil(setup) )
            Machine_T[choosed_M] = J[min_Flexible_job_index].Temperature
            Machine_Load[choosed_M] += setup + J[min_Flexible_job_index].processing_time
            J[min_Flexible_job_index].starting_time = Machine_Load[choosed_M] - J[min_Flexible_job_index].processing_time

            if J[min_Flexible_job_index].starting_time + J[min_Flexible_job_index].processing_time <= d:
                Pieces_Produced += J[min_Flexible_job_index].pieces
            J[min_Flexible_job_index].is_processed = True
            count_on_time_job += 1
            ''''''
            Machine_Load[choosed_M]=J[min_Flexible_job_index].processing_time+max(t,Machine_Load[choosed_M])
            newt=min(Machine_Load[1:])
            # print(Machine_Load[1:])
            t=max(t,newt)
            count += 1



            ''''''

            ''''''

            # count += 1
            # print(count)

    print("back", d)
    return Pieces_Produced/25, count

def LFJ_FastM(J, d):
    #J is Job_list with attribute
    J = sorted(J, key=lambda l: l.release_date, reverse=False)
    # print(len(J))
    #init
    t=0
    type(t)
    print("front",d)
    newt=0
    count=0
    count_on_time_job=0
    Pieces_Produced = 0
    Machine_Avail = [True for i in range(25)]
    Machine_Avail.insert(0, False)
    Machine_Load = [0 for i in range(26)]
    Machine_T = [100 for i in range(26)]
    # released_Job=[]

    #step 2 loop until all job scheduled

    while(len(J)>count and is_still_Avail(Machine_Load,d)):
        #step 2 check if any r_j < t


        # print("front of while ",t)
        if released_job_in_NS(J, t)==False:
        #step 3 t = min r_j
            t=find_min_r_j(J, t)
            # print("J[count].release_date ",t)
        #find LFJ
        min_Flexible_job_index=0
        # min_len_Mj=J[0].Mj

        #step 4 choose LFJ
        for k, j in enumerate(J):
            if J[min_Flexible_job_index].is_processed:
                min_Flexible_job_index=k
                continue

            if j.release_date<=t and count_LFJ_value(J[min_Flexible_job_index].Mj,Machine_Avail)<=count_LFJ_value(j.Mj,Machine_Avail) :
                if count_LFJ_value(J[min_Flexible_job_index].Mj,Machine_Avail)==count_LFJ_value(j.Mj,Machine_Avail) and J[min_Flexible_job_index].release_date<j.release_date:
                    min_Flexible_job_index = k
                else:
                    min_Flexible_job_index = k
        # print("r_j ",J[min_Flexible_job_index].release_date)
        #step 5 choose idle LFM
        idle_M=-1
        choosed_M=-1
        for k, i in enumerate(J[min_Flexible_job_index].Mj):
            if idle_M==-1 and  Machine_Load[i]<=t  :#Machine_Avail[i]
                idle_M=1
                choosed_M=i

            elif idle_M==1 and Machine_Load[i]<=t and Machine_Load[i]<Machine_Load[choosed_M]:
                choosed_M=i
        #step 6 check and set time
        if idle_M==-1:
            newt=min_M_Load(Machine_Load,J[min_Flexible_job_index])
            t= newt
            continue
        else:
            ''''''
            J[min_Flexible_job_index].Machine_Assigned = choosed_M
            setup = 5 + abs(Machine_T[choosed_M] - J[min_Flexible_job_index].Temperature) * (0.1)
            setup=int(math.ceil(setup) )
            Machine_T[choosed_M] = J[min_Flexible_job_index].Temperature
            Machine_Load[choosed_M] += setup + J[min_Flexible_job_index].processing_time
            J[min_Flexible_job_index].starting_time = Machine_Load[choosed_M] - J[min_Flexible_job_index].processing_time

            if J[min_Flexible_job_index].starting_time + J[min_Flexible_job_index].processing_time <= d:
                Pieces_Produced += J[min_Flexible_job_index].pieces
            J[min_Flexible_job_index].is_processed = True
            count_on_time_job += 1
            ''''''
            Machine_Load[choosed_M]=J[min_Flexible_job_index].processing_time+max(t,Machine_Load[choosed_M])
            newt=min(Machine_Load[1:])
            # print(Machine_Load[1:])
            t=max(t,newt)
            count += 1



            ''''''

            ''''''

            # count += 1
            # print(count)

    print("back", d)
    return Pieces_Produced/25, count

def NEH(J, d):
    #J is Job_list with attribute
    J = sorted(J, key=lambda l: l.release_date, reverse=False)
    U=copy.deepcopy(J)
    L=[]

    # print(len(J))
    while len(U)!=0:
        # print("len L,",len(L))
        print("len U,", len(U))

        bestObjValue=0
        TargetJob=U.pop(0)
        for j in range(len(L),-1,-1):
            # print("j= ",j)
            candidateSequence=copy.copy(L)
            # print("C1=",len(candidateSequence))
            candidateSequence.insert(j,copy.deepcopy(TargetJob))
            # print("C2=", len(candidateSequence))
            ObjValue=NEH_Objective(candidateSequence,d)
            if ObjValue>bestObjValue:
                bestObjValue=ObjValue
                L_temp=copy.copy(candidateSequence)

        L=copy.deepcopy(L_temp)
    for i ,j in enumerate(L):
        j.Machine_Assigned = 0
        j.starting_time = 0
        j.is_processed = False
    ObjValue = NEH_Objective(L, d)
    # J=copy.deepcopy(L)
    # J=L
    count=len(J)
    return NEH_Objective(L,d),count,L

def NEH_Objective(J, d):
    # for i, j in enumerate(J):
    #     j.is_processed=False
    #     j.Machine_Assigned=0

    t = 0
    type(t)
    # print("front", d)
    newt = 0
    count = 0
    count_on_time_job = 0
    Pieces_Produced = 0
    Machine_Avail = [True for i in range(25)]
    Machine_Avail.insert(0, False)
    Machine_Load = [0 for i in range(26)]
    Machine_T = [100 for i in range(26)]
    # released_Job=[]
    job_index=0
    while job_index<len(J):
        # if J[job_index].release_date>t:
        #     t=J[job_index].release_date

        choosed_M = J[job_index].Mj[0]
        for k, i in enumerate(J[job_index].Mj):

            if   Machine_Load[i] < Machine_Load[choosed_M]:
                choosed_M = i
        # step 6 check and set time
        # if idle_M == -1:
        #     newt = min_M_Load(Machine_Load, J[job_index])
        #     t = newt
        #     continue
        # else:
        #     ''''''
        J[job_index].Machine_Assigned = choosed_M
        setup = 5 + abs(Machine_T[choosed_M] - J[job_index].Temperature) * (0.1)
        setup = int(math.ceil(setup))
        Machine_T[choosed_M] = J[job_index].Temperature

        Machine_Load[choosed_M] =max(J[job_index].release_date, Machine_Load[choosed_M])
        Machine_Load[choosed_M] += setup + J[job_index].processing_time
        J[job_index].starting_time = Machine_Load[choosed_M] - J[job_index].processing_time

        if J[job_index].starting_time + J[job_index].processing_time <= d:
            Pieces_Produced += J[job_index].pieces
        J[job_index].is_processed = True
        count_on_time_job += 1
        ''''''
        # Machine_Load[choosed_M] = J[job_index].processing_time + max(J[job_index].release_date, Machine_Load[choosed_M])
        # newt = min(Machine_Load[1:])
        # print(Machine_Load[1:])
        # t = max(t, newt)
        job_index += 1
    return Pieces_Produced / 25

def SPT(J,d) :
    J = sorted(J, key=lambda l: l.release_date, reverse=False)
    J_copy = copy.copy(J)
    Pieces_Produced = 0
    count = 0 #job count
    Machine_Avail = [True for _ in range(25)]
    Machine_Avail.insert(0, False) #do not use machine_load[0]
    Machine_Load = [0 for _ in range(26)] #init machine load
    Machine_T = [100 for _ in range(26)] #init machine temperature
    min_heap = [] #min heap of processing time

    """init the min heap of processing time"""
    while J_copy :
        j = J_copy.pop(0)
        if j.release_date == 0 :
            heapq.heappush(min_heap,(j.processing_time ,j.index))
        else :
            break
    if not min_heap :
        j = J_copy.pop(0)
        heapq.heappush(min_heap,(j.processing_time ,j.index))

    """Main loop"""
    while min_heap :
        if reach_deadline(Machine_Avail) :
            break

        #print(min_heap)
        j = J[heapq.heappop(min_heap)[1]]
        # print(j.index)
        setup = int(math.ceil(5 + abs(Machine_T[j.Mj[0]] - j.Temperature) * (0.1)))
        min_machine_index = j.Mj[0]
        min_machine_load = Machine_Load[j.Mj[0]] + setup
        for i in j.Mj[1:] : #loop through machines that can run job j
            setup = int(math.ceil(5 + abs(Machine_T[i] - j.Temperature) * (0.1)))  # setup time
            if Machine_Load[i] + setup < min_machine_load and Machine_Avail[i] == True : #find least loading machine
                min_machine_index = i
                min_machine_load = Machine_Load[i]
        j.Machine_Assigned = min_machine_index
        setup = int(math.ceil(5 + abs(Machine_T[min_machine_index] - j.Temperature) * (0.1)))  # setup time
        Machine_T[min_machine_index] = j.Temperature #assing new temperature
        #update machine load and starting time
        Machine_Load[min_machine_index] = max(j.release_date,Machine_Load[min_machine_index])
        Machine_Load[min_machine_index] += setup + j.processing_time
        j.starting_time = Machine_Load[min_machine_index] - j.processing_time
        # for j in J_copy :
        #     print(j.release_date)
        """if job release, add to min heap"""
        counter = 0
        while len(J_copy) > 1  :
            job = J_copy[counter]
            r = job.release_date
            push = False #boolean variable : if push or not
            for i in job.Mj :
                if Machine_Load[i] >= r :
                    jb = J_copy.pop(counter)
                    heapq.heappush(min_heap,(jb.processing_time,jb.index))
                    push = True
                    counter -= 1
                    break
            if not push and job.release_date < J_copy[counter+1].release_date:
                break
            counter += 1


        if Machine_Load[min_machine_index] >= d:
            Machine_Avail[min_machine_index] = False
        if j.starting_time + j.processing_time <= d:
            Pieces_Produced += j.pieces
            count += 1
    return Pieces_Produced / 25, count

def WP_adjust(J,d) :
    J = sorted(J, key=lambda l: l.release_date, reverse=False)
    J_copy = copy.copy(J)
    Pieces_Produced = 0
    count = 0  # job count
    Machine_Avail = [True for _ in range(25)]
    Machine_Avail.insert(0, False)  # do not use machine_load[0]
    Machine_Load = [0 for _ in range(26)]  # init machine load
    Machine_T = [100 for _ in range(26)]  # init machine temperature
    min_heap = []  # min heap of processing time

    """init the min heap of WP"""
    while J_copy:
        j = J_copy.pop(0)
        if j.release_date == 0:
            heapq.heappush(min_heap, (j.WP, j.index))
        else:
            break
    if not min_heap:
        j = J_copy.pop(0)
        heapq.heappush(min_heap, (j.WP, j.index))

    """Main loop"""
    while min_heap:
        if reach_deadline(Machine_Avail):
            break
        j = J[heapq.heappop(min_heap)[1]]
        # print(j.index)
        setup = int(math.ceil(5 + abs(Machine_T[j.Mj[0]] - j.Temperature) * (0.1)))
        min_machine_index = j.Mj[0]
        min_machine_load = Machine_Load[j.Mj[0]] + setup
        for i in j.Mj[1:]:  # loop through machines that can run job j
            # do not consider temperature transformation time currently
            setup = int(math.ceil(5 + abs(Machine_T[i] - j.Temperature) * (0.1)))  # setup time
            if Machine_Load[i] + setup < min_machine_load and Machine_Avail[i] == True:  # find least loading machine
                min_machine_index = i
                min_machine_load = Machine_Load[i]
        j.Machine_Assigned = min_machine_index
        setup = int(math.ceil(5 + abs(Machine_T[min_machine_index] - j.Temperature) * (0.1)))  # setup time
        Machine_T[min_machine_index] = j.Temperature  # assing new temperature
        # update machine load and starting time
        Machine_Load[min_machine_index] = max(j.release_date, Machine_Load[min_machine_index])
        Machine_Load[min_machine_index] += setup + j.processing_time
        j.starting_time = Machine_Load[min_machine_index] - j.processing_time
        # for j in J_copy :
        #     print(j.release_date)
        """if job release, add to min heap"""
        counter = 0
        while len(J_copy) > 1:
            job = J_copy[counter]
            r = job.release_date
            push = False  # boolean variable : if push or not
            for i in job.Mj:
                # push = False
                if Machine_Load[i] >= r:
                    job = J_copy.pop(counter)
                    heapq.heappush(min_heap, (job.WP, job.index))
                    push = True
                    counter -= 1
                    break
            if not push and job.release_date < J_copy[counter + 1].release_date:
                break
            counter += 1

        if Machine_Load[min_machine_index] >= d:
            Machine_Avail[min_machine_index] = False
        if j.starting_time + j.processing_time <= d:
            Pieces_Produced += j.pieces
            count += 1
    return Pieces_Produced / 25, count

def count_LFM_value(J, d, M_index):
    count=0
    for k, j in enumerate(J):
        if M_index in j.Mj and j.is_processed==False:
            count+=1
    return count

def min_M_Load(Machine_Load,j):
    min=Machine_Load[j.Mj[0]]
    for k, j in enumerate(j.Mj):
        if Machine_Load[j]<min:
            min = Machine_Load[j]

    return min

def is_still_Avail(Machine_Load,d):

    for i in range(1,len(Machine_Load)):
        if Machine_Load[i]<d:
            return True
    return False

def released_job_in_NS(J,t):
    # min_r=-1
    for k, j in enumerate(J):
        if j.is_processed==False and j.release_date<=t:
            return True
    return False

def find_min_r_j(J,t):
    for k, j in enumerate(J):
        if j.is_processed==False :
            return j.release_date

def count_LFJ_value(Mj,Machine_Avail):
    count=0
    for i,j in enumerate(Mj):
        if Machine_Avail[j]==True :
            count+=1
    return count
