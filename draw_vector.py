from line_util import *
import os
from dx11_config import *

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

def dx11_read_to_draw_vector(file_collection,draw_vectors):
    for filename in file_collection.file_list:
        line_pos = 0
        start_pos = [filename, line_pos]
        end_pos = []
        with open(os.path.join(file_collection.temp_path,filename), "r") as f:
            is_save = False
            flag= False
            for line in f:
                resource_list = get_resource_from_line(line)
                if is_var_statement(line):
                    try:
                        res = parse_var_state_line(line)
                        if "uavIniCounts" in line and "NULL" in line and "4294967295" not in line and flag == False:
                                is_save = True
                                flag = True
                    except:
                        pass

                elif is_object_func_call(line):
                    if "pDev11_0->CreateRenderTargetView(pResource = pSwap_0_buf_0, pDesc = rtv"  in line :
                        is_save = True       
                    ## 判断是不是Draw()
                    res = parse_object_func_call(line)
                    if res[1] in draw_stage_func:
                        end_pos = [filename, line_pos]
                        dv = DrawVector(start_pos,end_pos,is_save)
                        dv.set_resource(resource_list)
                        draw_vectors.append(dv)
                        resource_list = []
                        start_pos = [filename, line_pos+1]
                        end_pos = []
                        is_save = False
                        flag = False
                line_pos = line_pos+1
