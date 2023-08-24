import re
from tool_function import *
from graph import *
import shutil
# 现在是做帧的简化步骤，要求是从第i帧到第j帧，从某个文件开始到某个文件结束，比如截取58到60帧，从文件序号59开始，到文件序号61结束
# 然后组成新的文件

# 1. 读取文件夹下的所有文件，然后按照文件名排序，然后按照文件名的数字排序
# 2. 先用所有的文件构成一个图，

# 建图后该怎么进行重构，
# 先试着截取1帧

def solve_dependency(filename,graph,nodelists,new_file_list):
    with open(filename, 'r') as f:
        line_pos = 0
        for line in f:
            if is_comment(line):
                pass
            elif is_empty(line):
                pass
            elif is_other(line):
                new_file_list.append([filename,line_pos])
                res = parse_statement(line)
                p_v = map(str.strip, res[3].split(","))
                for i in p_v:
                    # 第一个是类型，第二个是变量名称，第三个是数组，第四个才是依赖
                    if( is_decimal_or_hex(i)):
                        pass
                    elif(is_macro(i)):
                        pass
                    elif(is_valid_variable(i)):
                        # 当是合法的变量时候，应该去以res[i]去深度遍历所有依赖的节点。
                        dependency_node = [] 
                        graph.dfs(i,dependency_node)
                        new_file_list.extend(dependency_node)
                    else:
                        pass
            elif is_object_func_call(line):
                new_file_list.append([filename,line_pos])
                res = parse_object_func_call(line)
                # 对象->函数(参数)
                for i in res[2]:
                    p_v = parse_func_assignment(i)
                    if(is_macro(p_v[1])):
                        pass
                    elif(is_decimal_or_hex(p_v[1])):
                        pass
                    elif(is_valid_variable(p_v[1])):
                        dependency_node = [] 
                        graph.dfs(p_v[1],dependency_node)
                        new_file_list.extend(dependency_node)
            elif is_func_call(line):
                new_file_list.append([filename,line_pos])
            # 如果这行引用到了其他文件的变量，则去graph寻找            
            line_pos = line_pos+1
    for node in nodelists.nodes["MUST"]:
        new_file_list.append(node.line_pos)
    

def create_new_sdx_file(new_file_list,frame_index,new_filename):
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

    # 根据分类的行号生成新的sdx文件内容
    with open(new_filename, 'w') as new_file:
        for filename, line_numbers in content_map.items():
            # 指定文件不参与生成
            name_num = re.search(r'(\d+)\.sdx$', filename)
            if name_num:
                name_num = int(name_num.group(1))
            ## 不包括>frame_index的文件
            if name_num==0 or name_num>frame_index:
                continue
            with open(filename, 'r') as original_file:
                lines = original_file.readlines()
            for line_num in line_numbers:
                new_file.write(lines[line_num])

        
def simplify_one_frame(graph,nodelist,src_folder_path,targe_frame_index,des_folder_path):
    filenames = os.listdir(src_folder_path)
    source_files =[]
    for filename in filenames:
        if "_0" in filename:
            source_files.append(filename)
            
        if "_"+str(targe_frame_index) in filename:
            source_files.append(filename)
    
    shutil.copy(src_folder_path+source_files[0], des_folder_path+source_files[0])
    new_file_list = [] # 保存文件行所在位置

    solve_dependency(src_folder_path+source_files[1],graph,nodelist,new_file_list)
    create_new_sdx_file(new_file_list,targe_frame_index,des_folder_path+source_files[1].replace(str(targe_frame_index),str(1)))
    shutil.copy(src_folder_path+source_files[1], des_folder_path+source_files[1].replace(str(targe_frame_index),str(2)))
      
