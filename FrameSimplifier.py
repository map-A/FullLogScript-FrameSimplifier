from tool_function import *
from graph import *
from build_graph import *
from write_new_file import *
import configparser
import sys
import os
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
    parser.add_argument('-m', '--magic_number',required=False,type=int,default=0, help='i donnot know how to set it, it better set over 17,when it set 0,it work without wrong,but simple script\
                        will be larger, when is set over than 0,script will be small ,but it might work wrong')
    args = parser.parse_args()
    if(args):
        src_path = args.src_path
        scene_begins_index = args.first_scene_number
        save_start_index = args.begin
        numbers_to_simple = args.numbers_to_simple
        offset = args.magic_number
    else:
    

        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8') 
        # 尝试不同编码转换直到不报错
        # 尝试utf-8解码
        scene_begins_index= int(config['frame_index']['scene_begins_index'])
        save_start_index = int(config['frame_index']['save_start_index'])
        numbers_to_simple = int(config['frame_index']['n'])
        src_path = config['path']['src_path']
        offset  = config['frame_index']['magic_number']
    
    save_end_index = save_start_index+numbers_to_simple-1


    tmp_path = os.path.dirname(os.path.dirname(src_path)) +r"\temp\\" # 新的src path，原有的变成origin_path
    target_path = os.path.dirname(os.path.dirname(src_path)) +r"\frames\\"
    
    trim_files(src_path,tmp_path)

    graph = Graph()
    nodelist = NodeLists()
    mapstack = MapStack()
    drawvector = DrawVector()

    
    file_list = read_dir(tmp_path)
    for filename in file_list:
        read_to_graph(tmp_path+filename,graph,nodelist,mapstack)        
        read_to_draw_vector(tmp_path+filename,drawvector)

    
    simplify_frames(graph,nodelist,drawvector,src_path,tmp_path,target_path,save_start_index,save_end_index,offset)
    
    print("simplify success")
    input("Press enter to exit...")
    sys.exit()
