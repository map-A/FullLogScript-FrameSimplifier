import pandas as pd
import os
import subprocess
import time


files_info = {
    "3DMark_FireStrike-Extreme-orgSize-FixFPS0.5-GT1.csv":119,
    #"3DMark_SkyDiver-orgSize-FixFPS0.5-gt2.csv":6,
    #"3DMark_CloudGate-orgSize-FixFPS0.5-GT2.csv":21,
    #"3DMark_CloudGate-orgSize-FixFPS0.5-GT1.csv": 19,
    #"3DMark_FireStrike-orgSize-FixFPS0.5-GT1.csv":25,
    }
dont_exit = []
for csv_name,index in files_info.items():
    print(csv_name,index)
    df = pd.read_csv(csv_name)
    path = os.path.join(os.getcwd(), csv_name[:-4]+"\\vector",)
    for filename in os.listdir(path):
        if filename.endswith('_0.sdx'): 
            for j in df['Cmdbuf_Draw_Idx']:
                flag = 1
                for filename2 in os.listdir(path):
                    if "D" + str(j) + "_Trim.sdx" in filename2:
                        print(f"找到文件:{filename2}")
                        flag = 0

                        break
                if flag==0:
                    flag=1
                    continue

                cmd1 = ".\\TrimDX.exe -s " + os.path.join(path, filename) +" -f " +str(index) + " -d " +str(j)
                # cmd1 = ".\\TrimDX.exe -s " + os.path.join(path, filename) +" -f " +str(index) + " -l " +str(i)
                print(cmd1)
                p1 = subprocess.Popen(cmd1, shell=True)
                p1.wait()
                ## 检查是否有trim.sdx文件
                new_filename = " "
                for filename2 in os.listdir(path):
                    if "D" + str(j) + "_Trim.sdx" in filename2:
                        print(f"找到文件:{filename2}")
                        new_filename = filename2
                        break 

                time.sleep(2) 
                cmd2 = ".\\qReplay\\qReplay.exe -s " + os.path.join(path, filename) + " --inject " + filename.replace("_0.sdx","__Trim.inject")
                # p2 = subprocess.Popen(cmd2, shell=False)
                # p2.wait()
                # time.sleep(2)

                new_filename1 = os.path.join(path, new_filename)
                output_dir =  os.path.join(path, new_filename[:-4])+"\\"
                cmd3 = ".\\ExtractScriptResource.exe -s "+ new_filename1 +" -o "+ output_dir
                # p3 = subprocess.Popen(cmd3, shell=True)
                # p3.wait()
                # time.sleep(2)

         
                # try:
                #     os.remove(os.path.join(path,filename.replace("_0.sdx","__Trim.inject")))
                # except:
                #     pass
print("没有trim的所在行",dont_exit)