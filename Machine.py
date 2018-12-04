import math
import heapq
from random import uniform
class Machines(object) :
    class Machine(object):

        def __init__(self,index):
            self.index      = index
            self.Jobs       = []  # jobs that can be operated by this machine
            self.Job_list = []  # jobs that can be processed currently
            self.Job_done = [] #jobs that assigned to this machine
            self.total_pt   = 0  # total processing time
            self.total_rt = 0  # total release time
            self.total_weight = 0  # total weight
            self.Temp = []  # list of temperature
            self.Temperature = 100 #current temperature
            self.load = 0  # machine load.
            self.avail = True
            self.num_jobs = 0
            self.count = 0
        def Add_job(self,job):
            self.Jobs.append(job)
            self.Temp.append(job.Temperature)
            self.total_pt     += job.processing_time
            self.total_rt     += job.release_date
            self.total_weight += job.weight
            self.num_jobs     += 1
        def select_job(self,rule):
            self.update_joblist(rule)
            candidate = None
            while  candidate == None or candidate.is_processed == True:
                if not self.Jobs : #every job in machine has been processed
                    self.avail = False
                    return False
                #print(self.index,self.Jobs,self.load)
                if not self.Job_list: #if no job list , add nearest one to job list
                    j = min(self.Jobs, key=lambda x : x.release_date)
                    self.Jobs.remove(j)
                    heapq.heappush(self.Job_list,(rule(j),j))
                candidate = heapq.heappop(self.Job_list)[1]
            return candidate
        def assign_job(self,job,d) :

            setup = 5 + abs(self.Temperature - job.Temperature) * (0.1)
            setup = int(math.ceil(setup))
            # print(self.Temperature - job.Temperature,setup)
            self.Temperature = job.Temperature
            self.load = max(job.release_date,self.load)
            self.load += setup + job.processing_time
            if self.load >= d :
                self.avail = False
                return False
            job.Machine_Assigned = self.index
            job.starting_time = self.load - job.processing_time
            job.is_processed = True
            self.Job_done.append(job)

            return True


            # self.update_joblist()

        # def delete_job(self,job):
        #     for i in range(len(self.Job_list)) :
        #         if self.Job_list[i] == job :
        #             del self.Job_list[i]
        #             return
        #     print("Delete fail")
        def update_joblist(self,rule):
            del_list = []
            for j in self.Jobs :
                if self.load >= j.release_date :
                    del_list.append(j)
                    # print(self.index,j.processing_time,j,self.load)
                    heapq.heappush(self.Job_list, (rule(j) + j.index * 0.00000001 , j)) #heapq does not support same value comparison
                    self.count += 1
                    # heapq.heapify(self.Job_list)
                    # self.Job_list.append((j.processing_time,j))
                    # print(self.load,self.index,j.index)
                else :
                    break
            for j in del_list :
                self.Jobs.remove(j)
    num_machines = 25

    def __init__(self,J) :
        self.machine_list = [self.Machine(i) for i in range(self.num_machines+1)]
        for j in J  :
            for m in j.Mj :
                self.machine_list[m].Add_job(j)
        for i in range(1,26) :
            self.machine_list[i].Jobs.sort(key = lambda x : x.release_date)

    def select_machine(self,selection_rule = lambda x : x.load , second_rule = lambda x : x.release_date):
        #can be improved by heap and binary search
        sel_machine = self.machine_list[1]
        for m in self.machine_list[1:] :
            if m.avail == True and m.Jobs and sel_machine.Jobs:

                # print((selection_rule(sel_machine) == selection_rule(m)  and second_rule(sel_machine.Jobs[0]) > second_rule(m.Jobs[0])))
                if sel_machine.load > m.load or (sel_machine.load == m.load and sel_machine.Jobs[0].release_date > m.Jobs[0].release_date):
                    sel_machine = m
        # print(sel_machine.index,sel_machine.Jobs)
        return sel_machine
    def reach_deadline(self):
        for m in self.machine_list :
            if m.avail == True :
                return False
        return True


