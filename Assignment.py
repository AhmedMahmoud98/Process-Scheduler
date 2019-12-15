import numpy as np
import sys
import os

Number_Of_Arguments = len(sys.argv)

if(Number_Of_Arguments < 3):
    print("There is an missed argument")
    exit()

Input_File_Name = sys.argv[1]
Output_File_Name = sys.argv[2]
Number_Of_Processes = 0
Arrival_Time_Parameters = ()
Burst_Time_Parameters = ()
Priority_Parameter  = 0

if os.path.exists(Input_File_Name):
   with open(Input_File_Name, 'r') as Input_File:
       try:
           Inputs = Input_File.readlines()
           Number_Of_Processes = int(Inputs[0])
           Arrival_Time_Parameters = tuple(map(float, Inputs[1].split(' '))) 
           Burst_Time_Parameters = tuple(map(float, Inputs[2].split(' '))) 
           Priority_Parameter = float(Inputs[3])           
       except (OSError, IOError) as e:
           print("Error in reading input file")
           exit()
           
Output_File = open(Output_File_Name, "w+")
Output_File.write(str(Number_Of_Processes) + "\n")
for i in range(1, Number_Of_Processes + 1):
    Process_Data = (abs(int(np.random.normal(Arrival_Time_Parameters[0], Arrival_Time_Parameters[1]))),
    abs(int(np.random.normal(Burst_Time_Parameters[0], Burst_Time_Parameters[1]))),
    abs(int(np.random.poisson(Priority_Parameter))))
    Output_File.write(str(i) + " " + " ".join(map(str,Process_Data)) +"\n")

