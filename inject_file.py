
import re
import os
import copy
from line_util import *
class InjectFile():
    def __init__(self,file_collection,sava_path,des_pos) -> None:
        self.inject_file_path = file_collection.src_path
        self.inject_file_name = file_collection.file_list[0].replace('_0.sdx','_Trim.inject')
        if file_collection.dx_version==12:
            self.inject_file_name = file_collection.file_list[0].replace('0.sdx','_Trim.inject')
        self.save_path = sava_path # inject文件保存的路径
        self.file_collection = file_collection
        self.inject_des_pos = des_pos
        self.dont_save_resources = {} # 每个文件不需要保存的资源
        

    def generate_dx11_inject_file(self,graph):
        with open(os.path.join(self.inject_file_path,self.inject_file_name), "w") as inj:
            for filename in self.file_collection.file_list[:self.inject_des_pos+1]:
                with open(os.path.join(self.save_path,filename), "r") as f:
                    index = 0
                    lines = f.readlines()
                    for line in lines:
                        if is_var_statement(line):
                            continue
                        elif is_object_func_call(line):
                            resouce_list = get_resource_from_line(line)
                            ret = parse_object_func_call(line)
                            ref_list = []
                            for val in resouce_list:
                                graph.get_leaf(val,ref_list) # 获取了val的所在路径所有变量
                            if(len(ref_list)!=0):
                                file_pos = 'F'+ re.search(r'(\d+)\.sdx$', filename).group(1)
                                line_pose = 'L'+ str(len(lines))
                                argumets = "|".join(ref_list)
                                save_type = ".bin"
                                new_resoure = "\"new_resource" +  "_"+  file_pos + "_"+ line_pose + save_type +"\");\n"
                                upload_function="axdDumpResource("
                                function= upload_function+ret[0] + ',IID_ID3D11Resource,DXGI_FORMAT_UNKNOWN,'
                                inj.write(file_pos+","+ line_pose +"," + function + argumets+',0,' + new_resoure)
                
                        elif is_func_call(line):
                            ret = parse_func_call(line)
                            if(ret[0]=="axdRelease"):
                                file_pos = int(re.search(r'(\d+)\.sdx$', filename).group(1))
                                if ret[1][0] not in self.dont_save_resources:
                                    self.dont_save_resources[ret[1][0]] = []
                                self.dont_save_resources[ret[1][0]].append(file_pos)
                        index = index+1
                    inj.write('\n')


    def generate_final_dx11_inject_file(self,save_start_index):
        # 去除掉含有相同resource的lines
        # 在begin_frame 之前的resource dump下来，最近的，以前重复的不要
        with open(os.path.join(self.inject_file_path,self.inject_file_name), 'r') as org_inj:
            lines = org_inj.readlines()

        # 读取到内存中删去重复的
        data = {}
        for line in lines:
            fields = line.split(',')
            if len(fields) >= 6 and int(fields[0][1:])<save_start_index:
                new_field = copy.deepcopy(fields)
                resources = fields[5].split('|')
                for resource in resources:
                    if self.dont_save_resources.get(resource) and int(fields[0][1:]) <= min(self.dont_save_resources[resource]):
                        continue

                    # TODO: 如果有constant buffer，那么就不需要注入，这里重复了很多次，可以优化
                    #if (resource[0:4] == "pBuf" or resource[0:4] == "pTex"):
                    new_field[5] = resource.strip()
                    resource_type = ".bin"
                    if(new_field[5][0:4] != "pBuf"):
                        resource_type = ".dds"
                    new_field[7] = "\""+ new_field[5] + "_"+new_field[0]+ "_"+ new_field[1] + resource_type +"\");\n"

                    key = new_field[5]
                    if (key[0:4] == "pBuf" or key[0:4] == "pTex"):
                        data[key] = ', '.join(new_field)
        
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
        with open(os.path.join(self.save_path,self.inject_file_name), 'w') as fin_inj:
            for l in lines:
                fin_inj.write(l)        

    def generate_dx12_inject_file(self,graph):
        with open(os.path.join(self.inject_file_path,self.inject_file_name), "w") as inj:
            for filename in self.file_collection.file_list[:self.inject_des_pos+1]:
                # print(filename)
                with open(os.path.join(self.save_path,filename), "r") as f:
                    index = 0
                    lines = f.readlines()
                    for line in lines:
                        if is_object_func_call(line):
                            resouce_list = get_resource_from_line(line)
                            ret = parse_object_func_call(line)
                            ref_list = []
                            tt = ret[0]
                            if tt=="pDev12_0":
                                tt = "pCmdList_1"
                            for val in resouce_list:
                                graph.get_leaf(val,ref_list) # 获取了val的所在路径所有变量
                            if(len(ref_list)!=0):
                                #TODO：多个resource共用一个var name
                                file_pos = 'F'+ re.search(r'(\d+)\.sdx$', filename).group(1)
                                line_pose = 'L'+ str(len(lines))
                                argumets = "|".join(ref_list)
                                save_type = ".bin"
                                new_resoure = "\"new_resource" +  "_"+  file_pos + "_"+ line_pose + save_type +"\");\n"
                                upload_function="axdDumpResourceInCmdList("
                                function= upload_function+tt + ',IID_ID3D12Resource,'
                                inj.write(file_pos + ","+ line_pose +","+ function + argumets+ ","+ "DXGI_FORMAT_UNKNOWN, "+'0, ' + new_resoure)
                        elif is_func_call(line):
                            ret = parse_func_call(line)
                            if(ret[0]=="axdRelease"):
                                file_pos = int(re.search(r'(\d+)\.sdx$', filename).group(1))
                                if ret[1][0] not in self.dont_save_resources:
                                    self.dont_save_resources[ret[1][0]] = []
                                self.dont_save_resources[ret[1][0]].append(file_pos)
                        index = index+1
                    inj.write('\n')
    def generate_final_dx12_inject_file(self,graph,save_start_index):
         # 去除掉含有相同resource的lines
        # 在begin_frame 之前的resource dump下来，最近的，以前重复的不要
        with open(os.path.join(self.inject_file_path,self.inject_file_name), 'r') as org_inj:

            lines = org_inj.readlines()


        # 读取到内存中删去重复的
        data = {}
        for line in lines:
            fields = line.split(',')

            if len(fields) >= 7 and int(fields[0][1:])<save_start_index:
                new_field = copy.deepcopy(fields)
                resources = fields[4].split('|')
                resource_type = ".bin"
                for resource in resources:
                    if self.dont_save_resources.get(resource) and int(fields[0][1:]) <= min(self.dont_save_resources[resource]):
                        continue
                    new_field[4] = resource.strip()
                

                    # todo： 设置如何获取资源的类型
                    a = []
                    graph.get_leaf(resource,a)
                    for aa in a:
                        if re.match(r'resDesc_\d+$',aa):
                            resource_type = get_resource_type(graph.get_node(aa)[0].line)
                    new_field[7] = "\""+ new_field[4] + "_"+new_field[0]+ "_"+ new_field[1] + resource_type +"\");\n"
                    # pCommitRes_8_GpuAddr_601856
                    if re.match(r'pCommitRes_\d+$',new_field[4]):
                    # if ("Res_" in new_field[4]):
                        data[new_field[4]] = ', '.join(new_field)
        
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
        with open(os.path.join(self.save_path,self.inject_file_name), 'w') as fin_inj:
            for l in lines:
                fin_inj.write(l)    


