import struct
from line_util import *
import os
from dx11_config import *
from copy import deepcopy

class Draw():
    def __init__(self,draw_lines,draw_type,resource_list,is_contain_cssetshader):
        self.draw_lines = deepcopy(draw_lines)
        self.draw_type = deepcopy(draw_type)
        self.resource_list = deepcopy(resource_list) # 这段dispatch包含的
        self.is_contain_cssetshader = is_contain_cssetshader
        self.dump_resource = {}
    
    def set_save(self,value):
        self.is_contain_cssetshader = value
    def get_draw_type(self):
        return self.draw_type
    def get_is_contain_cssetshader(self):
        return self.is_contain_cssetshader
    def get_resource_list(self):
        return self.resource_list

    def get_draw_lines(self):
        return self.draw_lines
    def clear_draw_lines(self):
        self.draw_lines.clear()
    def append_draw_lines(self,line):
        self.draw_lines.append(line)
    def set_dump_resource(self,dump_resource_list):
        self.dump_resource = deepcopy(dump_resource_list)
    def get_dump_resource(self):
        return self.dump_resource

class DrawVector():
    # 将一个脚本文件分成一段一段的draw或者dispatch
    def __init__(self):
        self.__draw__ = {} # filename：[dispatch]
        self.UAV_pair_set = {}
    def add_draw(self,filename,draw):
        if self.__draw__.get(filename) is None:
            self.__draw__[filename] = []
        self.__draw__[filename].append(draw)
        
        if self.UAV_pair_set.get(",".join(draw.get_resource_list())) is not None:
            # 如果set已经包含，把原有的设置为False，再保存新的
            self.UAV_pair_set.get(",".join(draw.get_resource_list())).set_save(False)
        self.UAV_pair_set[",".join(draw.get_resource_list())] = draw

    def get_draw(self,filename):
        return self.__draw__[filename]
    def get_all(self):
        return self.__draw__



def dx11_read_to_draw_vector(file_collection,draw_vectors,graph):
    is_create_buffer = False
    index = 0 # 用于标识dump下的bufer id
    for filename in file_collection.file_list:
        with open(os.path.join(file_collection.temp_path,filename), "r") as f:
            is_save = False
            resource_list = []
            draw_lines = []
            for line_index,line in enumerate(f):
                draw_lines.append(line)
                if is_var_statement(line):
                    resource_list.extend(get_resource_from_line(line)[1:])
                if is_object_func_call(line):
                    res = parse_object_func_call(line)
                    if res[1] =="CSSetShader":
                        is_save = True
                    elif res[1] in draw_stage_func:
                        # 根据resource 有没有出现过，判断要不要存到vector中，怎么对其做一个替换
                        resource_list = list(set(resource_list))
                        dv = Draw(draw_lines,res[1],resource_list,is_contain_cssetshader=is_save)
                        draw_vectors.add_draw(filename,dv) # 某个文件的dispatch
                        draw_lines.clear()
                        resource_list.clear()
                        is_save = True
            
            dv = Draw(draw_lines,"Present",resource_list,False)
            draw_vectors.add_draw(filename,dv)
            draw_lines.clear()
            resource_list.clear()
            is_save = False

        if not os.path.exists(file_collection.refactor_path):
            os.makedirs(file_collection.refactor_path)
        with open(os.path.join(file_collection.refactor_path,filename), "w") as f:
            # 对文件进行重写        
            
            # 然后对每个draw进行重写，添加需要dump的资源，为了dump下数据
            for draw in draw_vectors.get_draw(filename):
                if not draw.get_is_contain_cssetshader():
                    for lines in draw.get_draw_lines():
                        f.write(lines)
                # 在每个draw后面根据信息添加copy construct
                else:
                    # else 就开始重写,行数也会变化，所以需要重新计算
                    # 创建一个用于copystruct 的buffer
                    # 这里需要插入一个buffer创建语句,应该只创建一次，bufer的闯将应该再第一次dispatch之前。
                    # 先构建dump语句
                    if not is_create_buffer:
                        f.write('D3D11_BUFFER_DESC bufDesc_for_dispatch[1] =(ByteWidth = 0x10,Usage = D3D11_USAGE_DEFAULT,BindFlags = D3D11_BIND_UNORDERED_ACCESS,CPUAccessFlags = 0x00000000,MiscFlags = D3D11_RESOURCE_MISC_DRAWINDIRECT_ARGS,StructureByteStride = 0x0,);\n')
                        f.write('D3D11_SUBRESOURCE_DATA bufData_for_dispatch[1] =(pSysMem = file(pBuf_for_dispatch.bin),SysMemPitch = 0x10,SysMemSlicePitch = 0x10,);\n')
                        f.write('pDev11_0->CreateBuffer(pDesc = bufDesc_for_dispatch, pInitialData = bufData_for_dispatch, ppBuffer = pBuf_for_dispatch);\n')
                        is_create_buffer = True

                    dump_resource_list = {}
                    for lines in draw.get_draw_lines():
                        f.write(lines)
                    for res in draw.get_resource_list():
                        # 有pBuf，pUAV，pSRV，只需要dump只一些
                        if res.startswith('pUAV'):
                            f.write('pCtx_0->CopyStructureCount(pDstBuffer = pBuf_for_dispatch, DstAlignedByteOffset = 0x0, pSrcView = '+res+');\n')
                            f.write('axdDumpResource(pCtx_0, IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN, pBuf_for_dispatch, 0, "'+ res+"_"+str(index)+'.bin");\n')
                            dump_resource_list[res]=res+"_"+str(index)+'.bin'
                            index = index+1 
                            # 需要把UAV引用到的buffer也dump下来
                            ref_resource = []
                            graph.get_leaf(res,ref_resource)
                            for ref in ref_resource:
                                if 'pBuf_' in ref:
                                    f.write('axdDumpResource(pCtx_0, IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN,'+ ref+', 0, "'+ ref+'_'+str(index)+'.bin");\n')
                                    dump_resource_list[ref] = ref+'_'+str(index)+'.bin'
                                    index = index+1
                                elif 'pTex' in ref:
                                    f.write('axdDumpResource(pCtx_0, IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN,'+ ref+', 0, "'+ ref+'_'+str(index)+'.dds");\n')
                                    dump_resource_list[ref] = ref+'_'+str(index)+'.dds'
                                    index = index+1
                        elif res.startswith('SRV'):
                            f.write('axdDumpResource(pCtx_0, IID_ID3D11Resource, DXGI_FORMAT_UNKNOWN,'+ res+', 0, "'+ res+'.dds");\n')
                        elif 'pSRV_' in res:
                            pass
                    
                    
                    draw.set_dump_resource(dump_resource_list)
                    
                    




