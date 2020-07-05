# cofing: utf-8
# reshape hasc logger's data

import os
import re

import numpy as np

import pandas as pd


def get_meta_list_from_path(folder_path=".\\") -> list:
    # folder_pathのフォルダから拡張子がmetaのファイルを抽出，リスト化しreturnする

    meta_data_list = []

    if folder_path[-1] != "/":
        folder_path += "/"
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
        info = re.findall(r"[\d\.]+|,\D", strs)
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


def identify_acter(label_df: pd.DataFrame) -> pd.Series:
    # TODO 辞書での処理に変更する
    # ↑配列での処理をするとNoneの部分について処理してしまってうまく動かないので

    # TODO Noneの含まれている列について，うまく処理されずデータフレームの末端が空白になっている　→　配列の処理から辞書での処理に変更することで対処可能かも
    # XXX 上記のせいでto_categorical, astype(np.int)がうまく動作しない

    # TODO label_df["actor"]が実数値にならない

    # ------------------
    # array版
    # ------------------
    #
    # duplicated_label = label_df[~label_df[["Height", "Weight"]].duplicated()][[
    #     "Height", "Weight"]].values
    # num_of_actor = []
    # for i, *d in enumerate(duplicated_label):
    #     num_of_actor.append([i, d])

    # flag = 0
    # for i in range(len(num_of_actor)):
    #     if np.isnan(num_of_actor[i][1][0][0]):
    #         flag = 1
    #         num_of_actor[i][0] = 0
    #     if flag:
    #         num_of_actor[i][0] -= 1

    # number = []
    # for i in range(len(label_df.index)):
    #     for j in range(len(num_of_actor)):
    #         if label_df.iloc[i]["Height"] == num_of_actor[j][1][0][0] and label_df.iloc[i]["Weight"] == num_of_actor[j][1][0][1]:
    #             number.append(int(j))
    # return pd.Series(number)
    # -------------------
    # array版
    # -------------------
    # ------------------------------------------------------------ #
    # -------------------
    # distionary版
    # -------------------

    # 人の番号付け
    # 1.番号付用の配列生成
    # 2.番号付用の辞書生成
    # 3.番号の配列生成
    # 4.Seriesにして返す

    # 1.番号付用の配列生成
    duplicated_array = label_df[~label_df[["Height", "Weight"]].duplicated()][[
        "Height", "Weight"]].values

    # 2.番号付用の辞書生成
    actor_dict = {}
    flag = False
    for i, value in enumerate(duplicated_array):
        value = value.tolist()
        if flag:
            actor_dict[i - 1] = value
            continue
        elif np.isnan(value[0]):
            flag = True
            actor_dict[len(duplicated_array) - 1] = value
            continue
        else:
            actor_dict[i] = value
            continue

    # 3.番号の配列生成
    num_of_actor = []
    value_list = label_df[["Height", "Weight"]].values
    for values in value_list:
        for num, value in actor_dict.items():
            if np.isnan(values[0]) and np.isnan(values[1]):
                if np.isnan(value[0]) and np.isnan(value[1]):
                    num_of_actor.append(num)
                    break
            elif values[0] == value[0] and values[1] == value[1]:
                num_of_actor.append(num)
                break

    # 4.series化して返す
    return pd.Series(num_of_actor)


if __name__ == "__main__":
    home = os.path.expanduser("~")
    data_dir = home + "/Desktop/dataset-0703"
    print("search in : ", data_dir)

    meta_list = get_meta_list_from_path(data_dir)
    print("found {} meta data files".format(len(meta_list)))

    tags_dict = get_tags_from_meta_file(meta_list=meta_list)
    # print(tags_list)
    comment_dict = get_comment_from_meta_file(meta_list=meta_list)
    # print(comment_list)
    terminal_id_dict = get_terminalid_from_meta_file(meta_list=meta_list)
    # print(terminal_id_list)
    height, weight, gender, species = comment_to_info(
        comment_dict=comment_dict)
    # print(height, weight, gender, species)
    activity = tags_to_info(tags_dict=tags_dict)
    # print(activity)

    meta_dict = dict(zip(range(len(meta_list)), meta_list))
    # print(meta_dict)

    label_df = make_df_from_dicts(len(meta_list),
                                  ("Activity", "Type", "Height", "Weight", "Gender",
                                   "Path", "TerminalID", "Comment", "Tags"),
                                  {"Activity": activity, "Type": species, "Height": height, "Weight": weight, "Gender": gender, "Tags": tags_dict, "Comment": comment_dict, "TerminalID": terminal_id_dict, "Path": meta_dict})

    # 行動の番号付
    label_df["act_num"] = to_act_num(label_df)

    # 人の番号付
    label_df["actor"] = identify_acter(label_df)

    # 並び替え
    label_df = label_df[["Activity", "Type", "act_num", "actor", "Height",
                         "Weight", "Gender", "Path", "TerminalID", "Comment", "Tags"]]

    print(label_df.head())
    print(type(label_df["actor"].values[0]))
    if not os.path.exists("./data"):
        os.mkdir("./data")
    label_df.to_csv("./data/y.csv", mode="w")
    print("saved in './data/y.csv'")
