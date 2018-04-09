## description
md格式协议稿模型解析,自动生成iOS与Android代码

## 使用效果:
 ![image](/1.gif)

 ## 注意事项:
   1. 生成的模型代码在md目录的(`iOS`|`android`)文件夹下
   * 默认读取md中的`# Title`作为类名，为默认值或不存在时，使用md文件名
   * 支持的列表解析格式为`list<xxx>`, `array<xxx>`, `[xxx]`,不用区分大小写
   * 不支持Map，Map应该作为另一个模型。
   * 默认iOS使用`MZ`前缀， android使用`Entity`后缀,可在`ObjcParser.py`和`AndroidParser.py`中修改


## usage
```shell
  python 脚本路径 模型路径(不填使用当前目录,可以是目录或文件) 参数(1 iOS, 2 android, 不填默认为iOS)
```

### 示例
```shell
  #示例1
  cd /workspace/beauty-api-doc/数据模型
  python /workspace/md-model-generator.py
  #示例2
  cd /workspace/beauty-api-doc/数据模型
  python /workspace/md-model-generator.py 2
  #示例3
  python /workspace/md-model-generator.py /workspace/beauty-api-doc/数据模型
  #示例4
  python /workspace/md-model-generator.py /workspace/beauty-api-doc/数据模型 2
```

## python version
v2.7

## dependency
无
