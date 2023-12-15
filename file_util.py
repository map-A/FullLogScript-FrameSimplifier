import os
import re
import sys
import shutil

# 读取某个文件夹下所有文件名到列表
class FileCollection():
    def __init__(self,src_path,temp_path,refactor_path,dump_path,end_index) -> None:
        self.src_path = src_path
        self.temp_path = temp_path
        self.refactor_path = refactor_path
        self.dump_path = dump_path
        self.file_list = []
        self.end_index = end_index
        self.read_dir()
        self.trim_files(self.temp_path)
        self.dx_version = self.get_dx_version()
        
        

    def read_dir(self):
        if not os.path.exists(self.src_path):
            print(self.src_path+' does not exist')
            sys.exit()
        for filename in os.listdir(self.src_path):
            if filename.endswith(".sdx") and "_" in filename and filename.split("_")[1][:-4].isdigit() and int(filename.split("_")[1][:-4])<=self.end_index:
                self.file_list.append(filename)
       
        self.file_list.sort(key=lambda x: int(x.split("_")[1][:-4].split(".")[0]))

    def trim_files(self,target_path):
        """
        将把文件夹下所有文本按照分号分割成句子，去除空格和换行符，写入新文件
        :param folder_path: 文件夹路径
        :param target_path: 目标保存文件夹路径
        :return: None
        """
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

        for filename in self.file_list:
            with open(os.path.join(self.src_path,filename), 'r') as f, open(os.path.join(target_path,filename), 'w') as out_f:
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

    def merge_files(self, target_path,start_index,target_index):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        new_file_name = "merge.sdx"
        with open(os.path.join(target_path,new_file_name), 'w') as target_file:
            for filename in self.file_list:
                if filename.split("_")[1][:-4].isdigit():
                    if int(filename.split("_")[1][:-4])<target_index and int(filename.split("_")[1][:-4])>=start_index:
                        print(filename)
                        with open(os.path.join(self.temp_path,filename)) as source_file:
                            target_file.write(source_file.read() + '\n')
   

    


    def get_dx_version(self):
        """
        获取DX版本
        :param src_path: 文件夹路径
        :return: DX版本 11,12,0,0表示出错
        """
        if not os.path.exists(self.src_path):
            print(self.src_path+' does not exist')
            sys.exit()
        with open(self.src_path + self.file_list[0], 'r') as f:
            for line in f:
                if re.match(r'D3D12CreateDevice', line):
                    return 12
                elif re.match(r'D3D11CreateDevice', line):
                    return 11
        return 0