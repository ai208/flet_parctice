import flet as ft
# クラスで開発する時のコツ 3個
#カプセル化 自分のことは自分でする
#インスタンス変数(self)の使い方
# 3コールバック関数を渡す仕組み
# 親　list と　itemによって実装する。
# 先に子から実装する。　持っている情報は、nameとチェックボックスと消去ボタンとコントロール
@ft.control
class RoutinesItem(ft.Row): # チェックボックスと消去ボタン
    # init のほうがいいのか？ 使い分けはどうやってする？
    def __init__(self,name,on_delete):#引数は名前と親要素を消去する関数(引数というイメージを持つ)
        super().__init__() # 初期化 ()を忘れない。
        self.name = name # 名前
        self.checkbox = ft.Checkbox(label= name)
        self.delete_btn = ft.FloatingActionButton(icon=ft.Icons.DELETE,on_click= lambda e:on_delete(self)) # ①押したら_deleteを実行するボタンを作る。_delete は親に通知するボタン
        self.controls = [
            self.checkbox,
            #self.checkbox.label としたら、チェックボックスがなくなる　かっこは残る　
            self.delete_btn,
        ]
        self._on_delete = on_delete #③ 親要素を消去する関数を実行する
    def _delete(self,e):#② ボタンで呼び出される。
        self._on_delete(self)

@ft.control
class RoutineList(ft.Column):
    def __init__(self):
        super().__init__()
        self.items=[] # からのitemを持つ
    def add_item(self,name):
        if name != "":
            # item = RoutinesItem(name,self.remove_item) #アイテムを作成する。引数が関数の時は、ラムダ式を使う
            item = RoutinesItem(
                name,
                # on_delete=lambda e :self.remove_item(self) #引数を関数で渡す　これだとエラーになる
                on_delete= self.remove_item # こっちだと上手く動く
            )
            self.items.append(item) #リストに加える
            self.controls.append(item) # コントロール(UI)に加える
            # name = ""　これでもできない
            self.update()
    def remove_item(self,item):
        self.items.remove(item) #リストから消す
        self.controls.remove(item) #コントロール(UI)から消す
        self.update()



def main(page:ft.Page):
    # page.add(ft.Text(value="Hello")) 確認完了
    routine_list = RoutineList()
    new_routine =ft.TextField(hint_text="タスクを入力してください。")
    # view = ft.Column(
    #     controls=[
    #         ft.Row(
    #             controls =[
    #             new_routine,
    #             #  ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=routine_list.add_item(new_routine)),　これがエラーの原因　読んだ結果を入れていた。ラムダ式で関数を渡す必要がある
    #             ft.FloatingActionButton(icon=ft.Icons.ADD, on_click= lambda e:routine_list.add_item(new_routine) )
    #             ],
    #         ),
    #         *routine_list.controls,
    #         # routine_list, 画面が灰色になる
    #     ]
    # )
    # page.add(view)
    # 書き直し　ボタンの列を作った後に、routinelist との一緒にページに加える
    row = ft.Row(
        controls=[
                new_routine,
                ft.FloatingActionButton(icon=ft.Icons.ADD, on_click= lambda e:routine_list.add_item(new_routine) )
                ],
    )
    page.add(row,routine_list)
ft.run(main)
#2026年3月7日実施　見ながら記述した。
#1. 最初にコントロールのエラーが出た。　クラスを追加する前に触るとだめらしいです。
# →on_click= ラムダ式関数にした
#2. 次はエラーはなかったが、画面が灰色になった。 原因の推定　page.addが正しくできていない。
# →　コラムがおかしい　 *routine_list.controls アスタリスクを付けた
#3. addをした後に、エラーが出る。　
#→ pageaddの方法を変更した。　ボタンを作った後に、追加した　アスタリスクが要らなくなった。
#4. たくさんのエラーが出た　！　引数に関数を渡す時は、ラムダ式にしないといけない。
#→ ボタンの引数　呼び出し方？　on_delete が引数だった　super().__init__()とかく
#5. デリートしたらリストのエラー　何もないと言われる
#6. チェックボックスで表示される　前直した routienで行った。　何をしたのか不明
# →　valueとする 
#7. ラムダ式をいつ使うのか？　click との違い　self いるときと要らないとき
#8. 追加したときに、入力フォームが空白にならない
# add 関連を見て確認する
