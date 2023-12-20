# 现在是做帧的简化步骤，要求是从第i帧到第j帧，从某个文件开始到某个文件结束，比如截取58到60帧，从文件序号59开始，到文件序号61结束
# 然后组成新的文件

# 1. 读取文件夹下的所有文件，然后按照文件名排序，然后按照文件名的数字排序
# 2. 先用所有的文件构成一个图，
# 建图后该怎么进行重构，
# 先试着截取1帧
# 解决文件filename的依赖，把依赖保存到new_file_list中
from copy import deepcopy
import os
import re
import shutil
import struct
import subprocess
from line_util import *
from dx11_config import *

class SimpleFrame():
    def __init__(self) -> None:
        self.src_path = ""
        self.scene_begins_index = 1
        self.save_start_index = 1
        self.numbers_to_simple = 1
        self.save_end_index = 1

    def set(self,src_path = "",scene_begins_index= 1,save_start_index = 1,numbers_to_simple = 1):
        self.src_path = src_path
        self.scene_begins_index = scene_begins_index
        self.save_start_index = save_start_index
        self.numbers_to_simple = numbers_to_simple
        self.save_end_index = save_start_index+numbers_to_simple-1

        
    def solve_line_dependency(self,filename,line_pos,line,graph,new_file_list): 
        new_file_list.append([filename,line_pos])
        resource_list = get_resource_from_line(line)
        
        dependency_node = []
        for i in resource_list: 
            graph.dfs(i,dependency_node)
        new_file_list.extend(dependency_node)

        

    def solve_other(self,graph,draw_vectors,file_collection,target_path,new_filename_0):
        # 将draw_vector 的内容保存到new_filelist,draw_vector 都是实实在在的内容，写到s_dx0后面
        with open(os.path.join(target_path,new_filename_0), 'a') as new_file:
            for filename,draws, in draw_vectors.get_all().items():
                for draw in draws:
                    if draw.get_is_contain_cssetshader():
                        # 重写该文件的dispath 的内容
                        # 先是上传之前dump下来的buffer
                        save_lines = deepcopy(draw.get_draw_lines())
                        draw.clear_draw_lines()
                        for k,v, in draw.get_dump_resource().items():
                            if("pBuf_" in k or "pTex" in k):
                                new_file.write('axdUpdateSubresourcesFromFile(pCtx_0, IID_ID3D11Resource,'+k +', 0, 1,"'+ v +'", 0);\n')
                        # 修改iniconuts
                        # 怎么显示修改呢？这个要dump之后才能修改
                        for line in save_lines:
                            if "ID3D11UnorderedAccessView*" in line:
                                new_file.write(line)
                                uav_resouces = get_resource_from_line(line)[1:]
                                uav_resouce_ini_count = []
                                for uav_res in uav_resouces:
                                    while not os.path.exists(os.path.join(file_collection.dump_path,draw.get_dump_resource()[uav_res])):
                                        # 检测需要的数据是否有,没有，执行一遍qreplay
                                        cmd = r".\\qReplay\\qReplay.exe -s "+ os.path.join(file_collection.refactor_path,file_collection.file_list[0])
                                        print(cmd)
                                        p1 = subprocess.Popen(cmd, shell=True)
                                        p1.wait()
                                    with open(os.path.join(file_collection.dump_path,draw.get_dump_resource()[uav_res]), 'rb') as file:
                                    # 读取4个字节，即一个DWORD，采用小端模式('<')
                                        dword = struct.unpack('<I', file.read(4))
                                        uav_resouce_ini_count.append(str(dword[0]))
                            elif "UINT uavIniCounts_" in line:
                                # 根据uav_resouce_ini_count修改
                                pattern = r'\((.*?)\)'
                                matches = re.findall(pattern, line)

                                # 替换括号内的数字
                                if matches:
                                    updated_string = re.sub(pattern, f'({",".join(uav_resouce_ini_count)})',line)
                                    new_file.write(updated_string)
                                else:
                                    print("未找到括号内的数字")
                            elif 'CSSetUnorderedAccessViews' in line:
                                new_file.write(line)
                            elif 'CSSetShader' in line or 'Dispatch' in line:
                                pass
                            else:
                                pass
                                # new_file.write(line)




    def solve_dependency(self,graph,nodelists,filename,new_file_list):
        with open(filename, 'r') as f:
            line_pos = 0
            for line in f:
                self.solve_line_dependency(filename,line_pos,line,graph,new_file_list)         
                line_pos = line_pos+1

        for i in nodelists.nodes:
            for node in nodelists.nodes[i]: 
                new_file_list.append(node.line_pos)
                graph.dfs(node.id,new_file_list)

                # if(i in must_add): # 保证添加一次
                #     break;
        
    def simplify_frames(self,file_collection,graph,nodelist,draw_vectors,inject_file,target_path):
        """
        从save_start_index开始保存，到save_end_index结束，
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


        # save_start_index,save_end_index, 保存为1-n的文件

        new_file_list = []
        # 保存0的部分
        with open(os.path.join(file_collection.temp_path,file_collection.file_list[0]), 'r') as f:
            line_pos = 0
            for line in f.readlines():
                if line_pos<4 or "swapDesc" in line or "Present" in line: #前4行必须保留
                    new_file_list.append([file_collection.file_list[0],line_pos])
                line_pos = line_pos+1

        #直接保存非0的部分
        for i in range(self.save_start_index,self.save_end_index+1):
            new_filename = re.sub(r'(\d+)\.sdx$',"F"+str(self.save_start_index)+'_'+str(i-self.save_start_index+1)+".sdx",file_collection.file_list[i])
            print("produce "+ new_filename)
            shutil.copy(os.path.join(file_collection.src_path,file_collection.file_list[i]), os.path.join(target_path,new_filename))
            self.solve_dependency(graph,nodelist,os.path.join(file_collection.temp_path,file_collection.file_list[i]),new_file_list)
        # 保存部分的draw和Dispatch
    
        new_filename_0 = re.sub(r'(\d+)\.sdx$',"F"+str(self.save_start_index)+'_0'+".sdx", file_collection.file_list[0])
        
        
        def custom_sort(item):
            filename = item[0]
            line_number = item[1]
            name_num = re.search(r'(\d+)\.sdx$', filename)
            if name_num:
                name_num = int(name_num.group(1))
            return (name_num, line_number)

        sorted_data = sorted(new_file_list, key=custom_sort)
        unique_sorted_data = []
        seen_items = set()
        for item in sorted_data:
            item_tuple = tuple(item)
            if item_tuple not in seen_items:
                seen_items.add(item_tuple)
                unique_sorted_data.append(item)

        content_map = {}
        # 将行号按文件名分类
        for filename, line_number in unique_sorted_data:
            if filename not in content_map:
                content_map[filename] = []
            content_map[filename].append(line_number)
        # 根据分类的行号生成新的0.sdx文件内容
        with open(os.path.join(target_path,new_filename_0), 'w') as new_file:
            for filename, line_numbers in content_map.items():
                name_num = re.search(r'(\d+)\.sdx$', filename)
                if name_num:
                    name_num = int(name_num.group(1))
                # 不包括在save_start_frame之后
                if name_num>=self.save_start_index:
                    continue
                with open(os.path.join(file_collection.temp_path,filename), 'r') as original_file:
                    lines = original_file.readlines()
                    for line_num in line_numbers:
                        new_file.write(lines[line_num])
        if file_collection.dx_version==11:
            self.solve_other(graph,draw_vectors,file_collection,target_path,new_filename_0)
            self.upload_files_dx11(inject_file,target_path,new_filename_0)
        elif file_collection.dx_version==12:
            self.upload_files_dx12(inject_file,target_path,new_filename_0)

    def upload_files_dx11(self,inject_file,target_path,new_filename_0):
        # 将inject文件中的内容添加到新的sdx文件中
        path = os.path.join(os.path.dirname(os.path.dirname(inject_file.save_path)),"ReplayDump\HW")
        files = os.listdir(path)
        with open(os.path.join(inject_file.save_path,inject_file.inject_file_name), 'r') as inj, open(os.path.join(target_path,new_filename_0), 'a') as new_file:
            lines = inj.readlines()
            for line in lines:
                # 拼凑 inject文件中的每一行
                fields = line.strip().split(',')
                # 按照逗号划分，fileds[5]是上传的对象名，fields[7].split(')')[0]+是上传的文件名（包含引号），最后0是上传的第几个
                # axdUpdateSubresourcesFromFile(pCtx_0, IID_ID3D11Resource, pTex2D_155, 0, 1, "pTex2D_155_f6_l414.dds", 0);
                use_obj = fields[2].strip().split('(')[1]
                obj_name = fields[5]
                obj_name_resource = fields[7].split(')')[0]
                new_obj_name_resources = []
                index = '0'
                pattern = r'\"(.+)\.(.+)\"'
                
                match = re.search(pattern, obj_name_resource)
                if match:
                    for file in files:
                        if match.group(1) in file:
                            new_obj_name_resources.append(file)
                if len(new_obj_name_resources)>1:
                    def sort_key(f):
                        m = re.search(r'(.+)_s(\d+)\.(.+)', f)
                        if m: 
                            return (int)(m.group(2))
                    new_obj_name_resources.sort(key=sort_key)

                for i in new_obj_name_resources:
                    m = re.search(r'(.+)_s(\d+)\.(.+)', i)
                    if m is not None: 
                        # index= '0'
                        index = m.group(2)
                        # axdUpdateSubresourcesFromFile(pCtx_0, IID_ID3D11Resource, pTex2D_105, 3, 1, "pTex2D_105_F0_L47346_s3.dds", 0);
                    l ="axdUpdateSubresourcesFromFile(" + use_obj+','+fields[3]+','+obj_name+', '+index+', 1, "' + i +'", 0);\n'
                    new_file.write(l)


    def upload_files_dx12(self,inject_file,target_path,new_filename_0):
        # 将inject文件中的内容添加到新的sdx文件中
        path = os.path.join(os.path.dirname(os.path.dirname(inject_file.save_path)),"ReplayDump\HW")
        files = os.listdir(path)
    
        with open(os.path.join(inject_file.save_path,inject_file.inject_file_name), 'r') as inj, open(os.path.join(target_path,new_filename_0), 'a') as new_file:
            new_file.write("axPath(Path = \"..\ReplayDump\HW\;\");\n")
            lines = inj.readlines()
            for line in lines:
                # 拼凑 inject文件中的每一行
                # F117, L233, axdDumpResourceInCmdList(pCmdList_1, IID_ID3D12Resource, pCommitRes_23, DXGI_FORMAT_UNKNOWN,1, "pCommitRes_23_F117_L233_s1.dds");
                fields = line.strip().split(',')
                use_obj = fields[2].strip().split('(')[1]
                obj_name = fields[4]
                subresource = int(fields[6])
                obj_name_resource = fields[7].split(')')[0]
                new_obj_name_resources = []
                
                pattern = r'\"(.+)\.(.+)\"'
                match = re.search(pattern, obj_name_resource)
                if match:
                    for file in files:
                        if match.group(1)+"_" in file:
                            new_obj_name_resources.append(file)


                
                # axdUpdateSubresourcesFromFile(pCmdQue_1, IID_ID3D12Resource, pCommitRes_29, 6, 1, "pCommitRes_29_f121_l2358_s6_submit_F200_L9493.dds", 0);
                if(new_obj_name_resources!=[]):
                    l ="axdUpdateSubresourcesFromFile(" + "pCmdQue_1"+','+fields[3]+','+obj_name+', '+fields[6] + ', 1, "' + new_obj_name_resources[0] +'", 0);\n'
                    new_file.write(l)
            new_file.write("ID3D12CommandList* ppCmdList_trim[1] = (pCmdList_14);\n")
            new_file.write("pCmdQue_1->ExecuteCommandLists(NumCommandLists = 1, ppCommandLists = ppCmdList_trim);\n")
        
