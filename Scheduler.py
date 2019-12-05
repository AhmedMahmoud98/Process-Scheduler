import numpy as np
import sys
import os

class Process:
    def __init__(self,PID , Arrival_Time , Burst_Time, Priority, Starting_Time = -1, Remaining_Time = -1):
        self.PID = PID 
        self.Arrival_Time = Arrival_Time
        self.Burst_Time = Burst_Time
        self.Priority = Priority
        self.Remaining_Time = Burst_Time
        self.Starting_Time = -1
        
class Scheduler:
    def __init__(self, Processes, Scheduling_Algorithm, Context_Switch_Time, Quantam = -1):
        self.Processes = Processes
        self.Scheduling_Algorithm = Scheduling_Algorithm
        self.Context_Switch_Time = Context_Switch_Time
        self.Quantam = Quantam
        self.Results = dict((key, []) for key in range(1, len(Processes) + 1))
        self.Context_Switch = [()]
        self.Ideal = [()]
        
    def Sort(self):
        if(Scheduling_Algorithm == "HPF"):
            self.Processes = sorted(self.Processes, key=lambda p: (p.Arrival_Time, p.Priority, p.PID))
        
        elif(Scheduling_Algorithm == "FCFS"):
            self.Processes = sorted(self.Processes, key=lambda p: (p.Arrival_Time, p.PID))
        
        elif(Scheduling_Algorithm == "SRTN"):
            self.Processes = sorted(self.Processes, key=lambda p: (p.Arrival_Time, p.Burst_Time, p.PID))
            
        elif(Scheduling_Algorithm == "RR"):
            self.Processes = sorted(self.Processes, key=lambda p: (p.Arrival_Time, p.PID))
            
    def Schedule(self):
        self.Sort()
        Step = 0
#########################################################################################               
        if(Scheduling_Algorithm == "HPF" or Scheduling_Algorithm == "FCFS"):
            for index, Process in enumerate(self.Processes):
                if(Process.Arrival_Time > Step):
                    self.Ideal.append((Step, Process.Arrival_Time))
                    Step = Process.Arrival_Time
                    
                if(index != 0 and Context_Switch_Time != 0):
                    self.Context_Switch.append((Step, Step + self.Context_Switch_Time ))
                    Step += self.Context_Switch_Time
    
                self.Results[Process.PID].append((Step, Step + Process.Burst_Time))
                Step += Process.Burst_Time
########################################################################################
        if(Scheduling_Algorithm == "SRTN"):
            
            Temp_Processes = self.Processes
            First_Time = True
            
            while(len(Temp_Processes) != 0):
                if(Temp_Processes[0].Arrival_Time > Step):
                    self.Ideal.append((Step, Temp_Processes[0].Arrival_Time))
                    Step = Temp_Processes[0].Arrival_Time
                    
                if(First_Time):
                    Start = Step
                    First_Time = False 
                    
                if(Temp_Processes[0].Starting_Time == -1):
                    Temp_Processes[0].Starting_Time = Step
                
                Temp_Processes[0].Remaining_Time -= 1
                Current_Process = Temp_Processes[0]
                Step += 1

                if(Current_Process.Remaining_Time == 0):
                    self.Results[Temp_Processes[0].PID].append((Start,Step))
                    Temp_Processes.pop(0)
                    if(len(Temp_Processes) == 0):
                        continue
                    Current_Process = Temp_Processes[0]
                    First_Time = True
                    
                
                for index in range(1, len(Temp_Processes)):
                    if(Temp_Processes[index].Arrival_Time > Step):
                            break
                    else:
                        print(Step,Temp_Processes[index].Arrival_Time, Step,Current_Process.Remaining_Time,Temp_Processes[index].Burst_Time)
                        if(Current_Process.Remaining_Time < Temp_Processes[index].Burst_Time):
                            break
                        else:
                            if(not First_Time):
                                self.Results[Temp_Processes[0].PID].append((Start,Step))
                            Temp_Processes.insert(0, Temp_Processes.pop(index))
                            if(Context_Switch_Time != 0):
                                self.Context_Switch.append((Step, Step + self.Context_Switch_Time))
                                Step += self.Context_Switch_Time - 1
                            First_Time = True
                            break
                
#############################################################################
        if(Scheduling_Algorithm == "RR"):
            Arrived = []
            for Process in self.Processes:
                if(Process.Arrival_Time <= Step):
                    Arrived.append(Process)
                    self.Processes.pop(0)
                else:
                    break
                    
            while(True):
                Temp = sorted(Temp, key=lambda p: (p.Arrival_Time, p.PID))
                Temp.append(Arrived)
                Arrived = Temp
                
                if(len(self.Processes) != 0 and len(Arrived) == 0):
                    self.Ideal.append((Step , self.Processes[0].Arrival_Time))
                    Step = self.Processes[0].Arrival_Time
                    continue
                    
                if(len(self.Processes) == 0 and len(Arrived) == 0):
                    break
                
                self.Results[Arrived[0].PID].append((Step, Step + Quantam))
                
                Step += Quantam
                if(Context_Switch_Time != 0):
                    self.Context_Switch.append((Step, Step + self.Context_Switch_Time))
                    Step += self.Context_Switch_Time
                Arrived.append(Arrived.pop(0))
#############################################################################                
   
Number_Of_Arguments = len(sys.argv)
if(Number_Of_Arguments < 4):
    print("There is an missed argument")
    exit()

Input_File_Name = sys.argv[1]
Scheduling_Algorithm = sys.argv[2]
Context_Switch_Time = int(sys.argv[3])
Quantam = 0

if(Scheduling_Algorithm == "RR") :
    if(Number_Of_Arguments < 5):
        print("There is an missed argument")
        exit()
    else:
        Quantam = int(sys.argv[4]) 

#load processes into array Process_Arr
Process_Arr = []
if os.path.exists(Input_File_Name):
   with open(Input_File_Name, 'r') as Input_File:
       try:
            for line in Input_File: # read rest of lines
                arr = [int(x) for x in line.split()]
                if(len(arr) != 0):
                    Process_Arr.append(Process(arr[0], arr[1],arr[2],arr[3]))
       except (OSError, IOError) as e:
           print("Error in reading input file")
           exit()

Scheduler = Scheduler(Process_Arr ,Scheduling_Algorithm, Context_Switch_Time, Quantam)
Scheduler.Schedule()
print(Scheduler.Results)
print(Scheduler.Ideal)
print(Scheduler.Context_Switch)