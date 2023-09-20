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
python .\FrameSimplifier.py -s D:\test\script\3dmark-org\3DMark_FireStrike-orgSize-FixFPS0.5-GT1\vector\ -f 112 -b 113 -n 1 -m -1
```
默认保存在`vector` 的同级目录frame下
-f 第一个有画面的索引
-b 想要dump的文件索引号
-n 想要dump几个
-m -1 保留所有Draw
-m 0,保留从某个位置开始一直到这个位置结尾的draw，偏移含义

# 打包成exe可执行文件

``` 
pyinstaller -F --console FrameSimplifier.py
```