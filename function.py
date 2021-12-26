import const
import re
import time


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
    df = df.iloc[0:200]
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