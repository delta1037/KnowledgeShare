# author: delta1037
# Date: 2022/01/02
# mail:geniusrabbit@qq.com

import csv

# 源文件的CSV格式
import os.path

from configuration_service import ConfigurationService

CSV_SRC_EXPLAIN = ["topic", "ideas", "attributes", "chapter"]
SUBSECTION_SPLIT_STR = "——————————————————————————\n"
SUBSECTION_SPLIT_STR_WITHOUT_N = "——————————————————————————"


# 读取csv格式文件成表格形式
def get_csv_src(csv_name, csv_format):
    src_csv_file = open(csv_name, "r", encoding='UTF-8')
    reader = csv.reader(src_csv_file)

    res_table = []
    for item in reader:
        if reader.line_num == 1:
            continue
        item_construct = {}
        index = 0  # 行索引
        for i in csv_format:
            item_construct[i] = item[index]
            index = index + 1
        res_table.append(item_construct)
    src_csv_file.close()
    return res_table


# 读取输出分类格式
def get_csv_classify(csv_name):
    classify_csv_file = open(csv_name, "r", encoding='UTF-8')
    reader = csv.reader(classify_csv_file)

    res_dic = {}
    for item in reader:
        res_dic[item[0]] = item[1]
    classify_csv_file.close()
    return res_dic


# latex文件输出格式控制

# 文本转码
def trans_code(text_src):
    text_src = text_src.replace("\\", "\\\\")
    text_src = text_src.replace('#', '\\#')
    text_src = text_src.replace('&', '\\&')
    return text_src


# 1、文件头内容
def latex_head(handle, chapter):
    head = "\\chapterimage{chapter_head_2.pdf}\n\\chapter{%s}\n\n" % trans_code(chapter)
    # print(head)
    handle.write(head)


# 2、章节头 section
def latex_section(handle, topic):
    section = "\\section{%s}\\index{%s}\n\n" % (trans_code(topic), trans_code(topic))
    handle.write(section)
    handle.write("\n\n")


# 2、章节头 section，只有单个内容的输出
def latex_section_single(handle, topic, idea):
    section = "\\section{%s}\\index{%s}\n\n" % (trans_code(topic), trans_code(topic))
    handle.write(section)
    handle.write(trans_code(idea).replace('\r', '').replace("\n", "\n\n"))
    handle.write("\n\n")


# 2、章节头 section，section的注意事项
def latex_section_attention(handle, idea):
    handle.write(trans_code(idea).replace('\r', '').replace("\n", "\n\n"))
    handle.write("\n\n")


# 3、子章节 subsection
def latex_subsection(handle, topic, subtopic, idea):
    subsection = "\\subsection{%s}\\index{%s!%s}\n\n" % (trans_code(subtopic), trans_code(topic), trans_code(subtopic))
    handle.write(subsection)
    handle.write(trans_code(idea).replace('\r', '').replace("\n", "\n\n"))
    handle.write("\n\n")


# 解析ideas的内容，分解成section和subsection
def parser_ideas(handle, line):
    # 先解析line["topic", "ideas", "attributes", "chapter"]

    # 一行内有多个内容的先做分割
    if line["ideas"].find(SUBSECTION_SPLIT_STR) != -1:
        # 多个内容分解成subsection
        ideas_array = line["ideas"].split(SUBSECTION_SPLIT_STR)
        latex_section(handle=handle, topic=line["topic"])
        for idea_raw in ideas_array:
            # 判断是否是注意事项或者备注
            if idea_raw[0:2] == "注意" or idea_raw[0:2] == "备注":
                latex_section_attention(
                    handle=handle,
                    idea=idea_raw.replace(SUBSECTION_SPLIT_STR_WITHOUT_N, ''))
            else:
                # 对每一个idea解析出来subtopic
                # print("############# idea_raw:" + idea_raw)
                subtopic = idea_raw.split('\n')[0].strip(': ：')  # 获取到第一行内容，处理成subsection
                idea = idea_raw[idea_raw.index('\n') + 1:]
                # print("############# idea:" + idea)
                latex_subsection(
                    handle=handle,
                    topic=line["topic"],
                    subtopic=subtopic,
                    idea=idea.replace(SUBSECTION_SPLIT_STR_WITHOUT_N, ''))
    else:
        # 单个内容直接输出
        latex_section_single(handle=handle,
                             topic=line["topic"],
                             idea=line["ideas"].replace(SUBSECTION_SPLIT_STR_WITHOUT_N, ''))


# 查找表格，按照指定的内容输出
def output_latex(ideas_table, classify, output_dir):
    # 遍历classify字典
    for item in classify:
        # 获取到输出文件句柄
        output_file = classify[item]
        file_handle = open(output_dir + "\\" + output_file, "w+", encoding='UTF-8')
        # 输出文件头
        latex_head(file_handle, item)
        # 遍历源table文件
        for line in ideas_table:
            # 过滤不属于本章节的内容
            if line["chapter"] != item:
                continue

            # 解析内容，并写入到文件中
            parser_ideas(file_handle, line)

        # 关闭文件
        file_handle.flush()
        file_handle.close()


if __name__ == '__main__':
    config = ConfigurationService()
    input_dir = config.get_key("input_dir")
    classify_dic = get_csv_classify(input_dir + "\\" + config.get_key("classify_file"))
    # print(classify_dic)
    csv_table = []
    for file in config.get_key("handout_file"):
        csv_table = csv_table + get_csv_src(csv_name=(input_dir + "\\" + file),
                                            csv_format=config.get_key("csv_src_format"))
    print("笔记条目数", len(csv_table))

    # 合成输出路径
    # print(os.path.abspath(os.path.dirname(os.getcwd())))
    root_dir = os.path.abspath(os.path.dirname(os.getcwd())) + "\\"
    output_path = root_dir + config.get_key("output_filename")
    print("output dir path: ", output_path)
    # 送入解析
    print("Start parser...")
    output_latex(ideas_table=csv_table, classify=classify_dic, output_dir=output_path)
    print("End parser")
