import sys
import os
import matplotlib.pyplot as plt
import numpy as np


class Process:
    def __init__(self, PID, Arrival_Time, Burst_Time, Priority, Starting_Time=-1, Remaining_Time=-1):
        self.PID = PID
        self.Arrival_Time = Arrival_Time
        self.Burst_Time = Burst_Time
        self.Priority = Priority
        self.Remaining_Time = Burst_Time
        self.Starting_Time = -1

    def __repr__(self):
        return "Process()"

    def __str__(self):
        return "PID {}, Arrival_Time {}, Burst_Time {}, Priority {}, Starting_Time {}, Remaining_Time {}".format(self.PID, self.Arrival_Time, self.Burst_Time, self.Priority, self.Starting_Time, self.Remaining_Time)


class Scheduler:
    def __init__(self, Processes, Scheduling_Algorithm, Context_Switch_Time, Quantam=-1):
        self.Processes = Processes
        self.ProcessesCpy = Processes
        self.Scheduling_Algorithm = Scheduling_Algorithm
        self.Context_Switch_Time = Context_Switch_Time
        self.Quantam = Quantam
        self.Results = dict((key, []) for key in range(1, len(Processes) + 1))
        self.Process_Data = dict((key, [])
                                 for key in range(1, len(Processes) + 1))
        self.Schedule_Data = []
        self.Context_Switch = []
        self.Ideal = []

    def __repr__(self):
        return "Scheduler()"

    def output_data(self, Data_File_Name="data.txt"):
        for p in self.Processes:
            # turnaround time [0]
            self.Process_Data[p.PID].append(
                self.Results[p.PID][-1][1] - p.Arrival_Time)
            # weigthed turnaround time [1]
            self.Process_Data[p.PID].append(
                self.Process_Data[p.PID][0]/p.Burst_Time)
            # waiting time [2]
            self.Process_Data[p.PID].append(
                self.Process_Data[p.PID][0] - p.Burst_Time)
        Avg_TA = 0
        Avg_TA_Weighted = 0
        for p in self.Processes:
            Avg_TA += self.Process_Data[p.PID][0]
            Avg_TA_Weighted += self.Process_Data[p.PID][1]

        if len(self.Processes) > 0:
            # avg turnaround time [3]
            self.Schedule_Data.append(Avg_TA/len(self.Processes))
            # avg weigthed turnaround time [4]
            self.Schedule_Data.append(Avg_TA_Weighted/len(self.Processes))
        else:
            self.Schedule_Data.append([0, 0])
        Data_File = open(Data_File_Name, "w")
        Data_File.write(
            "Processes Data:\nPID\t\t\t\tTA\t\t\t\tTA_W\t\t\tW_T\n")
        for p in self.Processes:
            Data_File.write(str(p.PID) + "\t\t\t\t" + str(self.Process_Data[p.PID][0]) + "\t\t\t\t" + str(
                round(self.Process_Data[p.PID][1], 1))+"\t\t\t\t" + str(self.Process_Data[p.PID][2]) + "\n")
        Data_File.write("\nSchedule Data:\nAvg_TA = " + str(
            self.Schedule_Data[0]) + "\nAVG_TA_Weighted = " + str(self.Schedule_Data[1]) + "\n")

    def Sort(self):
        if(Scheduling_Algorithm == "HPF"):
            self.ProcessesCpy = sorted(self.ProcessesCpy, key=lambda p: (
                p.Arrival_Time, p.Priority, p.PID))

        elif(Scheduling_Algorithm == "FCFS"):
            self.ProcessesCpy = sorted(
                self.ProcessesCpy, key=lambda p: (p.Arrival_Time, p.PID))

        elif(Scheduling_Algorithm == "SRTN"):
            self.ProcessesCpy = sorted(self.ProcessesCpy, key=lambda p: (
                p.Arrival_Time, p.Remaining_Time, p.PID))

        elif(Scheduling_Algorithm == "RR"):
            self.ProcessesCpy = sorted(
                self.ProcessesCpy, key=lambda p: (p.Arrival_Time, p.PID))

    def Schedule(self):
        self.Sort()
        Step = 0
#########################################################################################
        if(Scheduling_Algorithm == "HPF"):
            while(len(self.ProcessesCpy) != 0):
                if(self.ProcessesCpy[0].Arrival_Time > Step):
                    self.Ideal.append(
                        (Step, self.ProcessesCpy[0].Arrival_Time))
                    Step = self.ProcessesCpy[0].Arrival_Time

                self.Results[self.ProcessesCpy[0].PID].append(
                    (Step, Step + self.ProcessesCpy[0].Burst_Time))
                Step += self.ProcessesCpy[0].Burst_Time
                self.ProcessesCpy.pop(0)
                i = 0
                for p in self.ProcessesCpy:
                    if(p.Arrival_Time > Step):
                        break
                    i += 1
                if(i != 0):
                    # sorted -> max
                    self.ProcessesCpy[:i] = sorted(self.ProcessesCpy[:i],
                                                   key=lambda p: (p.Priority, p.PID))
                if(Context_Switch_Time != 0 and len(self.ProcessesCpy) != 0):
                    self.Context_Switch.append(
                        (Step, Step + self.Context_Switch_Time))
                    Step += self.Context_Switch_Time
#########################################################################################
        elif(Scheduling_Algorithm == "FCFS"):
            for index, Process in enumerate(self.ProcessesCpy):
                if(Process.Arrival_Time > Step):
                    self.Ideal.append((Step, Process.Arrival_Time))
                    Step = Process.Arrival_Time

                if(index != 0 and Context_Switch_Time != 0):
                    self.Context_Switch.append(
                        (Step, Step + self.Context_Switch_Time))
                    Step += self.Context_Switch_Time

                self.Results[Process.PID].append(
                    (Step, Step + Process.Burst_Time))
                Step += Process.Burst_Time
########################################################################################
        elif(Scheduling_Algorithm == "SRTN"):

            Temp_Processes = self.ProcessesCpy
            First_Time = True

            while(len(Temp_Processes) != 0):
                end = False
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
                    self.Results[Temp_Processes[0].PID].append((Start, Step))
                    Temp_Processes.pop(0)
                    if(len(Temp_Processes) == 0):
                        continue
                    if(Context_Switch_Time != 0):
                        self.Context_Switch.append(
                            (Step, Step + self.Context_Switch_Time))
                        end = True
                        Step += self.Context_Switch_Time
                    Current_Process = Temp_Processes[0]
                    First_Time = True
                    
                i = 0
                for p in Temp_Processes[1:len(Temp_Processes)]:
                    if(p.Arrival_Time > Step):
                        break
                    i += 1
                if(i != 0):
                    # sorted -> max
                    Temp_Processes[1:i] = sorted(Temp_Processes[1:i],
                                                   key=lambda p: (p.Remaining_Time, p.PID))
                    
              
                for index in range(1, len(Temp_Processes)):
                    if(Temp_Processes[index].Arrival_Time > Step):
                        break
                    else:
                        if(Current_Process.Remaining_Time <= Temp_Processes[index].Burst_Time):
                            continue
                        else:
                            if(not First_Time):
                                self.Results[Temp_Processes[0].PID].append(
                                    (Start, Step))
                            Temp_Processes.insert(0, Temp_Processes.pop(index))
                            if(not end and Context_Switch_Time != 0):
                                self.Context_Switch.append(
                                    (Step, Step + self.Context_Switch_Time))
                                Step += self.Context_Switch_Time
                            First_Time = True
                            break

#############################################################################
        elif(Scheduling_Algorithm == "RR"):
            Arrived = []
            if(len(self.ProcessesCpy) != 0 and self.ProcessesCpy[0].Arrival_Time != 0):
                self.Ideal.append((Step, self.ProcessesCpy[0].Arrival_Time))
                Step = self.ProcessesCpy[0].Arrival_Time
                
            Temp = np.copy(self.ProcessesCpy)
            for Process in Temp:
                if(Process.Arrival_Time == Step):
                    Arrived.append(self.ProcessesCpy.pop(0))
                else:
                    break
                
            while(True):
                if(len(self.ProcessesCpy) != 0 and len(Arrived) == 0):
                    self.Ideal.append(
                        (Step, self.ProcessesCpy[0].Arrival_Time))
                    Step = self.ProcessesCpy[0].Arrival_Time

                if(len(self.ProcessesCpy) == 0 and len(Arrived) == 0):
                    break

                if(len(Arrived) != 0):
                    if(self.Quantam < Arrived[0].Remaining_Time):
                        self.Results[Arrived[0].PID].append(
                            (Step, Step + self.Quantam))
                        Step += Quantam
                        Arrived[0].Remaining_Time -= Quantam
                    else:
                        self.Results[Arrived[0].PID].append(
                            (Step, Step + Arrived[0].Remaining_Time))
                        Step += Arrived[0].Remaining_Time
                        Arrived[0].Remaining_Time = 0
                if(Context_Switch_Time != 0 and len(Arrived) > 1):
                    self.Context_Switch.append(
                        (Step, Step + self.Context_Switch_Time))
                    Step += self.Context_Switch_Time

                Temp = []
                Count = 0
                for Process in self.ProcessesCpy:
                    if(Process.Arrival_Time <= Step):
                        Temp.append(Process)
                        Count += 1
                    else:
                        break

                self.ProcessesCpy = self.ProcessesCpy[Count:]
                if(len(Temp)):
                    Temp = sorted(Temp, key=lambda p: (p.Arrival_Time, p.PID))
                    Arrived.extend(Temp)
                if(Arrived[0].Remaining_Time != 0):
                    Arrived.append(Arrived.pop(0))
                else:
                    Arrived.pop(0)
#############################################################################

    def Draw(self):
        all_tuples = []
        Ideal_level = (0,)
        temp = ()
        for i in range(len(self.Ideal)):
            temp = self.Ideal[i] + Ideal_level
            all_tuples.append(temp)

        Context_Switch_level = (-1,)
        for i in range(len(self.Context_Switch)):
            temp = self.Context_Switch[i] + Context_Switch_level
            all_tuples.append(temp)

        for level_result in self.Results.items():
            for i in range(len(level_result[1])):
                temp = level_result[1][i] + (level_result[0],)
                all_tuples.append(temp)

        all_tuples = sorted(all_tuples, key=lambda tup: tup[0])

        x = []
        y = []
        for period in all_tuples:
            x.append(period[0])
            y.append(period[2])

        x.append(all_tuples[len(all_tuples) - 1][1])
        y.insert(0, 0)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.xticks(x, x)
        plt.yticks(y, y)

        ax.step(x, y)
        ratio = 0.5
        xleft, xright = ax.get_xlim()
        ybottom, ytop = ax.get_ylim()
        ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
        fig.set_figheight(15)
        fig.set_figwidth(20)
        plt.savefig('Graph.png')


#############################################################################
Number_Of_Arguments = len(sys.argv)
if(Number_Of_Arguments < 4):
    print("There is an missed argument")
    sys.exit()

Input_File_Name = sys.argv[1]
Scheduling_Algorithm = sys.argv[2]
Context_Switch_Time = int(sys.argv[3])
Quantam = 0

if(Scheduling_Algorithm == "RR"):
    if(Number_Of_Arguments < 5):
        print("There is an missed argument")
        exit()
    else:
        Quantam = int(sys.argv[4])

# load processes into array Process_Arr
Process_Arr = []
if os.path.exists(Input_File_Name):
    with open(Input_File_Name, 'r') as Input_File:
        try:
            Number_Of_Processes = Input_File.readline()
            for line in Input_File:  # read rest of lines
                arr = [int(x) for x in line.split()]
                if(len(arr) != 0):
                    Process_Arr.append(Process(arr[0], arr[1], arr[2], arr[3]))
        except (OSError, IOError) as e:
            print("Error in reading input file")
            exit()

Scheduler = Scheduler(Process_Arr, Scheduling_Algorithm,
                      Context_Switch_Time, Quantam)
Scheduler.Schedule()
Scheduler.Draw()
Scheduler.output_data()
