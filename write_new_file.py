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
# 解决文件filename的依赖，把依赖保存到new_file_list中

def solve_line_dependency(filename,line_pos,line,graph,new_file_list):
    
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


def solve_dependency(graph,nodelists,filename,new_file_list):
    with open(filename, 'r') as f:
        line_pos = 0
        for line in f:
            solve_line_dependency(filename,line_pos,line,graph,new_file_list)
            # 如果这行引用到了其他文件的变量，则去graph寻找            
            line_pos = line_pos+1
    for i in nodelists.nodes:
        for node in nodelists.nodes[i]: 
            new_file_list.append(node.line_pos)
            graph.dfs(node.id,new_file_list)


def solve_other(graph,drawvector,new_file_list,start_draw_index):
    # 把drawvector中pivote后面的new_file_list中
    for i in drawvector.get_target_drawvector(start_draw_index):
        with open(i[0][0], 'r') as f:
            lines = f.readlines()
            for j in range(i[0][1],i[1][1]+1):
                new_file_list.append([i[0][0],j])
                # 解决于lines[j]有关的依赖
                
                solve_line_dependency(i[0][0],j,lines[j],graph,new_file_list)



def create_new_sdx_file(new_file_list,save_start_index,new_filename):
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
            # 不包括在save_start_frame之后
            if name_num>=save_start_index:
                continue
            with open(filename, 'r') as original_file:
                lines = original_file.readlines()
                for line_num in line_numbers:
                    new_file.write(lines[line_num])

        
def simplify_frames(graph,nodelist,drawvector,src_path,target_path,save_start_index,save_end_index,start_draw_index):
    """
    从save_start_index开始保存，到save_end_index结束，
    """
    filenames = os.listdir(src_path)
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
    
    new_file_list = [] # 保存文件行所在位置
    for filename in filenames:
        name_num = re.search(r'(\d+)\.sdx$', filename)
        if name_num:
            name_num = int(name_num.group(1))
        if name_num==0:
            with open(src_path+filename, 'r') as f:
                line_pos = 0
                for line in f.readlines():
                    new_file_list.append([src_path+filename,line_pos])            
                    line_pos = line_pos+1
            
        if save_start_index<=name_num<=save_end_index:
            new_filename = re.sub(r'(\d+)\.sdx$',str(name_num-save_start_index+1)+".sdx", filename)
            print("produce "+ new_filename)
            shutil.copy(src_path+filename, target_path+new_filename)
            solve_dependency(graph,nodelist,src_path+filename,new_file_list)
            
    solve_other(graph,drawvector,new_file_list,start_draw_index)
    create_new_sdx_file(new_file_list,save_start_index,target_path+filenames[0])
      
