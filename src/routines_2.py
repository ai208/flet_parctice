# 今回はmainを極力記述が少なくなるようにする→Routine_list にnew_routineを持つ
import flet as ft
# 中身　UI一個
# UI要素としては、チェックボックス(ラベルが必要である)削除ボタン
@ft.control
class RoutineItem(ft.Row):
    # pass
    def __init__(self,name,on_delete):
        super().__init__()
        self.name = name

        self.controls = [
            ft.Checkbox(label = self.name),
            ft.IconButton(icon = ft.Icons.DELETE,on_click = self.par_delete),
        ]
        self.delete_action = on_delete

    def par_delete(self,e):
        self.delete_action(self)


#箱 追加・削除　アイテム管理
#UI要素としては、入力フォーム(Textfield)とRoutienItemを持っている
@ft.control
class RoutineList(ft.Column):
    def add_item(self,name):
        item = RoutineItem(name,self.delete_item)
        self.controls.append(item) # UIに追加する
        self.update()

    def delete_item(self,item):
        self.controls.remove(item) #UIから消す
        self.update()

#店　入力、画面、レイアウト
@ft.control
class RoutineApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = ft.Text(value = "ルーティンアプリ")
        self.input = ft.TextField(hint_text = "タスクを入力してください。")
        self.button = ft.IconButton(icon = ft.Icons.ADD,on_click = self.add_click)
        self.routine_list = RoutineList() #直接呼ばないようにする。ルーティンの方が分かりやすい
        self.input_row = ft.Row( # row の方が良い
            controls = [self.input,self.button]
        )
        self.controls = [
            self.title,
            self.input_row,
            self.routine_list,
        ]

    def add_click(self,e):
        # if self.input.value != "":
        if self.input.value.strip() != "": #空白も弾ける できた。
            self.list.add_item(self.input.value)
            self.input.value ="" #更新の際に初期化する
            self.update()




def main(page:ft.Page):
    # page.add(ft.Text(value = "Hello")) #確認完了

    #itemの動作確認完了
    # 仮の関数を作って、動作確認をする
    # def test_delete(item): できた。
    #     print("削除:", item)
    # item = RoutineItem("test_item",test_delete)
    # page.add(item)

    # リストの動作確認完了
    # list = RoutineList()
    # page.add(list)
    # list.add_item("test")
    # list.add_item("apple")

    #アプリの動作確認
    app = RoutineApp()
    page.add(app)



if __name__ == "__main__":
    ft.run(main)

# 1. List まで行ったときに、 RoutineList(9) Control must be added to the page first　とエラーが出た
# →　最初にコントロールは追加されなければならない　page.add してから　add_itemをする

# 2. Appの動作確認の時は、The application encountered an error: 'RoutineApp' object has no attribute '_i'　と出た
#→　iの属性を持っていない 作る前に追加してしまった。 super().__init__忘れ
# 3. 真っ白になった　エラーはない　何も表示されていない　コントロールがおかしい？
#        self.routine_list = RoutineList()  とせずに直接　RoutineListを読んでいた。