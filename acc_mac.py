# cofing: utf-8
# reshape hasc logger's data

import os

import numpy as np

import pandas as pd


def get_acc_list_from_label_csv(label_path="./", new_label_path="./") -> [list, pd.DataFrame]:
    # folder_pathのフォルダから加速度のファイルを抽出，リスト化しreturnする
    # TODO 今mainでやってる更新作業，新しいdfの定義をここでやりたい
    acc_data_list = []

    label_df = pd.read_csv(label_path)

    meta_list = label_df["Path"].values
    for name in meta_list:
        root, ext = os.path.splitext(name)
        csv_path = root + "-acc.csv"
        if not os.path.exists(csv_path):
            csv_path = np.nan
        acc_data_list.append(csv_path)

    label_df["acc_file_path"] = acc_data_list
    label_df.to_csv(label_path, index=False)
    print("update", label_path)

    label_df_csv = label_df.dropna(
        subset=["Height", "Weight", "acc_file_path"])
    acc_data_list = label_df_csv["acc_file_path"].values
    label_df_csv.to_csv(new_label_path, index=False)
    return acc_data_list, label_df_csv


def fetch_and_save_data(acc_path_list: [str]) -> [np.ndarray]:
    # fetch acc data, save x.csv
    # return acc data.
    acc_list = []
    for path in acc_path_list:
        acc = np.loadtxt(path, delimiter=",").T[1:]
        acc_list.append(acc)
    # TODO save
    return acc_list


def clip_data(acc_data_list: [np.ndarray], clip_size=256, strides=128) -> [[np.ndarray], [int]]:
    # return clipped_acc_data, num_of_separate
    acc_data = []
    num_of_data = []

    for acc in acc_data_list:
        full_size = acc.shape[1]
        print(full_size)
        # TODO clipping部分
    return acc_data, num_of_data


def make_new_label_csv(label: pd.DataFrame, acc_data_list: [np.ndarray], separate_num: [int]) -> bool:
    # make new DataFrame, save y_clip.csv
    # make acc_data_file: x_clip.csv
    # return success?

    return False


if __name__ == "__main__":
    label_path = "./data/y.csv"
    new_label_path = "./data/y_acc.csv"
    acc_path_list, label_df = get_acc_list_from_label_csv(
        label_path=label_path, new_label_path=new_label_path)

    acc_data_list = fetch_and_save_data(acc_path_list=acc_path_list)

    # new_data_list, separate_num = clip_data(
    #     acc_data_list=acc_data_list, clip_size=256, strides=128)

    # make_new_label_csv(label=label_df, acc_data_list=new_data_list,
    #                    separate_num=separate_num)
