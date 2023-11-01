from tool_function import *
from graph import *
from build_graph import *
from write_new_file import *
import configparser
import sys
import os
import subprocess
import argparse
if __name__ == "__main__":
    src_path = ""
    scene_begins_index= 1
    save_start_index = 1
    numbers_to_simple = 1
    offset = 0


    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_path',required=True,help='src script path')
    parser.add_argument('-f','--first_scene_number',required=True,type=int,help="the first scene present number")
    parser.add_argument('-b', '--begin',required=True,type=int,help='Begining Simplified Script Sequence Number')
    parser.add_argument('-n', '--numbers_to_simple',required=False,type=int,default=1, help='number consecutive frames')
    args = parser.parse_args()
    if(args):
        src_path = args.src_path
        scene_begins_index = args.first_scene_number
        save_start_index = args.begin
        numbers_to_simple = args.numbers_to_simple
    else:
    

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8') 
        # 尝试不同编码转换直到不报错
        # 尝试utf-8解码
        scene_begins_index= int(config['frame_index']['scene_begins_index'])
        save_start_index = int(config['frame_index']['save_start_index'])
        numbers_to_simple = int(config['frame_index']['n'])
        src_path = config['path']['src_path']
    
    save_end_index = save_start_index+numbers_to_simple-1


    tmp_path = src_path+r"temp\\" # 新的src path，原有的变成origin_path
    target_path = src_path +r"frames\\"
    trim_files(src_path+"\\vector\\",tmp_path)

    graph = Graph()
    nodelist = NodeLists()
    mapstack = MapStack()
    draw_vectors = []
    
    file_list = read_dir(tmp_path)
    inject_file = file_list[0].replace('_0.sdx','_Trim.inject')
    for filename in file_list:
        read_to_graph(tmp_path+filename,graph,nodelist,mapstack)        
        read_to_draw_vector(tmp_path+filename,draw_vectors)
        generate_inject_file(tmp_path+filename,src_path+inject_file,graph)
    
    simplify_frames(graph,nodelist,draw_vectors,src_path+"vector\\",tmp_path,target_path,save_start_index,save_end_index)
    
    generate_final_inject_file(src_path+"vector\\"+inject_file,tmp_path+inject_file,save_start_index)


    cmd = r".\\qReplay\\qReplay.exe -s "+ tmp_path+file_list[0]+" --inject "+ inject_file+ " --hide"
    print(cmd)
    p1 = subprocess.Popen(cmd, shell=True)
    p1.wait()

    new_filename_0 = re.sub(r'(\d+)\.sdx$',"F"+str(save_start_index)+'_0'+".sdx", file_list[0])
    upload_files(tmp_path,target_path,new_filename_0,inject_file)
    print("simplify success")
    input("Press enter to exit...")
    sys.exit()
