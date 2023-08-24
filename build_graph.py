from tool_function import *
from graph import *

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
                res = parse_statement(line) # 里面又None
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
                if res[1] in obj_create_func:
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

                elif res[1] in obj_single_set_func:
                    # TODO: 这类set只作用于一个变量
                    for i in res[2]:
                        p_v = parse_func_assignment(i) #parameters and values
                        if(is_macro(p_v[1])):
                            pass
                        elif(is_decimal_or_hex(p_v[1])):
                            pass
                        elif(is_valid_variable(p_v[1])):
                            node = Node(p_v[1],[filename,line_pos])
                            graph.add_vertex(node)
                            
                elif res[1] in obj_multi_set_func:
                    # TODO: 这类set作用于多个变量,需要将他们连接起来
                    node_list = []
                    for i in res[2]:
                        p_v = parse_func_assignment(i) #parameters and values
                        if(is_macro(p_v[1])):
                            pass
                        elif(is_decimal_or_hex(p_v[1])):
                            pass
                        elif(is_valid_variable(p_v[1])):
                            node = Node(p_v[1],[filename,line_pos])
                            node_list.append(node)
                            graph.add_vertex(node)
                    for i in range(len(node_list)-1):
                        for j in range(i,len(node_list)-1):
                            graph.add_edge(node_list[i],node_list[j])
                            graph.add_edge(node_list[j],node_list[i])

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
                    node = Node("MUST",[filename,line_pos])
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
                else:
                    node = Node("NULL_1",[filename,line_pos])
                    nodelists.add_node(node)    
            line_pos = line_pos+1


