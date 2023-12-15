from dx12_config import *
import re
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
    
def is_func_asigment(line):
   # 形如这种axCreateEvent(NULL, FALSE, FALSE, WIN_EVENT_ALL_ACCESS)=hEvent_91;
    pattern = r'\w+\(.*\)=\w+';
    if re.match(pattern, line):
        return True
    else:
        return False
def is_obj_func_asigment(line):
    #pDescHeap_5->GetCPUDescriptorHandleForHeapStart() = pDescHeap_5_cpuH;
    pattern = r'(.*)->(.*)\((.*)\)\s*=\s*(.*);'
    if re.match(pattern, line):
        return True
    else:
        return False


def is_var_statement(line):
    ## other line 指的是形如 A B[2] = C的语句，包括结构体嵌套定义
    # 这条语句默认加入吧
    pattern = r'(\w+\*?)\s*(\w+\*?)(\[.*?\]*)\s*=\s*\(.*\)'
    match = re.match(pattern, line)
    if match:
        return True
    else:
        return False


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
  return bool(re.fullmatch(r'\s*[A-Z0-9_]+\s*', string))


def is_valid_variable(string):    
    pattern = r'^[a-z][a-zA-Z0-9_]*$'
    if re.match(pattern, string):
        return True
    else:
        return False



# 如果是函数，函数的种类不同，提取的变量也不同
# 解析一个函数调用，返回函数名和参数列表
def parse_func_call(line):
    pattern = r'(\w+)\((.*)\);'  
    match =  re.match(pattern, line)
    if match:
        func_name = match.group(1)
        func_args = match.group(2)
        func_args = [arg.strip() for arg in func_args.split(',')] if func_args else []
        return func_name, func_args
    else:
        return None

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


def parse_func_assignment(string):
   pattern = r'(.*)\s*=\s*(.*)'
   match = re.match(pattern, string)
   if match:
    a = match.group(1)
    b = match.group(2) if match.group(2) else ""
    return a,b
   else:
      return None
   
def parse_var_state_line(string,line_map):
    """
    解析 诸如A B[2] = C的语句,结构体嵌套定义
    :param string
    :return:line_map将声明按照kv存储
    """

    # match = re.match(r'(\w+\*?)\s+(\w+\*?)\[(.*?\)\]\s*=\s*\(.*\)', string)
    pattern = r'(\w+\*?)\s*(\w+\*?)(\[.*?\]*)\s*=\s*\((.*)\);'
    match = re.match(pattern, string)
     
    if match:
        # 提取结构体类型、变量名和数组大小
        line_map["struct_type"] = match.group(1)
        line_map["var_name"] = match.group(2)
        line_map["array_size"] = match.group(3)
        # 提取结构体内的字段
    
    assign_part = re.sub(' ','',match.group(4))
    pattern1 = r'(\w+)=\(*([\w.,()]*)\)*,'
    matches = re.findall(pattern1, assign_part)
    line_map["assign_value"] = []
    if matches:
        for i in matches:
            line_map[i[0]] = i[1].strip(")")
    else:
        for i in assign_part.split(','):
            line_map["assign_value"].append(i)

def parse_func_assign_to_var(string):
    # axdAddCpuDescriptorHandle(pDescHeap_4, 3)=pDescHeap_4_cpuH_3;
    pattern = r'(.*)\((.*)\)\s*=\s*(.*);'
    match = re.match(pattern, string)
    if match:
     a = match.group(1)
     b = match.group(2) if match.group(2) else ""
     c = match.group(3) if match.group(2) else ""
     return a,b,c
    else:
        return None
   
def parse_obj_func_assign_to_var(string):
    # pDescHeap_5->GetCPUDescriptorHandleForHeapStart() = pDescHeap_5_cpuH;
    pattern = r'(.*)->(.*)\((.*)\)\s*=\s*(.*);'
    match = re.match(pattern, string)
    if match:
        a = match.group(1)
        b = match.group(2) if match.group(2) else ""
        c = match.group(3) if match.group(2) else ""
        d = match.group(4) if match.group(2) else ""
        return a,b,c,d
    else:
        return None



def get_resource_from_line(line):
    resource_list = []
    if is_var_statement(line):
        line_map = {}
        parse_var_state_line(line,line_map)
        for i in line_map:
            if type(line_map[i]) == str:
                if "," in line_map[i]:
                    for j in line_map[i].split(","):
                        if is_valid_variable(j.strip(" ")):
                            resource_list.append(j.strip(" "))
                else:
                    if is_valid_variable(line_map[i]):
                        resource_list.append(line_map[i])
            elif type(line_map[i]) == list:
                for j in line_map[i]:
                    if is_valid_variable(j.strip(" ")):
                        resource_list.append(j.strip(" "))

        # resource_list = [line_map[i] for i in line_map if is_valid_variable(line_map[i])]
        
    elif is_object_func_call(line):
        ret = parse_object_func_call(line)
        if is_valid_variable(ret[0]):
            resource_list.append(ret[0])
        resource_list.extend([parse_func_assignment(i)[1] for i in ret[2] if is_valid_variable(parse_func_assignment(i)[1])])
         
    
    elif is_func_call(line):
        
        ret = parse_func_call(line)
        for i in ret[1]:
            if "=" in i:
                if is_valid_variable(parse_func_assignment(i)[1]):
                    resource_list.append(parse_func_assignment(i)[1])
            else:
                if is_valid_variable(i):
                    resource_list.append(i)       
    elif is_func_asigment(line):
        ret = parse_func_assign_to_var(line)
        resource_list  = [i for i in ret[1].split(",") if is_valid_variable(i)]
        if is_valid_variable(ret[2]):
            resource_list.append(ret[2])
    elif is_obj_func_asigment(line):
        ret = parse_obj_func_assign_to_var(line)
        resource_list  = [i for i in ret if is_valid_variable(i)]            
    return resource_list

def get_resource_type(line):
    if is_var_statement(line):
        for  i in texture_type:  
            if line.find(i) != -1:
                return ".dds"        
    return ".bin"

