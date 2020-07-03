# cofing: utf-8
# reshape hasc logger's data

import os
import re

import numpy as np

import pandas as pd


def get_meta_list_from_path(folder_path=".\\") -> list:
    # folder_pathのフォルダから拡張子がmetaのファイルを抽出，リスト化しreturnする

    meta_data_list = []

    if folder_path[-1] != "\\":
        folder_path += "\\"
    dirlist = os.listdir(folder_path)

    for name in dirlist:
        if os.path.isdir(name):
            continue

        root, ext = os.path.splitext(name)
        if ext == ".meta":
            meta_data_list.append(folder_path + name)
    return meta_data_list


def get_comment_from_meta_file(meta_list=[]) -> dict:
    # meta data list -> comment's dictionary

    comment_list = {}
    for i, meta_file in enumerate(meta_list):
        with open(meta_file) as f:
            line = f.readline().rstrip()
            while line:
                if line.startswith("Comment"):
                    comment_list[i] = line
                    break
                line = f.readline().rstrip()
    return comment_list


def get_terminalid_from_meta_file(meta_list=[]) -> dict:
    # meta data list -> TerminalID's dictionary

    terminal_id_list = {}
    for i, meta_file in enumerate(meta_list):
        with open(meta_file) as f:
            line = f.readline().rstrip()
            while line:
                if line.startswith("TerminalID"):
                    terminal_id_list[i] = line
                    break
                line = f.readline().rstrip()
    return terminal_id_list


def get_tags_from_meta_file(meta_list=[]) -> dict:
    # meta data list -> tags' dictionary

    tags_list = {}
    for i, meta_file in enumerate(meta_list):
        with open(meta_file) as f:
            line = f.readline().rstrip()
            while line:
                if line.startswith("Tags"):
                    tags_list[i] = line
                    break
                line = f.readline().rstrip()
    return tags_list


def comment_to_info(comment_dict: dict) -> list:
    # comment's dictionary -> height, weight, gender, type dictionaries' list
    # return : list of dict
    height = {}
    weight = {}
    sex = {}
    species = {}

    for key, strs in comment_dict.items():
        info = re.findall(r"[\d\.]+|,m|,f|,l|,h", strs)
        if len(info) < 3 or len(info) > 4:
            height[key] = None
            weight[key] = None
            sex[key] = None
            species[key] = None
        elif len(info) == 3:
            # どこが抜けているかわからなくてめっちゃ面倒
            # 今回の場合は性別が抜けているパターンと階段の種類が抜けているパターンがある
            height[key] = float(info[0])
            weight[key] = float(info[1])
            if info[2] == "m":
                sex[key] = "m"
                species[key] = None
            else:
                sex[key] = "f"
                species[key] = info[2].lstrip(",")
        elif len(info) == 4:
            height[key] = float(info[0])
            weight[key] = float(info[1])
            sex[key] = info[2].lstrip(",")
            species[key] = info[3].lstrip(",")

    return height, weight, sex, species


def tags_to_info(tags_dict: dict) -> dict:
    # tags' dictionary -> activity's dictinary
    activity = {}

    for key, strs in tags_dict.items():
        info = re.findall(r" \D+", strs)
        activity[key] = info[0].strip()
    # print(activity)
    return activity


def make_df_from_dicts(len_of_data: int, dict_list: list, dict_dict: dict) -> pd.DataFrame:
    # dictionaries -> DataFrame
    data_list = []

    for i in range(len_of_data):
        tmp_list = []
        for dict_name in dict_list:
            if i in dict_dict[dict_name]:
                tmp_list.append(dict_dict[dict_name][i])
            else:
                tmp_list.append(None)
        data_list.append(tmp_list)

    return pd.DataFrame(data_list, index=np.arange(len_of_data), columns=dict_list)


def to_act_num(label_df: pd.DataFrame) -> pd.Series:
    # labeling

    # 0 = high down
    # 1 = low down
    # 2 = Walk
    # 3 = low up
    # 4 = high up
    # 5 = other
    act_num = []

    activity = label_df["Activity"].values
    types = label_df["Type"].values

    for i, act in enumerate(activity):
        if act == "Walk":
            act_number = 2
        elif act == "Up":
            if types[i] == "l":
                act_number = 3
            else:
                act_number = 4
        elif act == "Down":
            if types[i] == "l":
                act_number = 2
            else:
                act_number = 1
        else:
            act_number = 5

        act_num.append(act_number)

    return pd.Series(act_num)


if __name__ == "__main__":
    home = os.path.expanduser("~")
    data_dir = home + "\\Desktop\\階段データセット7-3計測"
    print("search in : ", data_dir)

    meta_list = get_meta_list_from_path(data_dir)
    print("found {} meta data files".format(len(meta_list)))

    tags_dict = get_tags_from_meta_file(meta_list=meta_list)
    # print(tags_list)
    comment_dict = get_comment_from_meta_file(meta_list=meta_list)
    # print(comment_list)
    terminal_id_dict = get_terminalid_from_meta_file(meta_list=meta_list)
    # print(terminal_id_list)
    height, weight, gender, species = comment_to_info(comment_dict=comment_dict)
    # print(height, weight, gender, species)
    activity = tags_to_info(tags_dict=tags_dict)
    # print(activity)

    meta_dict = dict(zip(range(len(meta_list)), meta_list))
    # print(meta_dict)

    label_df = make_df_from_dicts(len(meta_list),
                                  ("Activity", "Type", "Height", "Weight", "Gender", "Path", "TerminalID", "Comment", "Tags"),
                                  {"Activity": activity, "Type": species, "Height": height, "Weight": weight, "Gender": gender, "Tags": tags_dict, "Comment": comment_dict, "TerminalID": terminal_id_dict, "Path": meta_dict})

    label_df["act_num"] = to_act_num(label_df)

    # 並び替え
    label_df = label_df[["Activity", "Type", "act_num", "Height", "Weight", "Gender", "Path", "TerminalID", "Comment", "Tags"]]

    label_df.to_csv(".\\data\\y.csv")
    print("saved in '.\\data\\y.csv'")
