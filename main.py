from tool_function import *
from graph import *
from build_graph import *
from write_new_file import *
import configparser
import sys

if __name__ == "__main__":
   

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8') 
    # 尝试不同编码转换直到不报错
    # 尝试utf-8解码 

    start_draw_index = int(config['frame_index']['start_draw_index'])
    scene_begins_index= int(config['frame_index']['scene_begins_index'])
    save_start_index = int(config['frame_index']['save_start_index'])
    save_end_index = int(config['frame_index']['save_end_index'])
    src_path = config['path']['src_path']
    tmp_path = config['path']['tmp_path']
    target_path = config['path']['target_path']

    trim_files(src_path,tmp_path)

    graph = Graph()
    nodelist = NodeLists()
    mapstack = MapStack()
    drawvector = DrawVector()

    
    file_list = read_dir(tmp_path)
    for filename in file_list:
        read_to_graph(tmp_path+filename,graph,nodelist,mapstack)        
        read_to_draw_vector(tmp_path+filename,drawvector)

    
    simplify_frames(graph,nodelist,drawvector,tmp_path,target_path,save_start_index,save_end_index,start_draw_index)
    print("simplify success")
    input("Press enter to exit...")
    sys.exit()
