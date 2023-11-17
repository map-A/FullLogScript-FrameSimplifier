from draw_vector import *
from inject_file import InjectFile
from line_util import *
from file_util import *
from graph import *
import configparser
import sys
import argparse
import os
import subprocess
from simple_frame import *
if __name__ == "__main__":
    
    simplify_frames = SimpleFrame()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_path',required=True,help='src script path')
    parser.add_argument('-f','--first_scene_number',required=True,type=int,help="the first scene present number")
    parser.add_argument('-b', '--begin',required=True,type=int,help='Begining Simplified Script Sequence Number')
    parser.add_argument('-n', '--numbers_to_simple',required=False,type=int,default=1, help='number consecutive frames')
    args = parser.parse_args()
    if(args):
        simplify_frames.set(args.src_path,args.first_scene_number,args.begin,args.numbers_to_simple)
    else:
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8') 
        simplify_frames.set(config['path']['src_path'],int(config['frame_index']['scene_begins_index']),int(config['frame_index']['save_start_index']),int(config['frame_index']['n']))
        


    tmp_path = args.src_path+r"temp\\" # 新的src path，原有的变成origin_path
    target_path = args.src_path +r"frames\\"

    # 读取文件到file_collection中
    file_collection = FileCollection(args.src_path+"vector\\",tmp_path)
    file_collection.merge_files(args.src_path+r"merge\\",0,simplify_frames.save_start_index)
    
    # 用这些文件内容构建图
    graph = Graph()
    nodelist = NodeLists()
    mapstack = MapStack()
    draw_vectors = []
    if file_collection.dx_version==11:
        graph.read_dx11_to_graph(file_collection,nodelist,mapstack)
        dx11_read_to_draw_vector(file_collection,draw_vectors)
    elif file_collection.dx_version==12:
        graph.read_dx12_to_graph(file_collection,nodelist,mapstack)
    else:
        print("dx version error")
        sys.exit()

    # 用这些文件内容构建draw_vector
    
    
 
    

    #用这些文件生成inject文件
    inject_file = InjectFile(file_collection,tmp_path,simplify_frames.save_end_index)
    if file_collection.dx_version==11:
        inject_file.generate_dx11_inject_file(graph)
        inject_file.generate_final_dx11_inject_file(args.begin)

    elif file_collection.dx_version==12:
        inject_file.generate_dx12_inject_file(graph)
        inject_file.generate_final_dx12_inject_file(graph,args.begin)
    else:
        print("dx version error")
        sys.exit()

    # cmd = r".\\qReplay\\qReplay.exe -s "+ os.path.join(file_collection.temp_path,file_collection.file_list[0]) +" --inject "+ inject_file.inject_file_name+ " --hide"
    # print(cmd)
    # p1 = subprocess.Popen(cmd, shell=True)
    # p1.wait()

    # # 开始简化生成新的sdx文件
    simplify_frames.simplify_frames(file_collection,graph,nodelist,draw_vectors,inject_file,target_path)

    print("simplify success")
    input("Press enter to exit...")
    sys.exit()
