# FullLogScript-FrameSimplifier

## Description
简化0-n的脚本，使其更加简洁，易读，易用。
初始：0，1，2，3，n.sdx,
省去中间不显示图像的sdx
结果：0，1，2，3...

## Usage
```python main.py```

main.py的参数说明：
```
start_draw_index=968  # 假设所有的脚本有1088个Draw调用，那么从第968个开始，到最后一个，都是需要保留的，前面的都是不需要的，968是一个随机数字，需要根据实际情况修改
first_frame_index=49 # 第一帧有实际图像输出文件序号

src_path = r"vector\\" # 源sdx脚本所在路径
tmp_path = "output\\" # 临时文件输出路径，删去了原有sdx文件中换行，使得更整洁
target_path = "test-script\\" # 目标文件输出路径，最终的脚本文件
```

# 打包成exe可执行文件

``` 
pyinstaller -F --console main.py
```