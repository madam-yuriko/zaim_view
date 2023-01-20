import tkinter as tk

VIEW_ROW_CNT = 50
MAX_ROW_CNT = 1000

USE_COLS = ['日付', '方法', 'カテゴリ', 'カテゴリの内訳', '支払元', '品目', 'メモ', 'お店', '通貨変換前の金額', '集計の設定']

SHOW_COLS_1 = ['日付', '集計の設定', 'カテゴリ', 'カテゴリの内訳', '通貨変換前の金額', '支払元', '点数', '件数', 'お店', '品目', 'メモ']
SHOW_COLS_2 = ['お店', '最終訪問日', '訪問回数', '合計金額', '平均金額']

# DataFrameレイアウト
DATA_FLAME_LAYOUT_1 = {
    'No': [50, tk.E], '日付': [100, tk.W], '集計の設定': [160, tk.E], 'カテゴリ': [110, tk.E], 'カテゴリの内訳': [160, tk.E], '金額': [120, tk.E], '支払元': [180, tk.E],
    '点数': [60, tk.E], '件数': [60, tk.E], 'お店': [500, tk.W], '品目': [400, tk.W], 'メモ': [1000, tk.W]
}
DATA_FLAME_LAYOUT_2 = {
    'No': [50, tk.E], 'お店': [1500, tk.W], '最終訪問日': [100, tk.W], '訪問回数': [100, tk.E], '合計金額': [100, tk.E], '平均金額': [100, tk.E]
}

# 集計一覧
TOTALING_LIST = [
    '', '常に集計に含める', '集計に含めない'
]

# 方法一覧
METHOD_LIST = {
    '全て': '', '支出': 'payment', '収入': 'income', '残高': 'balance', '振替': 'transfer'
}

# 支出カテゴリ
PAYMENT_CATEGORY_LIST = [
    '', '食費', '日用雑貨', '交通', '娯楽費', 'エンタメ', '交際費', '教育・教養', '美容・衣服', '医療・保険', '通信', '水道・光熱', '住まい', 'クルマ', '税金', '大型出費', 'その他'
]

# 支払元
PAYMENT_LIST = [
    '', 'お財布', '楽天 Edy', 'モバイル PASMO', '楽天ゴールドカード', 'Amazonマスタークラシック', 'JCBカード', 'セゾンゴールド', 'シネマイレージカードセゾン', '三菱東京UFJ銀行', '住信 SBIネット銀行', 'Amazon'
]