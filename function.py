import const
import pandas as pd
import requests
from const import MAX_ROW_CNT


def processing_data_frame(df, year='', month='', totaling='', method='', category='', category_detail='', shop='', genre='', item='', memo='', price_sort=False, score_sort=False, all_show=False, visit_group=False):
    if year:
            df = df[df['日付'].str.contains(year)]
    if month:
            df = df[df['日付'].str.contains(f'-{month}-')]
    if totaling:
        df = df[df['集計の設定'].str.contains(totaling)]
    if method not in ['全て']:
        df = df[df['方法'] == const.METHOD_LIST[method]]
    if category:
        df = df[df['カテゴリ'].str.contains(category)]
    if category_detail:
        category_detail = category_detail.replace('(', '\(').replace(')', '\)')
        df = df[df['カテゴリの内訳'].str.contains(category_detail)]
    if shop:
        df = df[df['お店'].str.lower().str.replace(' ', '').str.contains(shop.lower().replace(' ', ''))]
    if genre:
        df = df[df['ジャンル'].str.contains(genre)]
    if item:
        df = df[df['品目'].str.lower().str.contains(item.lower())]
    if memo:
        df = df[df['メモ'].str.lower().str.contains(memo.lower())]
    if price_sort:
        df = df.sort_values(['通貨変換前の金額'], ascending=False)
    if score_sort:
        df = df[df['点数'] > 0].sort_values(['点数', '件数'], ascending=False)
    if not all_show:
        df = df[~df['カテゴリの内訳'].isin(['投資', 'ホテル代'])]
    if visit_group:
        df = df[~df['カテゴリの内訳'].str.contains('割り勘')]
        df1 = df.groupby('お店').count()['日付']
        df2 = df.groupby('お店').sum()['通貨変換前の金額']
        df3 = pd.concat([df1, df2], axis=1)
        df3.columns = ['訪問回数', '合計金額']
        df3['平均金額'] = (df3['合計金額'] / df3['訪問回数']).astype('int')
        df3 = df3.sort_values(['訪問回数', '合計金額'], ascending=False)
        df4 = df.sort_values('日付')
        df4 = df4[~df4.duplicated('お店', keep='last')][['お店', '日付']]
        df5 = pd.merge(df3, df4, on='お店')
        df5.columns = ['お店', '訪問回数', '合計金額', '平均金額', '最終訪問日']
        df = df5.reindex(columns=const.SHOW_COLS_2)
    return df


def extract_category(df):
    category_dict = {}
    for category in const.PAYMENT_CATEGORY_LIST:
        category_dict[category] = sorted(set(df[df['カテゴリ'] == category]['カテゴリの内訳']))
    return category_dict


def insert_tree(tree, df, is_group):
    # レイアウト
    show_cols = const.SHOW_COLS_2 if is_group else const.SHOW_COLS_1
    data_frame_layout = const.DATA_FLAME_LAYOUT_2 if is_group else const.DATA_FLAME_LAYOUT_1

    # ツリーを全削除
    for i in tree.get_children():
        tree.delete(i)
    # 再描画
    df = df.reindex(columns=show_cols)
    df = df.iloc[0:MAX_ROW_CNT]
    for i, row in enumerate(df.itertuples()):
        row = list(row)
        if not is_group:
            # 一覧に入力
            award_str = ''
            # 金額の3桁カンマ
            row[5] = f'￥{"{:,}".format(row[5])}'
            # 点数
            row[7] = '' if row[7] == 0 else '{:.2f}'.format(row[7])
            # 件数
            row[8] = '' if row[8] == 0 else row[8]
        else:
            # 訪問回数
            row[3] = f'{row[3]}回'
            # 金額の3桁カンマ
            row[4] = f'￥{"{:,}".format(row[4])}'
            row[5] = f'￥{"{:,}".format(row[5])}'
        # treeviewに格納
        tree.insert("", "end", tags=i, values=[i+1] + list(row[1:len(data_frame_layout)+1]))
        if i % 2 == 0:
            tree.tag_configure(i, background="#ffffff")
        elif i % 2 == 1:
            tree.tag_configure(i, background="#d5ffef")


# def load_csv(url):
#     # driver = webdriver.Chrome(driver_path)
#     # driver.get(URL)
#     # driver.find_element_by_class_name('new_addToCart').click()
#     # driver.quit()
# from selenium import webdriver
# from time import sleep
# driver = webdriver.Chrome('C:/Users/world/git/zaim_view/chromedriver')
# driver.get('https://content.zaim.net/home/money')
# # WebDriverWait(driver, WAIT_SECOND).until(EC.presence_of_element_located((By.CLASS_NAME, 'Btn')))
# # driver.find_element_by_class_name('form-horizontal download-money').click()
# # driver.quit()