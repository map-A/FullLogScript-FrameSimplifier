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
scene_begins_index= 53 # 首次出现画面的文件序号，比如3DMark_CloudGate-orgSize-FixFPS0.5-GT1脚本中是在_53.sdx中首次出现画面
save_start_index= 53 # 保存文件的起始序号，比如从3DMark_CloudGate-orgSize-FixFPS0.5-GT1/vector 的_53.sdx保存，
n = 3 # 表示从53帧的连续3帧
src_path = r"vector\\" # 源sdx脚本所在路径

```
默认保存在`src_path` 的同级目录下。
# 打包成exe可执行文件

``` 
pyinstaller -F --console main.py
```