# 根据已有的资源创建了另一个资源
# 原有的资源状态没有改变，创建另一个等同于改变了它的状态
# device 的函数, 一定要添加的，创建了资源
import copy


device_func = set({'CreateSwapChain','CreateRenderTargetView','CreateGeometryShader','CreateQuery',
               'CreateUnorderedAccessView','CreateInputLayout','CreateDepthStencilView',
               'CreateVertexShader','CreatePixelShader','CreateShaderResourceView','CreateTexture3D',
               'CreateSamplerState','CreateDepthStencilState','CreateBlendState', 
               'CreateTexture2D','CreateComputeShader',
                'CreateRasterizerState','CreateBuffer','CreateHullShader','CreateDomainShader',
                'CreateDeferredContext','CreateGeometryShaderWithStreamOutput','CreatePredicate',
                'CreateTexture1D','CreateBlendState1','CreateDeferredContext1',
                'CreateDeviceContextState','CreateQuery1','CreateRenderTargetView1',
                'CreateShaderResourceView1','CreateTexture2D1','CreateTexture3D1',
                'CreateUnorderedAccessView1','CreateFence',"CreateRasterizerState1",
                'ClearState', 'ClearDepthStencilView','ClearRenderTargetView','ClearUnorderedAccessViewFloat',
                "CreateDXGIFactory1","D3D11CreateDevice","CreateSwapChain",
                'CopyResource','CopyStructureCount','CopyCounter','CopyTiles','CopyTileMappings','CopyBufferRegion','CopySubresourceRegion',
                })



IA_stage_func = set({'IASetIndexBuffer','IASetVertexBuffers','IASetInputLayout',})
VS_stage_func = set({'VSSetShader','VSSetConstantBuffers','VSSetShaderResources',})
HS_stage_func = set({'HSSetShader','HSSetConstantBuffers','HSSetShaderResources','HSSetSamplers'})
TS_stage_func = set({'TSSetShader','TSSetConstantBuffers','TSSetShaderResources',})
DS_stage_func = set({'DSSetShader','DSSetConstantBuffers','DSSetShaderResources','DSSetSamplers',})
GS_stage_func = set({'GSSetShader','GSSetConstantBuffers','GSSetShaderResources','GSSetSamplers',})
RS_stage_func = set({'RSSetState','RSSetViewports',})
PS_stage_func = set({'PSSetShader','PSSetConstantBuffers','PSSetShaderResources','PSSetSamplers',})
OM_stage_func = set({'OMSetDepthStencilState','OMSetRenderTargets','OMSetBlendState','OMSetRenderTargetsAndUnorderedAccessViews',
                'ClearDepthStencilView','ClearRenderTargetView','CopyStructureCount', 
                'DiscardView','DiscardResource',
                })
CS_stage_func = set({'CSSetShader','CSSetConstantBuffers','CSSetShaderResources','CSSetSamplers','CSSetUnorderedAccessViews',})

#draw_stage_func = set({"Dispatch"})
draw_stage_func = set({'Draw','DrawIndexedInstanced','DrawIndexed',
                        'DrawAuto',
                        'Dispatch','DispatchIndirect',
                        'DrawIndexedInstancedIndirect',
                        'DrawInstanced','DrawInstancedIndirect',})


obj_set_func =set({
    'IASetIndexBuffer','IASetVertexBuffers','IASetInputLayout',
    'VSSetShader','VSSetConstantBuffers','VSSetShaderResources',
    'HSSetShader','HSSetConstantBuffers','HSSetShaderResources','HSSetSamplers',
    'TSSetShader','TSSetConstantBuffers','TSSetShaderResources',
    'DSSetShader','DSSetConstantBuffers','DSSetShaderResources','DSSetSamplers',
    'GSSetShader','GSSetConstantBuffers','GSSetShaderResources','GSSetSamplers',
    'RSSetState','RSSetViewports',
    'PSSetShader','PSSetConstantBuffers','PSSetShaderResources','PSSetSamplers',
    'OMSetDepthStencilState','OMSetRenderTargets','OMSetBlendState','OMSetRenderTargetsAndUnorderedAccessViews',
    'ClearDepthStencilView','ClearRenderTargetView','CopyStructureCount', 
    'DiscardView','DiscardResource',
    'CSSetShader','CSSetConstantBuffers','CSSetShaderResources','CSSetSamplers','CSSetUnorderedAccessViews',
    'GenerateMips','ClearUnorderedAccessViewFloat'})


map_func = set({'Map','Unmap','axdUpdatePtrFromFileInCtx11'})


# 一定添加的，不管是不是资源
must_add = set({'axdRelease','GetBuffer','IASetPrimitiveTopology','GenerateMips','D3DCompileFromFile','CreateDXGIFactory1'
                'CopyResource','CopyStructureCount','CopyCounter','CopyTiles','CopyTileMappings','CopyBufferRegion','CopySubresourceRegion',
                "CreateDXGIFactory1","D3D11CreateDevice","CreateSwapChain",})
# IASetPrimitiveTopology 保证在一个Draw添加一次即可# get Buffer 一次

# 为了生成一个inject文件
copy_func = set()
#copy_func = set({'CopyResource','CopyStructureCount','CopyCounter','CopyTiles','CopyTileMappings','CopyBufferRegion','CopySubresourceRegion',})




other_func = set({'Flush','ClearState','Present','CreateDXGIFactory1'})


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
        return []
    
    def get_neighbors(self, node_id):
        # 获取node_id的邻居节点
        if node_id in self.edges:
            return self.edges[node_id]
        return []

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
    
    def get_leaf(self,nodeid,res):
        # 获取nodeid的叶子节点
        temp = []
        stack = [nodeid]
        visited = set()
        while stack:
            cur = stack.pop()
            temp.append(cur.strip())
            if(" " in cur):
                print(cur,"dadaasdasd")
            if cur not in visited:
                visited.add(cur)
                neibo = self.get_neighbors(cur)
                if neibo:
                    for nxt in neibo:
                        if nxt.id not in visited:
                            stack.append(nxt.id)
        for i in temp:
            if i[0:4]=="pBuf" or i[0:4]=="pTex" or i == "pSwap_0_buf_0" or i[0:4]=="pSRV" or i[0:4]=="pUAV"  or i[0:4]=="RTV" or i[0:4]=="DSV": 
                res.append(i)
        # for i in temp:
        #     if i[0:4]=="pBuf" or i[0:4]=="pTex" or i == "pSwap_0_buf_0": 
        #     #or i[0:3]=="pCS" or i[0:3]=="pDS" or i[0:3]=="pGS" or i[0:3]=="pHS" or i[0:3]=="pPS" or i[0:3]=="pVS" or i[0:3]=="pIn":
        #         res.append(i)    
        
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
    

class DrawVector():
    # 将一个脚本文件集划分成一段一段的draw或者dispatch
    def __init__(self,start_pos,end_pos,is_save=False):
        self.__pos__ = [start_pos,end_pos]
        self.__is_save__ = is_save
        self.__resource__ = []

    def get_is_save(self):
        return self.__is_save__
    
    def get_pos(self):
        return self.__pos__
    def get_resource(self):
        return self.__resource__
    
    def set_resource(self,resource):
        self.__resource__ = resource
    def set_is_save(self,is_save):
        self.__is_save__ = is_save

    def print_drawvector(self):
        for i in self.__drawVector__:
            print(i)

    
