from tool_function import *
from graph import *
import re
import copy
# 使用解析好的资源构建链表或者图
# 首先是设计图的节点类的结构，然后是边的关系，最后是图的结构
# 读取一个文件，解析每一行，判断每一行语句的种类，然后进行处理
# 1. 读取文件
# 2. 解析每一行
# 3. 判断语句种类
# 4. 处理语句

def read_to_graph(filename,graph,nodelists,mapstack):
    line_pos = 0
    with open(filename, "r") as f:
        for line in f:
            if is_comment(line):
                pass
            elif is_empty(line):
                pass
            elif is_other(line):
                res = parse_statement(line) # 里面可能会有None,axCreateWindow(x = 0, y = 0, w = 1920, h = 1080, depth = 0, xvis = NULL, cfg = NULL)=win_1;
                try:
                    # res[1]是变量名，res[3]是变量值
                    # res[3]这个变量值可能引用到了其他变量，所以需要进行解析
                    node = Node(res[1],[filename,line_pos])
                    graph.add_vertex(node)
                    # res[3]引用的都是(a,b,c)这种，里面没有括号，有括号的没有引用
                    # 姑且认为包括括号的都没有引用其他变量   
                    if "=" in res[3]:
                        pass
                    else:
                        val_list = res[3].split(",")
                        val_list = [val.strip() for val in val_list]
                        for val in val_list:
                            if(is_macro(val)): # 去除空格
                                pass
                            elif(is_decimal_or_hex(val)):
                                pass
                            elif(is_valid_variable(val)):
                                val_node = Node(val,[filename,line_pos])
                                graph.add_edge(node,val_node)
                    
                except:
                    node = Node("NULL",[filename,line_pos])
                    nodelists.add_node(node)
            elif is_object_func_call(line):
                
                res = parse_object_func_call(line) # 解析对象调用
                if res[1] in device_func:
                    # 如果在创建函数中，会根据已有的资源创建一个对象，然后连接起他们
                    ext_node_list = [] # 已经存在的节点
                    dontext_node_list = [] # 不存在的节点
                    for i in res[2]:
                        p_v = parse_func_assignment(i) #parameters and values
                        if(is_macro(p_v[1])):
                            pass
                        elif(is_decimal_or_hex(p_v[1])):
                            pass
                        elif(is_valid_variable(p_v[1])):
                            # 如果是一个合法的变量，那么就是一个资源，创建一个资源节点
                            node = Node(p_v[1],[filename,line_pos])
                            if not graph.has_vertex(node):
                                graph.add_vertex(node)
                                dontext_node_list.append(node)
                            else:
                                ext_node_list.append(node)
                    # 将存在的与不存在的进行连接
                    for ex in ext_node_list:
                        for dont in dontext_node_list:
                            # 比如用pBuf_13创建了pBuf0_14，最后文件中pBuf_14依赖于pBuf_13，
                            # 访问pBuf_14的时候，需要去访问pBuf_13，所以是pBuf_14->pBuf_13
                            graph.add_edge(dont,ex)
                    
                elif res[1] in map_func:    
                    # TODO: map和unmap必须成对存在，他们的特点是第一个resource一样
                    # 他们最后都需要连接到创建的资源上
                    if res[1] =="Map":
                        ext_node_list = [] # 已经存在的节点，其实只有一个
                        dontext_node_list = [] # 不存在的节点，也只有以一个
                        for i in res[2]:
                            p_v = parse_func_assignment(i) #parameters and values
                            if(is_macro(p_v[1])):
                                pass
                            elif(is_decimal_or_hex(p_v[1])):
                                pass
                            elif(is_valid_variable(p_v[1])):
                                # map的资源不需要加入到vertex中
                                node = Node(p_v[1],[filename,line_pos])
                                if not graph.has_vertex(node):
                                    graph.add_vertex(node)
                                    dontext_node_list.append(node)
                                else:
                                    ext_node_list.append(node)
                        mapstack.push((ext_node_list[0],dontext_node_list[0]))
                    elif res[1]=="Unmap":
                        p_v = parse_func_assignment(res[2][0])
                        if(is_macro(p_v[1])):
                            pass
                        elif(is_decimal_or_hex(p_v[1])):
                            pass
                        elif(is_valid_variable(p_v[1])):
                             
                            if mapstack.top()[0].id == p_v[1]:
                                node = Node(p_v[1],[filename,line_pos])
                                graph.add_edge(mapstack.top()[1],mapstack.top()[0])
                                graph.add_edge(mapstack.top()[1],node)
                               
                                mapstack.pop()

                elif res[1] in must_add:
                    node = Node(res[1],[filename,line_pos])
                    nodelists.add_node(node)

                elif res[1] in other_func:
                    pass
            elif is_func_call(line):
                res = parse_func_call(line)
                if(res[0] in map_func):
                    node = Node(parse_func_assignment(res[1][1])[1],[filename,line_pos])
                    graph.add_vertex(node)
                elif(res[0] in must_add):
                    node = Node(res[1][0],[filename,line_pos])
                    graph.add_vertex(node)
                    nodelists.add_node(node)
                elif(res[0] in other_func):
                    pass


            line_pos = line_pos+1
    


def read_to_draw_vector(filename,drawvector):
    line_pos = 0
    start_pos = [filename, line_pos]
    end_pos = []
    with open(filename, "r") as f:
        for line in f:
            if is_comment(line):
                pass
            elif is_empty(line):
                pass
            elif is_object_func_call(line):
                if "pDev11_0->CreateRenderTargetView(pResource = pSwap_0_buf_0, pDesc = rtv"  in line :
                    drawvector.add_pivote([filename, line_pos])
                ## 判断是不是Draw()
                res = parse_object_func_call(line)
                if res[1] in draw_stage_func:
                    end_pos = [filename, line_pos]
                    drawvector.add_draw(res[1],start_pos,end_pos)
                    start_pos = [filename, line_pos+1]
                
            line_pos = line_pos+1

def generate_inject_file(filename,inject_file,graph):
    with open(filename, "r") as f, open(inject_file, "a") as inj:
        index = 0
        start_pos = [filename, index]
        lines = f.readlines()
        for line in lines:
            if is_comment(line):
                pass
            elif is_empty(line):
                pass
            elif is_object_func_call(line):
                res = parse_object_func_call(line)
                if res[1] in copy_func: # 设置成空，已经不起作用了
                    # 根据copy的资源，判断是否需要注入
                    file_pos = 'F'+ re.search(r'(\d+)\.sdx$', filename).group(1)
                    line_pose = 'L'+ str(index)
                    function= 'axdDumpResource('+res[0] + ', IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN'
                    p_v = parse_func_assignment(res[2][0]) #parameters and values
                    if(is_macro(p_v[1])):
                        pass
                    elif(is_decimal_or_hex(p_v[1])):
                        pass
                    elif(is_valid_variable(p_v[1])):
                        resource = p_v[1]
                    argumets = resource
                    # TODO:需要判断注入那种类型的资源，dds还是bin
                    save_type = ".bin"
                    if(resource[0:3] != "pBu" ):
                        save_type = ".dds"
                    new_resoure = "\"" + resource+ "_"+ file_pos + "_"+ line_pose + save_type +"\");\n"
                    inj.write(file_pos+', ' + line_pose+', ' + function+', ' + argumets+', 0, ' + new_resoure)

                elif res[1] in draw_stage_func:
                    end_pos = [filename, index]
                    #print("dasda",start_pos[0],start_pos[1],end_pos[1])
                    # start pos 和end pos之间分析
                    # 如果是Draw，那么就注入
                    
                    idx = start_pos[1]
                    for l in lines[start_pos[1]:end_pos[1]]:
                        idx = idx+1
                        if is_comment(l):
                            pass
                        elif is_empty(l):
                            pass
                        elif is_other(l):
                            # 形如ID3D11Buffer* ppBuf_18533[0x3] = (pBuf_3, pBuf_4, pBuf_3);
                            ret = parse_statement(l)
                             # 里面可能会有None,axCreateWindow(x = 0, y = 0, w = 1920, h = 1080, depth = 0, xvis = NULL, cfg = NULL)=win_1;
                            try:
                                # res[1]是变量名，res[3]是变量值
                                # res[3]这个变量值可能引用到了其他变量，所以需要进行解析
                                # res[3]引用的都是(a,b,c)这种，里面没有括号，有括号的没有引用
                                # 姑且认为包括括号的都没有引用其他变量   
                                if "=" in ret[3]:
                                    #axCreateWindow(x = 0, y = 0, w = 1920, h = 1080, depth = 0, xvis = NULL, cfg = NULL)=win_1;这种
                                    pass
                                else:
                                    val_list = ret[3].split(",")
                                    val_list = [val.strip() for val in val_list]
                                    
                                   
                                    for val in val_list:
                                        if(is_macro(val)):
                                            pass
                                            ref_list.append(val)
                                        elif(is_decimal_or_hex(val)):
                                            pass
                                            ref_list.append(val)
                                        elif(is_valid_variable(val)):

                                            
                                            # 如果出现了合法的变量，那么认为整个val_list都是资源
                                            # 现在可以把val_list中的资源当成一个整体dump下来
                                            ref_list = []
                                            graph.get_leaf(val,ref_list) # 获取了val的所在路径所有变量
                                            for ref  in ref_list:
                                                file_pos = 'F'+ re.search(r'(\d+)\.sdx$', filename).group(1)
                                                # line_pose = 'L'+ str(idx)
                                                line_pose = 'L'+str(len(lines)-1)
                                                function= 'axdDumpResource('+res[0] + ', IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN'
                                                argumets = ref
                                                save_type = ".bin"
                                                if(ref_list[0][0:4] != "pBuf"):
                                                    save_type = ".dds"
                                                new_resoure = "\"" + ref_list[0]+ "_"+  file_pos + "_"+ line_pose + save_type +"\");\n"
                                                inj.write(file_pos+', ' + line_pose+', ' + function+', ' + argumets+', 0, ' + new_resoure)                            
                            except:
                                pass
                        elif is_object_func_call(l):
                            ret = parse_object_func_call(l) # 解析对象调用
                            if ret[1] in device_func:
                                # 如果是Create类的话，不用管，后面解决依赖会处理
                                pass
                            
                            elif ret[1] in obj_set_func:
                                for i in ret[2]:
                                    p_v = parse_func_assignment(i) #parameters and values
                                    if(is_macro(p_v[1])):
                                        pass
                                    elif(is_decimal_or_hex(p_v[1])):
                                        pass
                                    elif(is_valid_variable(p_v[1])):
                                        ref_list = []
                                        graph.get_leaf(p_v[1],ref_list)
                                        #ref_list.append(val)   
                                        # 现在有了一个dispatch所有引用的buffer，是否应该写一个dump函数，然后注入
                                        # 处理 ref_list，去重，然后去graph中寻找
                                        ref_list = list(set(ref_list))
                                        for ref in ref_list:
                                            file_pos = 'F'+ re.search(r'(\d+)\.sdx$', filename).group(1)
                                            # line_pose = 'L'+ str(idx)
                                            line_pose = 'L'+str(len(lines)-1)
                                            function= 'axdDumpResource('+res[0] + ', IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN'
                                            argumets = ref
                                            # TODO:需要判断注入那种类型的资源，dds还是bin
                                            save_type = ".bin"
                                            if(ref[0:3] != "pBu"):
                                                save_type = ".dds"
                                            new_resoure = "\"" + ref+ "_"+  file_pos + "_"+ line_pose + save_type +"\");\n"

                                            inj.write(file_pos+', ' + line_pose+', ' + function+', ' + argumets+', 0, ' + new_resoure)       
                                            

                            elif ret[1] in map_func:
                                #map 和之前的device create一样
                                pass
                            elif ret[1] in must_add:
                                pass
                            elif ret[1] in other_func:
                                pass
                        elif is_func_call(l):
                            pass
                    
                    start_pos[1] = index+1
            
            index = index+1

    
def generate_final_inject_file(orgin_inject_file,final_inject_file,save_start_index):
# 去除掉含有相同resource的lines
    # 在begin_frame 之前的resource dump下来，最近的，以前重复的不要
    with open(orgin_inject_file, 'r') as org_inj:
        lines = org_inj.readlines()

    # 读取到内存中删去重复的
    data = {}
    for line in lines:
        fields = line.strip().split(',')
        if len(fields) >= 6 and int(fields[0][1:])<save_start_index:
            key = fields[5]
            # if key not in data:
            data[key] = line
            # else:
            #     old_field = data[key].strip().split(',')
            #     new_field = line.strip().split(',')
            #     if int(old_field[1][2:])<int(new_field[1][2:]):
            #         data[key] = line



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
    with open(final_inject_file, 'w') as fin_inj:
        for l in lines:
            fin_inj.write(l)        