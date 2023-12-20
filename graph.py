from line_util import *
from dx11_config import *
from dx12_config import *
import os

class Node():
    def __init__(self, id, line_pos,line,line_type):
        self.id = id # 资源名称,如果是crete，那么就是变量名称，如果是函数调用，那么就是函数名称，如果是对象调用，那么就是对象名称
        self.line_pos = line_pos # 资源所在位置
        self.line = line # 资源行的原样
        self.resource_list = []
        self.line_type = line_type # 资源类型

    def print(self):
        print(self.id, self.line_pos,self.line)

## 应该建立有向图，每个节点是一个资源，每个边是一个资源的依赖关系
class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    # 判断是否存在该节点
    def has_vertex(self, node_id):
        if self.vertices.get(node_id) is  not None:
            return True
        return False
    
    def has_edge(self, vertex1, vertex2):
        if self.edges.get(vertex1.id) is not None and vertex2 in self.edges[vertex1.id]:
            return True
        return False
    
    def get_node(self,node_id):
        # 根据id 获取图中属性为id的所有位置
        if self.vertices.get(node_id) is not None:
            return self.vertices[node_id]
        return []
    
    def get_neighbors(self, node_id):
        # 获取node_id的邻居节点
        if self.edges.get(node_id) is not None:
            return self.edges[node_id]
        return []

    def add_vertex(self, node):
        if node.id not in self.vertices:
            self.vertices[node.id] = []
        self.vertices[node.id].append(node)
        if self.edges.get(node.id) is None:
            self.edges[node.id] = [] # 为了防止出现没有邻居节点的情况，所以这里先初始化
        self.edges[node.id].append(node)
        


    def add_edge(self, vertex1, vertex2):
        # vertex1.id -> vertex2
        # if self.has_vertex(vertex1.id) and self.has_vertex(vertex2.id):
        if self.edges.get(vertex1.id) is None:
            self.edges[vertex1.id] = []
        self.edges[vertex1.id].append(vertex2)

    
    def print(self):
        self.print_vertices()
        self.print_edges()

    def print_vertices(self):
        for key in self.vertices:
            for node in self.vertices[key]:
                node.print()
    def print_edges(self):
        for key in self.edges:
            print(key, "->",self.edges[key],)

    def dfs(self,node_id,res):
        #从属性值为node_id的开始深度遍历，遍历的结果存到res数组中
        stack = [node_id]
        visited = set()
        while stack:  
            cur = stack.pop()
            if cur not in visited:
                visited.add(cur)
                neibo = self.get_neighbors(cur)
                
                if neibo:

                    for nxt in neibo:
                        res.append(nxt.line_pos)
                        if nxt.id not in visited:
                            stack.append(nxt.id)
        

    def get_leaf(self,nodeid,res):
        # 获取nodeid的叶子节点
        temp = []
        stack = [nodeid]
        visited = set()
        while stack:
            cur = stack.pop()
            temp.append(cur)
            if cur not in visited:
                visited.add(cur)
                neibo = self.get_neighbors(cur)
                if neibo:
                    for nxt in neibo:
                        if nxt.id not in visited:
                            stack.append(nxt.id)
        # for i in temp:
        #     if i[0:4]=="pBuf" or i[0:4]=="pTex" or i == "pSwap_0_buf_0" or i[0:4]=="pSRV" or i[0:4]=="pUAV"  or i[0:4]=="RTV" or i[0:4]=="DSV": 
        #         res.append(i)
        res.extend(temp)


    def add_other_line_to_graph(self,pos,line):
        """
        将其他类型的语句加入到图中
        :param pos: 位置
        :param graph: 图
        :return: None
        """
        
        resource_list = get_resource_from_line(line)
        # node_list = [Node(res,pos,line,is_var_statement.__str__) for res in resource_list]
        ext_node_list = [] # 已经存在的节点
        dontext_node_list = [] # 不存在的节点
        for i in resource_list:
            node = Node(i,pos,line,is_object_func_call.__str__)
            if not self.has_vertex(node.id):
                self.add_vertex(node)
                dontext_node_list.append(node)
            else:
                ext_node_list.append(node)
        for ex in ext_node_list:
            for dont in dontext_node_list:
                self.add_edge(dont,ex)


    def add_object_func_call_to_graph(self,pos,line,nodelists,mapstack,dx_version):
        device_func = dx11_device_func
        res = parse_object_func_call(line) # 解析对象调用
        if dx_version==12:
            device_func = dx12_device_func

        if res[1] in must_add_func_12 and dx_version==12:
            resource_list = get_resource_from_line(line) # 获取资源列表
            # 如果在创建函数中，会根据已有的资源创建一个对象，然后连接起他们
            ext_node_list = [] # 已经存在的节点
            dontext_node_list = [] # 不存在的节点
            for i in resource_list:
                node = Node(i,pos,line,is_object_func_call.__str__)
                nodelists.add_node(node)
                if not self.has_vertex(node.id):
                    self.add_vertex(node)
                    dontext_node_list.append(node)
                else:
                    ext_node_list.append(node)
            for ex in ext_node_list:
                for dont in dontext_node_list:
                    self.add_edge(dont,ex)

        
   

        elif res[1] in device_func:
            resource_list = get_resource_from_line(line) # 获取资源列表
            # 如果在创建函数中，会根据已有的资源创建一个对象，然后连接起他们
            ext_node_list = [] # 已经存在的节点
            dontext_node_list = [] # 不存在的节点
            
            for i in resource_list:
                node = Node(i,pos,line,is_object_func_call.__str__)
                nodelists.add_node(node)
                if not self.has_vertex(node.id):
                    self.add_vertex(node)
                    dontext_node_list.append(node)
                else:
                    ext_node_list.append(node)
            for ex in ext_node_list:
                for dont in dontext_node_list:
                    self.add_edge(dont,ex)
        elif res[1] in dx12_device_func2 and dx_version==12: 
            # CreateUnorderedAccessView 这类api资源已经创建了，但是还没有加入到图中，所以这里需要加入到图中
            resource_list = get_resource_from_line(line)
            # # 默认最后一个是不存在的资源
            node_list = [Node(res,pos,line,is_object_func_call.__str__) for res in resource_list]
            ext_node_list = [i for i in node_list[:-1]] # 已经存在的节点
            dontext_node_list = [node_list[-1]] # 不存在的节点
            
            self.add_vertex(node_list[-1])
            # if self.has_vertex(node_list[-1].id):
            #     a = self.get_neighbors(node_list[-1].id)
            #     for i in a:
            #         i.print()
            for ex in ext_node_list:
                for dont in dontext_node_list:
                    # if resource_list[-1]=="pDescHeap_5_cpuH":
                    #     print("pDescHeap_5_cpuH",ex.id,dont.id)
                    self.add_edge(dont,ex)
            # if resource_list[-1]=="pDescHeap_5_cpuH":
            #     a = self.get_neighbors("pDescHeap_5_cpuH")
            #     for i in a:
            #         i.print()

            
            
        elif dx_version ==12 and res[1] in commitRes_obj_func:    
            # dx12的map和unmap 默认添加
            resource_list = get_resource_from_line(line)
            if res[1] =="Map":
                ext_node_list = [] 
                dontext_node_list = []
                for i in resource_list:
                    node = Node(i,pos,line,is_object_func_call.__str__)
                    if not self.has_vertex(node.id):
                        self.add_vertex(node)
                        dontext_node_list.append(node)
                    else:
                        ext_node_list.append(node)
                for ex in ext_node_list:
                    for dont in dontext_node_list:
                        self.add_edge(dont,ex)

                nodelists.add_node(dontext_node_list[0])
            #     mapstack.push(ext_node_list[0])
            # elif res[1]=="Unmap":
            #     resource_list = get_resource_from_line(line)
            #     print(line)
            #     print("map and unmap",mapstack.top().id,resource_list[0])
            #     if mapstack.top()[0].id == resource_list[0]: # dx12 的resource 只有一个
            #         node = Node(resource_list[0],pos,line,is_object_func_call.__str__)
            #         nodelists.add_node(node)
                    
            #         mapstack.pop()
        elif res[1] in pCmdList_set_func and dx_version==12:
            resource_list = get_resource_from_line(line) # 获取资源列表
            for i in resource_list:
                node = Node(i,pos,line,is_object_func_call.__str__)
                nodelists.add_node(node)
        
        


    def add_func_call_to_graph(self,pos,line,dx_version):
        func_table = func_set
        res = parse_func_call(line) # 解析对象调用
        if res is not None and res[0] in func_table:
            resource_list = get_resource_from_line(line) # 获取资源列表
            # 如果在创建函数中，会根据已有的资源创建一个对象，然后连接起他们
            ext_node_list = [] # 已经存在的节点
            dontext_node_list = [] # 不存在的节点
            for i in resource_list:
                node = Node(i,pos,line,is_object_func_call.__str__)
                if not self.has_vertex(node.id):
                    self.add_vertex(node)
                    dontext_node_list.append(node)
                else:
                    ext_node_list.append(node)


            for ex in ext_node_list:
                for dont in dontext_node_list:
                    # 比如用pBuf_13创建了pBuf0_14，最后文件中pBuf_14依赖于pBuf_13，访问pBuf_14的时候，需要去访问pBuf_13，所以是pBuf_14->pBuf_13
                    self.add_edge(dont,ex)
    
    def add_func_asigment_to_graph(self,pos,line):
            
        resource_list = get_resource_from_line(line)
        
        ext_node_list = [] # 已经存在的节点
        dontext_node_list = [] # 不存在的节点
        for i in resource_list:
            node = Node(i,pos,line,is_func_asigment.__str__)
            if not self.has_vertex(node.id):
                self.add_vertex(node)
                dontext_node_list.append(node)
            else:
                ext_node_list.append(node)         

        for ex in ext_node_list:
            for dont in dontext_node_list:
                
                self.add_edge(dont,ex)



    def read_dx11_to_graph(self,file_collection,nodelists,mapstack):
        for filename in file_collection.file_list:
            line_pos = 0
            with open(os.path.join(file_collection.temp_path,filename), "r") as f:
                for line in f:
                    if is_var_statement(line):
                        self.add_other_line_to_graph([filename,line_pos],line)

                    elif is_object_func_call(line):
                        self.add_object_func_call_to_graph([filename,line_pos],line,nodelists,mapstack,file_collection.dx_version)

                    elif is_func_call(line):
                        res = parse_func_call(line)
                        if(res[0] in map_func):
                            node = Node(parse_func_assignment(res[1][1])[1],[filename,line_pos],line,is_func_call.__str__)
                            self.add_vertex(node)
                        elif(res[0] in must_add):
                            node = Node(res[1][0],[filename,line_pos],line,is_func_call.__str__)
                            self.add_vertex(node)
                            nodelists.add_node(node)
                        elif(res[0] in other_func):
                            pass
                    elif is_func_asigment(line):
                        self.add_func_asigment_to_graph([filename,line_pos],line)
                    
                    line_pos = line_pos+1

    def read_dx12_to_graph(self,file_collection,nodelists,mapstack):
        for filename in file_collection.file_list:
            line_pos = 0
            with open(os.path.join(file_collection.temp_path,filename), "r") as f:
                for line in f:
                    if is_var_statement(line):
                        self.add_other_line_to_graph([filename,line_pos],line)

                    elif is_object_func_call(line):
                        
                    #    axdAddCpuDescriptorHandle(pDescHeap_2, 1)=pDescHeap_2_cpuH_1;
                        self.add_object_func_call_to_graph([filename,line_pos],line,nodelists,mapstack,file_collection.dx_version)
                        
                    elif is_func_call(line):
                        # ret = parse_func_call(line)
                        # if ret[0] in must_add_func:
                        if "axdHintResourceGpuVirtualAddr" in line or "axMemCpy" in line:
                            resource_list = get_resource_from_line(line)
                            node = Node(resource_list[0],[filename,line_pos],line,is_func_call.__str__)
                            nodelists.add_node(node)
                            self.add_vertex(node)
                        elif  "D3DCompileFromFile" in line:
                            node = Node("MUST",[filename,line_pos],line,is_func_call.__str__)
                            nodelists.add_node(node)
                        self.add_func_call_to_graph([filename,line_pos],line,file_collection.dx_version)

                    elif is_func_asigment(line):
                        self.add_func_asigment_to_graph([filename,line_pos],line)
                        

                    elif is_comment(line):
                        pass
                    elif is_obj_func_asigment(line):
                        
                        resource_list = get_resource_from_line(line)
                        node_list = [Node(res,[filename,line_pos],line,is_obj_func_asigment.__str__) for res in resource_list]
                        for node in node_list[::-1]:
                            self.add_vertex(node)
                            self.add_edge(node_list[-1],node)      
                    else:
                        pass
                    line_pos = line_pos+1

        
class NodeLists():
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = []
        self.nodes[node.id].append(node)
    
    def get_node(self,node_id):
        # 根据id 获取途中属性为id的所有位置
        return self.nodes[node_id]

    def print(self):
        for node in self.nodes:
            node.print()
        

class MapStack():
    def __init__(self):
        # 格式是：[(map,line_pos),...]
        self.stack = []

    def push(self, node):
        self.stack.append(node)

    def pop(self):
        return self.stack.pop()
    
    def top(self):
        return self.stack[-1]
    