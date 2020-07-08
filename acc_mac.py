# cofing: utf-8
# reshape hasc logger's data

import os

import csv

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


def fetch_and_save_data(acc_path_list: [str], data_dir_path="./") -> [[np.ndarray]]:
    # fetch acc data, save x.csv
    # return acc data.
    # mac だとnumbersの仕様でうまく動かないので，txtファイルに保存推奨
    data_path = data_dir_path + "x.csv"
    acc_data_list = []

    for path in acc_path_list:
        acc = np.loadtxt(path, delimiter=",").T[1:]
        # 僕にはこうしないと無理
        for i in range(acc.shape[0]):
            acc_data_list.append(acc[i])
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(acc_data_list)
    print("saved :", data_path)
    return acc_data_list


def crop_data(acc_data_list: [[np.ndarray]], crop_size=256, strides=128, del_head=50, del_tail=20, how="throw") -> [[np.ndarray], [int]]:
    # return cropped_acc_data, num_of_separate
    # acc data list = 2 demention data list [xyzxyzxyzxyz.....]
    # how = "throw" or "strides"
    if how == "strides":
        how = False
    else:
        how = True

    x_data = []
    y_data = []
    z_data = []
    target_data_list = [x_data, y_data, z_data]

    cropped_acc_data = []
    num_of_separate = []

    for i, acc in enumerate(acc_data_list):
        # target data save
        target_data = target_data_list[i % 3]
        acc = acc[del_head: -del_tail]
        target_data.append(acc)

    for x, y, z in zip(x_data, y_data, z_data):
        maxlen = len(x)
        cropping_num = maxlen // crop_size
        if ~how:
            cropping_num += 1

        for i in range(cropping_num):
            if ~how and i == cropping_num - 1:
                cropped_acc_data.append(x[-crop_size:])
                cropped_acc_data.append(y[-crop_size:])
                cropped_acc_data.append(z[-crop_size:])
                break

            cropped_acc_data.append(x[0 + crop_size * i: crop_size * (i + 1)])
            cropped_acc_data.append(y[0 + crop_size * i: crop_size * (i + 1)])
            cropped_acc_data.append(z[0 + crop_size * i: crop_size * (i + 1)])
        num_of_separate.append(cropping_num)

    return cropped_acc_data, num_of_separate


def make_new_label_csv(label: pd.DataFrame, cropped_data_list: [np.ndarray], separate_num: [int], data_dir_path="./") -> bool:
    # make new DataFrame, save y_crop.csv
    # make cropped_data_file: x_crop.csv
    # return success?
    data_path = data_dir_path + "x_crop.csv"
    label_path = data_dir_path + "y_crop.csv"
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(cropped_data_list)
    return False


if __name__ == "__main__":
    data_dir_path = "./data/"

    acc_path_list, label_df = get_acc_list_from_label_csv(
        data_dir_path=data_dir_path)

    acc_data_list = fetch_and_save_data(
        acc_path_list=acc_path_list, data_dir_path=data_dir_path)

    cropped_data_list, separate_num = crop_data(
        acc_data_list=acc_data_list, crop_size=256, strides=128, del_head=40, del_tail=20, how="throw")

    make_new_label_csv(label=label_df, cropped_data_list=cropped_data_list,
                       separate_num=separate_num, data_dir_path=data_dir_path)
