# 笔记生成

# 一、环境配置

### 1.1 python

网上很多教程，装一下就行了，可以在`powershell`中执行`py -V`看一下版本信息

### 1.2 配置文件

配置文件名为`config.json`，内容为（附带解释，实际上没有）

```json
{
    # 源文件目录文件夹
    "input_dir" : "input",
    # 分类文件（将知识点归为哪一个章节）
    "classify_file": "classify_dic.csv",
    # 需要处理的笔记源文件
    "handout_file": [
        "handout_0.csv",
        "handout_1.csv",
        "handout_2.csv"
    ],
	# 笔记源文件的格式，其中chapter是分类用的
    "csv_src_format": [
        "topic",
        "ideas",
        "attributes",
        "chapter"],
	# 输出目录，该目录是相对脚本的上级目录
    "output_filename": "sub_chapter"
}
```

-   可以根据需要对`config`文件进行修改；

-   因为脚本与笔记格式绑定，所以笔记源文件格式必须包含`["topic","ideas","attributes","chapter"]`这些内容

## 二、执行

在`powershell`中执行`py main.py`即可，生成好的文件会输出到配置中`output_filename`所指定的目录中

