from tool_function import *
from graph import *
import re
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
            # if "pBuf_609" in line:
            #     print(line,line_pos)
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

                elif res[1] in obj_set_func:
                    # TODO: 这类set只作用于一个变量
                    pass
                    for i in res[2]:
                        p_v = parse_func_assignment(i) #parameters and values
                        if(is_macro(p_v[1])):
                            pass
                        elif(is_decimal_or_hex(p_v[1])):
                            pass
                        elif(is_valid_variable(p_v[1])):
                            pass
                            node = Node(p_v[1],[filename,line_pos])
                            # graph.add_vertex(node)
                            
                elif res[1] in obj_set_func:
                    pass
                    # TODO: 这类set作用于多个变量,需要将他们连接起来
                    # node_list = []
                    for i in res[2]:
                    
                        p_v = parse_func_assignment(i) #parameters and values
                        if(is_macro(p_v[1])):
                            pass
                        elif(is_decimal_or_hex(p_v[1])):
                            pass
                        elif(is_valid_variable(p_v[1])):
                            pass
                            node = Node(p_v[1],[filename,line_pos])
                            # graph.add_vertex(node)
                            # node_list.append(node)
                    

                    # for i in range(0,len(node_list)):
                    #     for j in range(i+1,len(node_list)):
                    #         graph.add_edge(node_list[i],node_list[j])
                    #         graph.add_edge(node_list[j],node_list[i])
                    

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
                    # TODO：如果在其他的函数中，保证加入到图中
                    # print("here",res[1]) get_bufer
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

def generate_inject_file(filename,inject_file):
    with open(filename, "r") as f, open(inject_file, "a") as inj:
        index = 0
        start_pos = [filename, index]
        end_pos = []
        for line in f:
            if is_comment(line):
                pass
            elif is_empty(line):
                pass
            elif is_object_func_call(line):
                res = parse_object_func_call(line)
                if res[1] in copy_func:
                    # 根据copy的资源，判断是否需要注入
                    file_pos = 'F'+ re.search(r'(\d+)\.sdx$', filename).group(1)
                    line_pose = 'L'+ str(index)
                    function= 'axDumpResource('+res[0] + ', IID_ID3D11Resource, DXGI_FORMAT_UNKNOW'
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
                    if(resource[0:3] != "pBu"):
                        save_type = ".dds"
                    new_resoure = "\"" + resource+ "_"+ file_pos + "_"+ line_pose + save_type +"\")\n"
                    inj.write(file_pos+', ' + line_pose+', ' + function+', ' + argumets+', 0, ' + new_resoure)
                elif res[1] in draw_stage_func:
                    end_pos = [filename, index]
                    # start pos 和end pos之间分析
                    # 如果是Draw，那么就注入
                    lines = f.readlines()[start_pos[1],end_pos[1]]
                    # 分析这段的lines，看看有没有注入的必要
                    for line in lines:
                        

                    start_pos = [filename, index+1]

            # TODO: 还有一类dispatch需要inject的
            # 从何处开始，从何处结束，如果两个dispacth的树子节点相同，可以合并他们，dump出他们的buffer
            # 每一个dispatch dump下来，然后再合并
            index = index+1
    