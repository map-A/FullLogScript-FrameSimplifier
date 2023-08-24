# 根据已有的资源创建了另一个资源
# 原有的资源状态没有改变，创建另一个等同于改变了它的状态
obj_create_func = set({'GetBuffer', 'CreateRenderTargetView','CreateGeometryShader','CreateQuery',
               'CreateUnorderedAccessView','CreateInputLayout','CreateSwapChain',
               'CreateDepthStencilView',
               'CreateVertexShader','CreatePixelShader','CreateShaderResourceView',
               'CreateSamplerState','CreateDepthStencilState','CreateBlendState', 
               'CreateTexture2D','CreateComputeShader',
                'CreateRasterizerState','CreateBuffer',
                })

# 设置已有的资源 
obj_single_set_func =set({'ClearDepthStencilView','PSSetShader',
                          'RSSetState','VSSetConstantBuffers',
                          'GSSetConstantBuffers','IASetIndexBuffer',
                          'PSSetConstantBuffers', 'RSSetViewports',
                          'GSSetShaderResources','PSSetSamplers',
                          'PSSetShaderResources','IASetInputLayout',
                          'GSSetShader','OMSetDepthStencilState',
                          'VSSetShader','VSSetShaderResources',
                          'DiscardResource','DrawInstancedIndirect','DiscardView'
                          })




obj_multi_set_func = set({'OMSetRenderTargets','OMSetBlendState',
                          'IASetVertexBuffers','OMSetRenderTargetsAndUnorderedAccessViews',
                          'ClearRenderTargetView','CopyStructureCount', 
                          })



map_func = set({'Map','Unmap','axdUpdatePtrFromFileInCtx11'})



# 一定添加的，不管是不是资源
must_add = set({'CopyResource','IASetPrimitiveTopology','axdRelease',})

# 只做行为动作，不依赖任何资源
other_func = set({'Flush','ClearState','Present', 'Draw','DrawIndexedInstanced','DrawIndexed'})


class Node:
    def __init__(self, id, line_pos):
        self.id = id # 资源名称
        self.line_pos = line_pos # 资源所在位置
    
    def print(self):
        print(self.id, self.line_pos)

## 应该建立有向图
class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    # 判断是否存在该节点
    def has_vertex(self, node):
        return node.id in self.vertices
    
    def has_edge(self, vertex1, vertex2):
        if vertex1.id in self.edges:
            return vertex2 in self.edges[vertex1.id]
        return False
    
    def get_node(self,node_id):
        # 根据id 获取途中属性为id的所有位置
        if (self.has_vertex(Node(node_id,[]))):
            return self.vertices[node_id]
        return None
    
    def get_neighbors(self, node_id):
        # 获取node_id的邻居节点
        if node_id in self.edges:
            return self.edges[node_id]
        return None

    def add_vertex(self, node):
        if node.id not in self.vertices:
            self.vertices[node.id] = []
        self.vertices[node.id].append(node)


    def add_edge(self, vertex1, vertex2):
        # vertex1.id -> vertex2
        if self.has_vertex(vertex1) and self.has_vertex(vertex2):
            if vertex1.id not in self.edges:
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
            print(key, "->",self.edges[key], self.edges[key])

    def dfs(self,node_id,res):
        #从属性值为node_id的开始深度遍历，遍历的结果存到res数组中
        stack = [node_id]
        visited = set()
        while stack:
            cur = stack.pop()
            if cur not in visited:
                visited.add(cur)
                for i in self.get_node(cur):
                    res.append(i.line_pos)
                neibo = self.get_neighbors(cur)
                if neibo:
                    for nxt in neibo:
                        res.append(nxt.line_pos)
                        if nxt.id not in visited:
                            stack.append(nxt.id)

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
        

class MapStack:
    def __init__(self):
        # 格式是：[(map,line_pos),...]
        self.stack = []

    def push(self, node):
        self.stack.append(node)

    def pop(self):
        return self.stack.pop()
    
    def top(self):
        return self.stack[-1]