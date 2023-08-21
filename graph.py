# 根据已有的资源创建了另一个资源
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

class Node:
    def __init__(self, id, line_pos):
        self.id = id # 资源名称
        self.line_pos = line_pos # 资源所在位置
    
    def print(self):
        print(self.id, self.line_pos)


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    # 判断是否存在该节点
    def has_vertex(self, node):
        return node.id in self.vertices
    

    def add_vertex(self, node):
        self.vertices[node.id] = node


    def add_edge(self, vertex1, vertex2):
        # vertex1 -> vertex2
        if self.has_vertex(vertex1) and self.has_vertex(vertex2):
            if vertex1 not in self.edges:
                self.edges[vertex1] = []
            self.edges[vertex1].append(vertex2)
            
    def get_neighbors(self, vertex):
        return self.vertices[vertex]
    
    def print(self):
        for key in self.vertices:
            self.vertices[key].print()

    def print_vertices(self):
        for key in self.vertices:
            print(key)
    def print_edges(self):
        for key in self.edges:
            print(key, "->",self.edges[key])
