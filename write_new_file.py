
import re
def create_new_sdx_file(new_file_list,new_filename):
    def custom_sort(item):
        filename = item[0]
        line_number = item[1]
        name_num = re.search(r'(\d+)\.sdx$', filename)
        if name_num:
            name_num = int(name_num.group(1))
        return (name_num, line_number)

    sorted_data = sorted(new_file_list, key=custom_sort)
    unique_sorted_data = []
    seen_items = set()
    for item in sorted_data:
        item_tuple = tuple(item)
        if item_tuple not in seen_items:
            seen_items.add(item_tuple)
            unique_sorted_data.append(item)

    content_map = {}
    # 将行号按文件名分类
    for filename, line_number in unique_sorted_data:
        if filename not in content_map:
            content_map[filename] = []
        content_map[filename].append(line_number)

    # 根据分类的行号生成新的sdx文件内容
    with open(new_filename, 'w') as new_file:
        for filename, line_numbers in content_map.items():
            # 指定文件不参与生成
            name_num = re.search(r'(\d+)\.sdx$', filename)
            if name_num:
                name_num = int(name_num.group(1))
            if name_num==0 or name_num>58:
                continue
            with open(filename, 'r') as original_file:
                lines = original_file.readlines()
            for line_num in line_numbers:
                new_file.write(lines[line_num])