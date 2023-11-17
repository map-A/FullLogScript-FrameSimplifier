import re
import shutil
import subprocess
import os
import sys
path = "D:\\work\\dx12\\3DMarkNightRaid-GT1-fixfps1\\vector\\3DMarkNightRaid_0.sdx"
path1 = "D:\\work\\dx12\\3DMarkNightRaid-GT1-fixfps1\\trim\\"
path2 = "D:\\work\\dx12\\3DMarkNightRaid-GT1-fixfps1\\inject\\"




if not os.path.exists(path2):
    os.makedirs(path2)
if not os.path.exists(path1):
    os.makedirs(path1)
number = 190
def merge_inject_file(path):
    inject_list = []
    for filename in os.listdir(path):
        if filename.endswith(".inject"):
            inject_list.append(filename)
    inject_list.sort(key=lambda x: int(x.split("_")[1][:-7]))
    print(inject_list)
    data = {}
    
    for filename in inject_list:
        with open(os.path.join(path,filename), "r") as f:
            for line in f:
                fields = line.split(',')
                if len(fields)>6:
                    data[fields[4]] = line

    lines = []
    for line in data.values():
        lines.append(line)
            
                

        # 定义一个函数，用于提取排序的关键字
    def get_key(line):
        fields = line.strip().split(',')
        return int(fields[0].strip()[1:]), int(fields[1].strip()[1:])
    # 对行进行排序
    lines.sort(key=get_key)
    # 将排序后的行写入新的文件
    with open(os.path.join(path,"inject_all.inject"), "w") as fin_inj:
        for l in lines:
            fin_inj.write(l) 




for draw_num in range(0, 2):
    cmd = ".\\TrimDX.exe -s "+ path +" -f " + str(number) +" -d " + str(draw_num)
    p1 = subprocess.Popen(cmd, shell=True)
    p1.wait()
    # 重命名inject文件
    # 找到生成的inject文件
    
    for filename in os.listdir(os.path.dirname(path)):
        if "D"+str(draw_num) in filename:
            os.rename(os.path.join(os.path.dirname(path),filename),os.path.join(path1,filename))
        if filename.endswith(".inject"):
            os.rename(os.path.join(os.path.dirname(path),filename),os.path.join(path2,"inject_"+str(draw_num)+".inject"))
            

#合并inject文件
# merge_inject_file(path2)
# os.rename(os.path.join(path2,"inject_all.inject"),os.path.join(os.path.dirname(path),"3DMarkNightRaid_Trim.inject"))
# #生成dump文件
# cmd = ".\\qReplay\\qReplay.exe -s "+ path +" --inject 3DMarkNightRaid_Trim.inject"
# #+ " --hide"
# p1 = subprocess.Popen(cmd, shell=True)
# p1.wait()

# 对Trim.sdx 合并
# 首先是整理成行
# 然后去除重复的
def trim_files(src_path,target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    else:
        # 删除子文件夹和文件
        for f in os.listdir(target_path):
            full_path = os.path.join(target_path, f)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)

    if not os.path.exists(src_path):
        print(src_path+' does not exist')
        sys.exit()
    file_list = []
    for filename in os.listdir(src_path):
        "3DMarkNightRaid__F190_L1016D0_Trim.sdx"
        pattern = r'(.*)__F(\d+)_L(\d+)D(\d+)_Trim.sdx'
        match = re.match(pattern,filename)
        if match:
            file_list.append(filename)

    file_list.sort(key=lambda x: int(match.group(4)))

    for filename in file_list:
        with open(os.path.join(src_path,filename), 'r') as f, open(os.path.join(target_path,filename), 'w') as out_f:
            sentence = ""
            index = 0
            for line in f:
                index = index + 1
                line = line.strip()
                if(index <2): #忽略前两行
                    out_f.write(line + '\n')
                    continue
                else:
                    if re.search(r'[;]', line):
                        sentence += line
                        out_f.write(sentence + '\n')
                        sentence = ""
                    else:
                        sentence += line
            if sentence:
                out_f.write(sentence + '\n')
    print("trim successful")

trim_files(path1,os.path.dirname(path1)+"trim1\\")







