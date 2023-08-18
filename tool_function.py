import os
import re

def read_dir(folder_path):
    """
    读取文件夹下所有符合条件的文件
    :param folder_path: 文件夹路径
    :return: 经过排序后的文件列表
    """
    if not os.path.exists(folder_path):
        print('Folder does not exist')
        return 
    file_list = []
    
    # 获取文件夹下所有符合条件的文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".sdx") and "_" in filename and filename.split("_")[1][:-4].isdigit():
            file_list.append(filename)
    file_list.sort(key=lambda x: int(x.split("_")[1][:-4].split(".")[0]))
    return file_list

def trim_files(src_path,target_path):
    """
    将把文件夹下所有文本按照分号分割成句子，去除空格和换行符，写入新文件
    :param folder_path: 文件夹路径
    :param target_path: 目标保存文件夹路径
    :return: None
    """
    if not os.path.exists(src_path):
        print('Folder does not exist')
        return
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    file_list = read_dir(src_path)
    for filename in file_list:
        with open(src_path + filename, 'r') as f, open(target_path+filename, 'w') as out_f:
            sentence = ""
            index = 0
            for line in f:
                index = index + 1
                line = line.strip()
                if(index <2):
                  out_f.write(line + '\n')
                  continue
                else:
                    if re.search(r'[;]$', line):
                        sentence += line
                        out_f.write(sentence + '\n')
                        sentence = ""
                    else:
                        sentence += line
        if sentence:
            out_f.write(sentence + '\n')

# 判断文件中的语句是什么类型的语句
# 1. 函数调用
# 2. 对象调用
# 3 注释
# 4. 空行
# 5. 其他 ,声明，赋值




def is_comment(line):
    return line.startswith('//')

def is_empty(line):
    return line == '\n'


def is_func_call(line):
    pattern = r'\w+\(.*\);'  
    if re.match(pattern, line):
        return True
    else:
        return False

def is_object_func_call(line):
    pattern = r'\w+->\w+\(.*\);'
    if re.match(pattern, line):
        return True
    else:
        return False


def is_other(line):
    if is_comment(line) or is_empty(line) or is_func_call(line) or is_object_func_call(line):
        return False
    else:
        return True


###################################
### 解析一个语句，返回一个词列表，判断这些词的属性

def is_decimal_or_hex(string):
  """
  判断是否是十进制或十六进制
  :param string
  :return:bool
  """
  string = string.strip()
  if not string:
    return False

  try: 
    int(string, 10)
    return True
  except ValueError:
    pass

  try:
    int(string, 16)
    return True
  except ValueError:
    pass

  return bool(re.match(r'^[0-9a-fA-F]+$', string))


def is_macro(string):
  """
  判断是否是宏定义
  :param string
  :return:bool
  """
  return bool(re.fullmatch(r'[A-Z0-9_]+', string))


def is_valid_variable(string):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    return re.match(pattern, string) and any(c.islower() for c in string)

### 如果是一个声明，那么只需要提取等号左边的变量，
# 如果是函数，函数的种类不同，提取的变量也不同


# 解析一个函数调用，返回函数名和参数列表
def parse_func_call(func_call):
    func_name = func_call.split('(')[0]
    func_args = func_call.split('(')[1].split(')')[0].split(',')
    func_args = [arg.strip() for arg in func_args]
    return func_name, func_args
#解析一个对象函数调用，返回对象名、函数名和参数列表
def parse_object_func_call(statement):
    pattern = r'(\w+)\s*->\s*(\w+)\s*\((.*?)\);'
    match = re.match(pattern, statement)
    
    if match:
        object_name = match.group(1)
        function_name = match.group(2)
        arguments = match.group(3)
        argument_list = [arg.strip() for arg in arguments.split(',')] if arguments else []
        return object_name, function_name, argument_list
    else:
        return None

# 解析一个声明语句，返回声明变量类型，声明变量，赋值
def parse_statement(string):
  pattern = r'(\w+\*?)\s*(\w+\*?)(\[.*?\]*)\s*=\s*(.*?);'
  match = re.match(pattern, string)
  if match:
    a = match.group(1)
    b = match.group(2) 
    c = match.group(3)if match.group(3) else ""
    d = match.group(4)
    return a,b,c,d
  else:
    return None
  
# 解析一个赋值语句，返回赋值变量，赋值
def parse_func_assignment(string):
   print(string)
   pattern = r'(.*)\s*=\s*(.*)'
   match = re.match(pattern, string)
   if match:
    a = match.group(1)
    b = match.group(2) if match.group(2) else ""
    return a,b
   else:
      return None