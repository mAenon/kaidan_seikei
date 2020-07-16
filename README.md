# HASC data shaping

## データ計測時の注意
***
- Comment  
身長(double), 体重(double), 性別(m / f), 階段のタイプ(l /  h / f)  
の4つ


- Tags  
一つまで

## 注意
***
pythonわからんなのでmacとwinで使うファイルが違う

## label_win.py / label_mac.py
***
ちょっと編集してmetaデータのあるフォルダをちゃんと指定する必要がある

metaデータよりlabelデータを作成  
***./data/y.csv***  
にラベルデータを保存

## acc_win.py / acc_mac.py
***
**label_ *hogehoge*.py** により作成したメタデータファイルを読み込み，加速度データファイルパスを追記して ***y.csv*** を更新

欠損を含んだ使えないデータを含んだラベルを削除し  
***./data/y_new.csv***  
に新たなラベルデータを保存

作成したラベルデータを基に加速度データをそのままの形で
取得・加速度ファイルを作成  
***./data/x.csv***  
に生のセンサデータを保存(時間軸情報は時系列情報のみ残る)

- 注意  
mac標準のnumbersでは作成した生加速度データファイルの列数が多すぎてうまく表示できないのでtxtファイルに保存推奨

データの先端，末端を落とし，クロッピングしたデータを  
***./data/x_crop.csv***  
に保存

クロッピングデータに対応したラベルデータファイルを  
***./data/y_crop.csv***  
に保存

クロッピングの際の端のデータについて， ***crop_data*** 関数の引数 **how** で指定可能
```python
cropped_data_list, separate_num =
    crop_data(acc_data_list, how="throw")
```
としたときは端数のデータを捨てる

```python
cropped_data_list, separate_num =
    crop_data(acc_data_list, how="strides")
```
としたときは端数のデータをストライド幅を調整して残す

## acc_drop_mac.py
***
***actor*** を参照し，ある数人について，削除して  
***x_drop.csv*** ***y_crop_drop.csv*** ***x_crop_drop.csv***  
にする