import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import pandas as pd
import webbrowser
import const
import function as func
import glob
import re


# アプリの定義
class MouseApp(tk.Frame):

    # 初期化
    def __init__(self, master=None):
        self.init = True

        # ★バグ対応用の関数を追加
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        def func_genre(row):
            val = re.findall(r'【(.*)】', row.お店)
            return '' if len(val) == 0 else val[0]

        def func_place(row):
            val = re.findall(r'\((.*)\)', row.お店) + re.findall(r'.* (.*)店.*', row.お店)
            return '' if len(val) == 0 else val[0]

        def func_score(row):
            val = re.findall(r'(^\d\.\d\d)/', row.メモ)
            try:
                return float(val[0])
            except:
                return 0.00

        def func_number(row):
            val = re.findall(r'/(.*?)件', row.メモ)
            try:
                return int(val[0])
            except:
                return 0


        tk.Frame.__init__(self, master, width=720, height=1080)

        # タイトルの表示
        self.master.title('Zaim')

        # ラベルの生成
        self.lbl_title = tk.Label(self, text='Zaim',
                        font=(36, 36),
                        foreground='#ffffff',
                        background='#00aa00')

        # データフレーム取得
        files = glob.glob("./*.csv")
        target = max([int(re.findall('.*\.(.*)\.', i)[0]) for i in files])
        df = pd.read_csv(f'Zaim.{target}.csv', encoding='utf-8', usecols=const.USE_COLS, low_memory=False).fillna('')
        # 必要なカラムを生成
        df['ジャンル'] = df.apply(func_genre, axis=1)
        df['場所'] = df.apply(func_place, axis=1)
        df['点数'] = df.apply(func_score, axis=1)
        df['件数'] = df.apply(func_number, axis=1)
        df = df.sort_values(['日付'], ascending=False)

        # カテゴリの辞書を生成
        category_dict = func.extract_category(df)

        # 年
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '年'))
        self.lbl_year = tk.Label(self, text='年')
        year_list = [''] + [i[0:4] for i in df.日付.tolist()]
        year_list = sorted(set(year_list), key=year_list.index)
        self.cmb_year = ttk.Combobox(self, width=10, height=50, textvariable=sv, values=year_list)

        # 集計
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '集計'))
        self.lbl_totaling = tk.Label(self, text='集計')
        self.cmb_totaling = ttk.Combobox(self, width=20, height=50, textvariable=sv, values=list(const.TOTALING_LIST))

        # 方法
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '方法'))
        self.lbl_method = tk.Label(self, text='方法')
        self.cmb_method = ttk.Combobox(self, width=20, height=50, textvariable=sv, values=list(const.METHOD_LIST.keys()))

        # カテゴリ
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, 'カテゴリ', category_dict))
        self.lbl_category = tk.Label(self, text='カテゴリ')
        self.cmb_category = ttk.Combobox(self, width=20, height=50, textvariable=sv, values=[])

        # カテゴリの内訳
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, 'カテゴリの内訳'))
        self.lbl_category_detail = tk.Label(self, text='カテゴリの内訳')
        self.cmb_category_detail = ttk.Combobox(self, width=20, height=50, textvariable=sv, values=[])

        # 方法の初期値
        self.cmb_method.current(0)

        # お店
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_shop = tk.Label(self, text='お店')
        self.txt_shop = tk.Entry(self, width=30, textvariable=sv)

        # ジャンル
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_genre = tk.Label(self, text='ジャンル')
        self.txt_genre = tk.Entry(self, width=20, textvariable=sv)

        # 品目
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_item = tk.Label(self, text='品目')
        self.txt_item = tk.Entry(self, width=20, textvariable=sv)

        # メモ
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_memo = tk.Label(self, text='メモ')
        self.txt_memo = tk.Entry(self, width=20, textvariable=sv)

        # 金額ソート
        self.bv1 = tk.BooleanVar()
        self.bv1.trace("w", lambda name, index, mode, bv=self.bv1, df=df: self.on_check_changed(df, '金額ソート'))
        self.chk_price_sort = tk.Checkbutton(self, variable=self.bv1, text='金額ソート')

        # 点数ソート
        self.bv2 = tk.BooleanVar()
        self.bv2.trace("w", lambda name, index, mode, bv=self.bv2, df=df: self.on_check_changed(df, '点数ソート'))
        self.chk_score_sort = tk.Checkbutton(self, variable=self.bv2, text='点数ソート')

        # 全表示
        self.bv3 = tk.BooleanVar()
        self.bv3.trace("w", lambda name, index, mode, bv=self.bv3, df=df: self.on_check_changed(df, '全表示'))
        self.chk_all_show = tk.Checkbutton(self, variable=self.bv3, text='全表示')

        # 訪問回数グループ化
        self.bv4 = tk.BooleanVar()
        self.bv4.trace("w", lambda name, index, mode, bv=self.bv4, df=df: self.on_check_changed(df, '訪問回数グループ化'))
        self.chk_visit_group = tk.Checkbutton(self, variable=self.bv4, text='訪問回数グループ化')

        # ツリーレイアウト 
        self.tree = None
        self.make_tree()

        # スクロールバー
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill="y")
        self.tree.pack()
        self.tree["yscrollcommand"] = scroll.set

        # ウィジェット配置
        self.widget()

        # バグ対応を処理
        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        style.configure("Treeview", font=("Arial", 11, 'bold'), rowheight=28)

        self.init = False
        self.reload(df)


    def make_tree(self):
        data_frame_layout = const.DATA_FLAME_LAYOUT_2 if self.bv4.get() else const.DATA_FLAME_LAYOUT_1
        self.tree = ttk.Treeview(self)
        self.tree['height'] = const.VIEW_ROW_CNT
        self.tree["column"] = list(data_frame_layout.keys())
        self.tree["show"] = "headings"
        [self.tree.heading(k, text=k) for k in data_frame_layout.keys()]
        [self.tree.column(k, width=v[0], anchor=v[1]) for k, v in data_frame_layout.items()]
        self.tree.bind("<Double-1>", lambda event: self.on_tree_double_click(event))


    def on_tree_double_click(self, event):
        select = self.tree.selection()[0]
        print(select)
        shop = self.tree.set(select)['お店']
        shop = re.sub(r'\[.*\]', '', shop)
        shop = re.sub(r'【.*】', '', shop)
        shop = shop.replace('(', '').replace(')', '')
        print(shop)
        webbrowser.open(f'https://www.google.com/search?q=食べログ+{shop}')


    def on_check_changed(self, df, type=''):
        print(type)
        if type == '金額ソート':
            if self.bv1.get():
                self.bv2.set(False)
                self.bv4.set(False)
        elif type == '点数ソート':
            if self.bv2.get():
                self.bv1.set(False)
                self.bv4.set(False)
        elif type == '訪問回数グループ化':
            if self.bv4.get():
                self.bv1.set(False)
                self.bv2.set(False)
        self.widget_forget()
        self.make_tree()
        self.widget()
        self.on_text_changed(df)


    def on_text_changed(self, df, col='', category_dict=''):
        print(col)
        if col == '方法':
            self.reset()
            val = self.cmb_method.get()
            if val == '支出':
                self.cmb_category['values'] = const.PAYMENT_CATEGORY_LIST
            elif val == '収入':
                self.cmb_category['values'] = const.INCOME_CATEGORY_LIST
        elif col == 'カテゴリ':
            self.cmb_category_detail.set('')
            val = self.cmb_category.get()
            self.cmb_category_detail['values'] = category_dict[val]
        self.reload(df)


    def reset(self):
        try:
            self.cmb_category.set('')
            self.cmb_category_detail.set('')
            self.txt_shop.delete(0, tk.END)
            self.txt_genre.delete(0, tk.END)
            self.txt_item.delete(0, tk.END)
            self.txt_memo.delete(0, tk.END)
        except:
            pass


    def on_enter(self, df):
        self.reload(df)


    def reload(self, df):
        if self.init:
            return
        print('reload')
        year = self.cmb_year.get()
        totaling = self.cmb_totaling.get()
        method = self.cmb_method.get()
        category = self.cmb_category.get()
        category_detail = self.cmb_category_detail.get()
        shop = self.txt_shop.get()
        genre = self.txt_genre.get()
        item = self.txt_item.get()
        memo = self.txt_memo.get()
        price_sort = self.bv1.get()
        score_sort = self.bv2.get()
        all_show = self.bv3.get()
        visit_group = self.bv4.get()
        if year != '':
            df = df[df['日付'].str.contains(year)]
        if totaling != '':
            df = df[df['集計の設定'].str.contains(totaling)]
        if method not in ['全て']:
            df = df[df['方法'] == const.METHOD_LIST[method]]
        if category != '':
            df = df[df['カテゴリ'].str.contains(category)]
        if category_detail != '':
            category_detail = category_detail.replace('(', '\(').replace(')', '\)')
            df = df[df['カテゴリの内訳'].str.contains(category_detail)]
        if shop != '':
            df = df[df['お店'].str.lower().str.contains(shop.lower())]
        if genre != '':
            df = df[df['ジャンル'].str.contains(genre)]
        if item != '':
            df = df[df['品目'].str.lower().str.contains(item.lower())]
        if memo != '':
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
        if visit_group:
            self.lbl_title['text'] = f'Zaim {"{:,}".format(len(df))}件 hit 総訪問回数 {"{:,}".format(df["訪問回数"].sum())}回 総額 ￥{"{:,}".format(df["合計金額"].sum())}'
        else:
            self.lbl_title['text'] = f'Zaim {"{:,}".format(len(df))}件 hit 総額 ￥{"{:,}".format(df["通貨変換前の金額"].sum())}'

        func.insert_tree(self.tree, df, visit_group)


    def widget(self):
        # ウィジェット配置
        self.lbl_title.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.lbl_year.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
        self.cmb_year.pack(side=tk.LEFT, after=self.lbl_year, anchor=tk.W, padx=5, pady=5)
        self.lbl_totaling.pack(side=tk.LEFT,after=self.cmb_year,  anchor=tk.W, padx=5, pady=5)
        self.cmb_totaling.pack(side=tk.LEFT, after=self.lbl_totaling, anchor=tk.W, padx=5, pady=5)
        self.lbl_method.pack(side=tk.LEFT, after=self.cmb_totaling, anchor=tk.W, padx=5, pady=5)
        self.cmb_method.pack(side=tk.LEFT, after=self.lbl_method, anchor=tk.W, padx=5, pady=5)
        self.lbl_category.pack(side=tk.LEFT, after=self.cmb_method, anchor=tk.W, padx=5, pady=5)
        self.cmb_category.pack(side=tk.LEFT, after=self.lbl_category, anchor=tk.W, padx=5, pady=5)
        self.lbl_category_detail.pack(side=tk.LEFT, after=self.cmb_category, anchor=tk.W, padx=5, pady=5)
        self.cmb_category_detail.pack(side=tk.LEFT, after=self.lbl_category_detail, anchor=tk.W, padx=5, pady=5)
        self.lbl_shop.pack(side=tk.LEFT, after=self.cmb_category_detail, anchor=tk.W, padx=5, pady=5)
        self.txt_shop.pack(side=tk.LEFT, after=self.lbl_shop, anchor=tk.W, padx=5, pady=5)
        self.lbl_genre.pack(side=tk.LEFT, after=self.txt_shop, anchor=tk.W, padx=5, pady=5)
        self.txt_genre.pack(side=tk.LEFT, after=self.lbl_genre, anchor=tk.W, padx=5, pady=5)
        self.lbl_item.pack(side=tk.LEFT, after=self.txt_genre, anchor=tk.W, padx=5, pady=5)
        self.txt_item.pack(side=tk.LEFT, after=self.lbl_item, anchor=tk.W, padx=5, pady=5)
        self.lbl_memo.pack(side=tk.LEFT, after=self.txt_item, anchor=tk.W, padx=5, pady=5)
        self.txt_memo.pack(side=tk.LEFT, after=self.lbl_memo, anchor=tk.W, padx=5, pady=5)
        self.chk_price_sort.pack(side=tk.LEFT, after=self.txt_memo, anchor=tk.W, padx=5, pady=5)
        self.chk_score_sort.pack(side=tk.LEFT, after=self.chk_price_sort, anchor=tk.W, padx=5, pady=5)
        self.chk_all_show.pack(side=tk.LEFT, after=self.chk_score_sort, anchor=tk.W, padx=5, pady=5)
        self.chk_visit_group.pack(side=tk.LEFT, after=self.chk_all_show, anchor=tk.W, padx=5, pady=5)

    
    def widget_forget(self):
        self.tree.pack_forget()
        self.lbl_year.pack_forget()
        self.cmb_year.pack_forget()
        self.lbl_method.pack_forget()
        self.cmb_method.pack_forget()
        self.lbl_category.pack_forget()
        self.cmb_category.pack_forget()
        self.lbl_category_detail.pack_forget()
        self.cmb_category_detail.pack_forget()
        self.lbl_shop.pack_forget()
        self.txt_shop.pack_forget()
        self.lbl_genre.pack_forget()
        self.txt_genre.pack_forget()
        self.lbl_item.pack_forget()
        self.txt_item.pack_forget()
        self.lbl_memo.pack_forget()
        self.txt_memo.pack_forget()
        self.chk_price_sort.pack_forget()
        self.chk_score_sort.pack_forget()
        self.chk_visit_group.pack_forget()
                 
# アプリの実行
f = MouseApp()
f.pack()
f.mainloop()