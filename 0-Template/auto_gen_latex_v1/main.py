# author: delta1037
# Date: 2022/01/02
# mail:geniusrabbit@qq.com

import csv
import pandas as pd

from configuration_service import config

SUBSECTION_SPLIT = config.get_key("section_content_divider")
SUBSECTION_SPLIT_LF = SUBSECTION_SPLIT + "\n"
SUBSECTION_SPLIT_CRLF = SUBSECTION_SPLIT + "\r\n"


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
    # text_src = text_src.replace("\\", "\\\\")
    text_src = text_src.replace('#', '\\#')
    text_src = text_src.replace('&', '\\&')
    return text_src


# 1、文件头内容
def latex_head(handle, chapter):
    head = "\\chapterimage{chapter_head_2.pdf}\n\\chapter{%s}\n\n" % trans_code(chapter)
    # print(head)
    handle.write(head)


# 2、章节头 section
def latex_section(handle, section_name=None, section_content=None):
    section_name = str(section_name)
    section_content = str(section_content)

    if section_name != "None":
        section = "\\section{%s}\\index{%s}\n\n" % (trans_code(section_name), trans_code(section_name))
        handle.write(section)
    if section_content != "nan" and section_content != "None" and str(section_content) != "":
        handle.write(trans_code(section_content).replace('\r', '').replace("\n", "\n\n"))
        handle.write("\n\n")


# 3、子章节 subsection
def latex_subsection(handle, section_name=None, sub_section_name=None, subsection_content=None, check_content=False):
    section_name = str(section_name)
    sub_section_name = str(sub_section_name)
    subsection_content = str(subsection_content)

    content_valid = (subsection_content != "nan" and subsection_content != "None" and subsection_content != "")
    if check_content and not content_valid:
        return
    if section_name != "None" and sub_section_name != "None":
        subsection = "\\subsection{%s}\\index{%s!%s}\n\n" % (trans_code(sub_section_name), trans_code(section_name), trans_code(sub_section_name))
        handle.write(subsection)
    if subsection_content != "nan" and subsection_content != "None" and subsection_content != "":
        handle.write(trans_code(subsection_content).replace('\r', '').replace("\n", "\n\n"))
        handle.write("\n\n")


# 查找表格，按照指定的内容输出
def output_latex(notes_df, classify_dic):
    # 笔记输出目录定义
    output_dir = config.get_key("output_path")
    # 笔记标题分类表
    notes_col_type_map = config.get_key("csv_src_format")

    # 处理笔记内容
    for item in classify_dic:
        print("解析章节:" + item)
        # 打开输出文件
        output_file = classify_dic[item]
        output_file_handle = open(output_dir + "\\" + output_file, "w+", encoding='UTF-8')

        # 生成文件章节头
        latex_head(output_file_handle, item)
        chapter_col_name = notes_col_type_map["chapter"]
        for idx, row in notes_df.iterrows():
            # 不属于本章节的内容跳过
            if row[chapter_col_name] != item:
                continue
            # 一级标题
            section_name = notes_col_type_map["section_name"]
            latex_section(output_file_handle, section_name=row[section_name])
            # 一级标题下的内容
            section_content_list = notes_col_type_map["section_content"]
            for section_content in section_content_list:
                if section_content not in row:
                    # print(section_content + " not exist")
                    continue
                # 一级标题下的内容做内部分割
                if SUBSECTION_SPLIT_LF not in row[section_content] and SUBSECTION_SPLIT_CRLF not in row[section_content]:
                    latex_section(output_file_handle, section_content=row[section_content])
                else:
                    # 多个内容分解成subsection
                    if SUBSECTION_SPLIT_LF in row[section_content]:
                        subsection_content_list = row[section_content].split(SUBSECTION_SPLIT_LF)
                    else:
                        subsection_content_list = row[section_content].split(SUBSECTION_SPLIT_CRLF)
                    # print(subsection_content_list)
                    for subsection_content in subsection_content_list:
                        # 判断是否是注意事项或者备注
                        if subsection_content[0:2] == "注意" or subsection_content[0:2] == "备注":
                            latex_section(
                                handle=output_file_handle,
                                section_content=subsection_content.replace(SUBSECTION_SPLIT, '')
                            )
                        else:
                            # 对每一个idea解析出来subtopic
                            # print("############# idea_raw:" + idea_raw)
                            subtopic = subsection_content.split('\n')[0].strip(': ：')  # 获取到第一行内容，处理成subsection
                            subsection_content = subsection_content[subsection_content.index('\n') + 1:]
                            # print("############# idea:" + idea)
                            latex_subsection(
                                handle=output_file_handle,
                                section_name=row[section_name],
                                sub_section_name=subtopic,
                                subsection_content=subsection_content.replace(SUBSECTION_SPLIT, ''),
                                check_content=True
                            )

            # 二级标题和二级标题下的内容
            subsection_content_list = notes_col_type_map["subsection_content"]
            for subsection_content in subsection_content_list:
                if subsection_content not in row:
                    # print(subsection_content + " not exist")
                    continue
                latex_subsection(
                    output_file_handle,
                    section_name=row[section_name],
                    sub_section_name=subsection_content,
                    subsection_content=row[subsection_content],
                    check_content=True
                )

        # 关闭文件
        output_file_handle.flush()
        output_file_handle.close()


if __name__ == '__main__':
    # 数据目录
    data_dir = config.get_key("data_dir")

    # 分类字典：key=章节；value=文件名
    _classify_dic = get_csv_classify(data_dir + "\\" + config.get_key("classify_file"))

    # 加载笔记数据
    _notes_df = None
    for file in config.get_key("handout_file"):
        notes_path = data_dir + "\\" + file
        print("加载笔记文件:" + notes_path)
        data_df = pd.read_csv(notes_path, encoding="utf-8")
        # print(_data_df.info())
        if _notes_df is None:
            _notes_df = data_df
        else:
            _notes_df = pd.concat([_notes_df, data_df], ignore_index=True, axis=0)
    if _notes_df is None:
        print("笔记源文件不存在")
        exit(0)
    print("笔记条目数", _notes_df.shape[0])
    # print(_notes_df.info())
    # print(_notes_df)

    # 送入解析
    print("Start parser...")
    output_latex(notes_df=_notes_df, classify_dic=_classify_dic)
    print("End parser")
