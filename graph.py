# 根据已有的资源创建了另一个资源
# 原有的资源状态没有改变，创建另一个等同于改变了它的状态
create_func = set({'Map','GetBuffer', 'CreateRenderTargetView','CreateGeometryShader','CreateQuery',
               'CreateUnorderedAccessView','CreateInputLayout','CreateSwapChain','CreateDepthStencilView',
               'CreateVertexShader','CreatePixelShader','CreateShaderResourceView','CreateSamplerState',
               'CreateDepthStencilState','CreateBlendState', 'CreateTexture2D','CreateComputeShader',
                'CreateRasterizerState','CreateBuffer'})

# 设置已有的资源
set_func = set({'RSSetState','OMSetBlendState','PSSetShader','VSSetConstantBuffers','OMSetRenderTargets','GSSetConstantBuffers',
            'IASetIndexBuffer','PSSetConstantBuffers','RSSetViewports','GSSetShaderResources','PSSetSamplers','PSSetShaderResources', 
            'IASetVertexBuffers','IASetInputLayout', 'OMSetRenderTargetsAndUnorderedAccessViews', 'GSSetShader','OMSetDepthStencilState',
            'IASetPrimitiveTopology', 'VSSetShader', 'VSSetShaderResources',
            'ClearRenderTargetView','ClearDepthStencilView', 
            'CopyResource','CopyStructureCount', 
            'DiscardResource','DiscardView','Unmap','DrawInstancedIndirect'})

# 只做行为动作，不依赖任何资源
other_func = set({'Flush','ClearState', 'Present', 
              'Draw','DrawIndexedInstanced','DrawIndexed'})


# 函数调用名称
a = {'axPath', 'D3D11CreateDevice', 'axdUpdatePtrFromFileInCtx11', 'CreateDXGIFactory1', 'axdRelease'}

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
    
    def get_node(self,node_id):
        # 根据id 获取途中属性为id的所有位置
        if (self.has_vertex(Node(node_id,[]))):
            return self.vertices[node_id]
        return None
    
    def get_neighbors(self, node_id):
        # 获取node_id的邻居节点
        if node_id  in self.edges:
            return self.edges[node_id]
        return None

    def add_vertex(self, node):
        if node.id not in self.vertices:
            self.vertices[node.id] = []
        self.vertices[node.id].append(node)


    def add_edge(self, vertex1, vertex2):
        # vertex1.id -> vertex2
        if self.has_vertex(vertex1) and self.has_vertex(vertex2):
            if vertex1 not in self.edges:
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
        #从属性值为id的开始深度遍历，遍历的结果存到res数组中
        stack = [node_id]
        visited = set()
        while stack:
            cur = stack.pop()
            if cur not in visited:
                visited.add(cur)
                res.append(cur)
                neibo = self.get_neighbors(cur)
                if neibo:
                    for nxt in neibo:
                        if nxt not in visited:
                            stack.append(nxt)
        return res

class NodeList():
    def __init__(self):
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def print(self):
        for node in self.nodes:
            node.print()