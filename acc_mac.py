# cofing: utf-8
# reshape hasc logger's data

import os

import numpy as np

import pandas as pd


def get_acc_list_from_label_csv(label_path="./") -> [list, pd.DataFrame]:
    # folder_pathのフォルダから加速度のファイルを抽出，リスト化しreturnする

    acc_data_list = []

    label_df = pd.read_csv(label_path)

    meta_list = label_df["Path"].values
    for name in meta_list:
        root, ext = os.path.splitext(name)
        csv_path = root + "-acc.csv"
        if not os.path.exists(csv_path):
            csv_path = ""
        acc_data_list.append(csv_path)
    return acc_data_list, label_df


def clip_data(acc_list: list, clip_size=256, strides=128) -> [[np.ndarray], list]:
    # return acc_data, num_of_data
    acc_data = []
    num_of_data = []

    for path in acc_list:
        acc = np.loadtxt(path, delimiter=",").T[1:, :]
        full_size = acc.shape[1]
        print(full_size)
        # TODO clipping部分
    return acc_data, num_of_data


if __name__ == "__main__":
    label_path = "./data/y.csv"
    new_label_path = "./data/y_acc.csv"
    acc_list, label_df = get_acc_list_from_label_csv(label_path)
    label_df["acc_file_path"] = acc_list
    label_df["acc_file_path"].replace("", np.nan, inplace=True)
    label_df.to_csv(label_path, index=False)
    print("update", label_path)

    label_df_csv = label_df.dropna(
        subset=["Height", "Weight", "acc_file_path"])
    acc_list = label_df_csv["acc_file_path"].values
    label_df_csv.to_csv(new_label_path, index=False)

    new_data_list = clip_data(acc_list=acc_list, clip_size=256, strides=128)
