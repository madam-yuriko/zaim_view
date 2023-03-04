import tkinter as tk
import tkinter.ttk as ttk
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

        # 支出一覧
        self.payment_list = list(set(df[df['方法'] == 'payment']['カテゴリ'].tolist()))
        # 収入一覧
        self.income_list = list(set(df[df['方法'] == 'income']['カテゴリ'].tolist()))

        # カテゴリの辞書を生成
        category_dict = func.extract_category(df)

        # 年
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '年'))
        self.lbl_year = tk.Label(self, text='年')
        year_list = [''] + [i[0:4] for i in df.日付.tolist()]
        year_list = sorted(set(year_list), key=year_list.index)
        self.cmb_year = ttk.Combobox(self, width=8, height=50, textvariable=sv, values=year_list)

        # 月
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '月'))
        self.lbl_month = tk.Label(self, text='月')
        self.cmb_month = ttk.Combobox(self, width=4, height=50, textvariable=sv, values=[''])

        # 集計
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '集計'))
        self.lbl_totaling = tk.Label(self, text='集計')
        self.cmb_totaling = ttk.Combobox(self, width=16, height=50, textvariable=sv, values=list(const.TOTALING_LIST))

        # 方法
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '方法'))
        self.lbl_method = tk.Label(self, text='方法')
        self.cmb_method = ttk.Combobox(self, width=10, height=50, textvariable=sv, values=list(const.METHOD_LIST.keys()))

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

        # 支払元
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df, '支払元'))
        self.lbl_payment = tk.Label(self, text='支払元')
        self.cmb_payment = ttk.Combobox(self, width=20, height=50, textvariable=sv, values=const.PAYMENT_LIST)

        # 方法の初期値
        self.cmb_method.current(0)

        # 金額 下限
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_money_lower = tk.Label(self, text='金額(下限)')
        self.txt_money_lower = tk.Entry(self, width=10, textvariable=sv)

        # 金額 上限
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_money_upper = tk.Label(self, text='金額(上限)')
        self.txt_money_upper = tk.Entry(self, width=10, textvariable=sv)

        # お店
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df: self.on_text_changed(df))
        self.lbl_shop = tk.Label(self, text='お店')
        self.txt_shop = tk.Entry(self, width=25, textvariable=sv)

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
        self.txt_memo = tk.Entry(self, width=25, textvariable=sv)

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
        print('on_tree_double_click')
        select = self.tree.selection()[0]
        shop = re.sub(r'【.*】', '', re.sub(r'\[.*\]', '', self.tree.set(select)['お店'])).replace('(', '').replace(')', '')
        if not self.bv4.get():
            category = self.tree.set(select)['カテゴリ']
            if category == '食費':
                webbrowser.open(f'https://www.google.com/search?q={shop}')
            else:
                item = self.tree.set(select)['品目']
                webbrowser.open(f'https://www.google.com/search?q={item}')
        else:
            # 訪問回数グループ化
            webbrowser.open(f'https://www.google.com/search?q={shop}')

    def on_check_changed(self, df, type=''):
        print('on_check_changed', type)
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
        print('on_text_changed', col)
        if col == '年':
            val = self.cmb_year.get()
            if val:
                self.cmb_month['values'] = [''] + [str(i).zfill(2) for i in list(range(1, 13))]
            else:
                self.cmb_month.set('')
                self.cmb_month['values'] = ['']
        if col == '方法':
            self.reset()
            val = self.cmb_method.get()
            if val == '全て':
                self.cmb_category['values'] = [''] + self.payment_list + self.income_list
            elif val == '支出':
                self.cmb_category['values'] = const.PAYMENT_CATEGORY_LIST
            elif val == '収入':
                self.cmb_category['values'] = [''] + self.income_list
        elif col == 'カテゴリ':
            self.cmb_category_detail.set('')
            val = self.cmb_category.get()
            self.cmb_category_detail['values'] = [''] + category_dict[val]
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
        month = self.cmb_month.get()
        totaling = self.cmb_totaling.get()
        method = self.cmb_method.get()
        category = self.cmb_category.get()
        category_detail = self.cmb_category_detail.get()
        payment = self.cmb_payment.get()
        money_lower = self.txt_money_lower.get()
        money_upper = self.txt_money_upper.get()
        shop = self.txt_shop.get()
        genre = self.txt_genre.get()
        item = self.txt_item.get()
        memo = self.txt_memo.get()
        price_sort = self.bv1.get()
        score_sort = self.bv2.get()
        all_show = self.bv3.get()
        visit_group = self.bv4.get()
        df = func.processing_data_frame(df, year, month, totaling, method, category, category_detail, payment, money_lower, money_upper, shop, genre, item, memo, price_sort, score_sort, all_show, visit_group)
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
        self.lbl_month.pack(side=tk.LEFT,after=self.cmb_year,  anchor=tk.W, padx=5, pady=5)
        self.cmb_month.pack(side=tk.LEFT, after=self.lbl_month, anchor=tk.W, padx=5, pady=5)
        self.lbl_totaling.pack(side=tk.LEFT,after=self.cmb_month,  anchor=tk.W, padx=5, pady=5)
        self.cmb_totaling.pack(side=tk.LEFT, after=self.lbl_totaling, anchor=tk.W, padx=5, pady=5)
        self.lbl_method.pack(side=tk.LEFT, after=self.cmb_totaling, anchor=tk.W, padx=5, pady=5)
        self.cmb_method.pack(side=tk.LEFT, after=self.lbl_method, anchor=tk.W, padx=5, pady=5)
        self.lbl_category.pack(side=tk.LEFT, after=self.cmb_method, anchor=tk.W, padx=5, pady=5)
        self.cmb_category.pack(side=tk.LEFT, after=self.lbl_category, anchor=tk.W, padx=5, pady=5)
        self.lbl_category_detail.pack(side=tk.LEFT, after=self.cmb_category, anchor=tk.W, padx=5, pady=5)
        self.cmb_category_detail.pack(side=tk.LEFT, after=self.lbl_category_detail, anchor=tk.W, padx=5, pady=5)
        self.lbl_payment.pack(side=tk.LEFT, after=self.cmb_category_detail, anchor=tk.W, padx=5, pady=5)
        self.cmb_payment.pack(side=tk.LEFT, after=self.lbl_payment, anchor=tk.W, padx=5, pady=5)
        self.lbl_money_lower.pack(side=tk.LEFT, after=self.cmb_payment, anchor=tk.W, padx=5, pady=5)
        self.txt_money_lower.pack(side=tk.LEFT, after=self.lbl_money_lower, anchor=tk.W, padx=5, pady=5)
        self.lbl_money_upper.pack(side=tk.LEFT, after=self.txt_money_lower, anchor=tk.W, padx=5, pady=5)
        self.txt_money_upper.pack(side=tk.LEFT, after=self.lbl_money_upper, anchor=tk.W, padx=5, pady=5)
        self.lbl_shop.pack(side=tk.LEFT, after=self.txt_money_upper, anchor=tk.W, padx=5, pady=5)
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
        self.lbl_month.pack_forget()
        self.cmb_month.pack_forget()
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