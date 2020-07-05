# cofing: utf-8
# reshape hasc logger's data

import os

import numpy as np

import pandas as pd


def get_acc_list_from_label_csv(data_dir_path="./") -> [list, pd.DataFrame]:
    # label_pathに保存されているcsvファイルより加速度のファイルパスを抽出，リスト化しreturnする
    label_path = data_dir_path + "y.csv"
    new_label_path = data_dir_path + "y_new.csv"
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

    # nan を消して使えるデータのみ残す
    label_df_csv = label_df.dropna(
        subset=["Height", "Weight", "acc_file_path"])
    acc_data_list = label_df_csv["acc_file_path"].values
    label_df_csv.to_csv(new_label_path, index=False)
    return acc_data_list, label_df_csv


def fetch_and_save_data(acc_path_list: [str], data_dir_path="./") -> [np.ndarray]:
    # fetch acc data, save x.csv
    # return acc data.
    data_path = data_dir_path + "x.csv"
    acc_data_list = []
    # TODO saveできない．うまく処理してください

    for path in acc_path_list:
        acc = np.loadtxt(path, delimiter=",").T[1:]
        print(acc.shape)
        acc_data_list.append(acc.reshape())
    # print(np.ndarray(acc_data_list).shape)
    # np.savetxt(data_path, acc_data_list)
    print("saved :", data_path)
    return acc_data_list


def crop_data(acc_data_list: [np.ndarray], clip_size=256, strides=128) -> [[np.ndarray], [int]]:
    # return cropped_acc_data, num_of_separate
    cropped_acc_data = []
    num_of_separate = []

    for acc in acc_data_list:
        full_size = acc.shape[1]
        print(full_size)
        # TODO cropping方法の検討
    return cropped_acc_data, num_of_separate


def make_new_label_csv(label: pd.DataFrame, cropped_data_list: [np.ndarray], separate_num: [int], data_dir_path="./") -> bool:
    # make new DataFrame, save y_crop.csv
    # make cropped_data_file: x_crop.csv
    # return success?
    data_path = data_dir_path + "x_crop.csv"
    label_path = data_dir_path + "y_crop.csv"
    return False


if __name__ == "__main__":
    data_dir_path = "./data/"

    acc_path_list, label_df = get_acc_list_from_label_csv(
        data_dir_path=data_dir_path)

    acc_data_list = fetch_and_save_data(
        acc_path_list=acc_path_list, data_dir_path=data_dir_path)

    exit()
    cropped_data_list, separate_num = crop_data(
        acc_data_list=acc_data_list, clip_size=256, strides=128)

    make_new_label_csv(label=label_df, cropped_data_list=cropped_data_list,
                       separate_num=separate_num, data_dir_path=data_dir_path)
