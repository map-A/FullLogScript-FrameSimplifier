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
        try:
            p_v = map(str.strip, res[3].split(","))
            for i in p_v:
                # 第一个是类型，第二个是变量名称，第三个是数组，第四个才是依赖
                if(is_decimal_or_hex(i)):
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
        except:
            new_file_list.append([filename,line_pos])
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
            if(i in must_add): # 保证添加一次
                break;


def solve_other(graph,drawvector,new_file_list,scene_begins_index,offset):
    # 把drawvector中pivote后面的new_file_list中
    # 把dispatch 添加到new_file_list中
    # 忽略所有的drawindex

    for i in drawvector.get_draw_vector("DrawIndexedInstanced"):
        with open(i[0][0], 'r') as f:
            lines = f.readlines()
            for j in range(i[0][1],i[1][1]+1):
                new_file_list.append([i[0][0],j])
                # 解决于lines[j]有关的依赖
                solve_line_dependency(i[0][0],j,lines[j],graph,new_file_list)



    # 保存部分的draw
    # for i in drawvector.get_target_drawvector(scene_begins_index,offset):
    #     with open(i[0][0], 'r') as f:
    #         lines = f.readlines()
    #         for j in range(i[0][1],i[1][1]+1):
    #             new_file_list.append([i[0][0],j])
    #             # 解决于lines[j]有关的依赖
    #             solve_line_dependency(i[0][0],j,lines[j],graph,new_file_list)



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

        
def simplify_frames(graph,nodelist,drawvector,origin_path,src_path,target_path,scene_begins_index,save_start_index,save_end_index,offset):
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
                    if line_pos<4 or "swapDesc" in line or "Present" in line: #前4行必须保留
                        new_file_list.append([src_path+filename,line_pos])
                    line_pos = line_pos+1

          
        if save_start_index<=name_num<=save_end_index:
            new_filename = re.sub(r'(\d+)\.sdx$',"F"+str(save_start_index)+'_'+str(name_num-save_start_index+1)+".sdx", filename)
            print("produce "+ new_filename)
            shutil.copy(origin_path+filename, target_path+new_filename)
            solve_dependency(graph,nodelist,src_path+filename,new_file_list) 

    # 保存部分的draw和Dispatch     
    # solve_other(graph,drawvector,new_file_list,scene_begins_index,offset)
    new_filename_0 = re.sub(r'(\d+)\.sdx$',"F"+str(save_start_index)+'_0'+".sdx", filenames[0])
    create_new_sdx_file(new_file_list,save_start_index,target_path+new_filename_0)


    # 删除子文件夹和文件
    # for f in os.listdir(src_path):
    #     full_path = os.path.join(src_path, f)
    #     if os.path.isfile(full_path):
    #         os.remove(full_path)
    #     elif os.path.isdir(full_path):
    #         shutil.rmtree(full_path)
    # shutil.rmtree(src_path)
      


def upload_files(tmp_path,target_path,new_filename_0,inject_file):
    # 将inject文件中的内容添加到新的sdx文件中
    path = "D:\\work\\3DMark_FireStrike-Extreme-orgSize-FixFPS0.5-GT2\\ReplayDump\HW\\"
    files = os.listdir(path)
    with open(tmp_path+inject_file, 'r') as inj, open(target_path+new_filename_0, 'a') as new_file:
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
            # print(l)
                new_file.write(l)