# ACVA 構造を意識して記述する
# ListをViewとするUIであることを強調するために #やっぱり、リスト　itemとつながっているから
import flet as ft
@ft.control
class RoutineItem(ft.Row): #名前とチェック(削除ボタン付き)
    def __init__(self,name,on_delete): # 親にお願いする
        super().__init__()
        self.name = name
        self.on_delete = on_delete # nameと同じように書く
        # self.checkbox = ft.Checkbox(label = self.name)
        # self.controls = ft.Row( コントロールはリストにする
        #     controls = [
        #         self.checkbox,
        #         ft.IconButton(icon = ft.Icons.DELETE, on_click = self._on_delete),# _on_ クリック時に呼ばれる
        #     ]
        # )
        # rowは定義でしているから要らない
        self.controls = [
                ft.Checkbox(label=name),
                ft.IconButton(icon = ft.Icons.DELETE, on_click = self._on_delete),# _on_ クリック時に呼ばれる
        ]
    def _on_delete(self,e):#selfがいる _on_delete クリック時に呼ばれる
        self.on_delete(self) #== list._on_delete(item)

#通常のクラス
class RoutineController:
    def __init__(self):
        self.routines = []

    def add_item(self,item):
        self.routines.append(item)

    def remove_item(self,item):
        self.routines.remove(item)

@ft.control # UI controller のリストを使ってUIを作る コントローラーの後
# 行うこと　追加された時の更新　と　削除された時の更新
class RoutineList(ft.Column):
    def __init__(self,controller:RoutineController):
        super().__init__()
        self.controller = controller
        # self.refresh()　これがあるとエラーが出る
    def refresh(self):
        self.controls.clear()
        for name in self.controller.routines:
            self.controls.append(RoutineItem(name,self._on_delete))
        self.update()
    def _on_delete(self,item): #itemのクリックが押されると実行される関数
        if item.name in self.controller.routines:
            self.controller.remove_item(item.name) #コントローラーから削除
            self.refresh()

#画面全体のレイアウト　タイトル　入力フィールド　リスト
@ft.control
class RoutineApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = ft.Text(value="ルーティンアプリ")
        self.new_routine = ft.TextField(hint_text = "タスクを入力してください。")
        self.controller = RoutineController()
        self.routine_list = RoutineList(self.controller)
        self.button = ft.FloatingActionButton(icon = ft.Icons.ADD,on_click = self.clicked_button)
        self.input_row = ft.Row(
            controls =[
            self.new_routine,
            self.button,
            ]
        )
        self.controls = [
            self.title,
            self.input_row,
            self.routine_list,
        ]
    def clicked_button(self,e):
        if self.new_routine.value.strip() != "":
            self.controller.add_item(self.new_routine.value) #コントローラーのデータの変更
            self.routine_list.refresh() #UIリストの更新
            self.new_routine.value = ""







def main(page:ft.Page):
    #完成version
    app = RoutineApp()
    page.add(app)

    # page.add(ft.Text(value = "Hello")) 確認終了
    #item の確認
    # def demo(e):
    #     print("削除")
    # item = RoutineItem("test",demo)
    # page.add(item)

    # controller listの確認
    # controller = RoutineController()
    # for i in range( 1,10):
    #     controller.add_item(f'{i}回目')
    # routines_list = RoutineList(controller)
    # page.add(routines_list)
    # routines_list.refresh()
if __name__ =="__main__":
    ft.run(main)

# 1. itemの確認の際に何も表示されない
#→ ft.checkbox(label) としていなかった
# on_delete 親から　_on_delete クリック時に呼ばれる

# 2. controller list エラーが出る　RuntimeError: RoutineList(9) Control must be added to the page first　いつものエラー　List init でrefreshをしたらエラーが出た
# 3. 灰色になった　コントロールのミス Listからcheckboxを作る処理がなかった(item)を使って
# 4. 白色で何も表示されない
# →　itemの表示を見た。前確認したはず？
# 5     self.routines.remove(item) ValueError: list.remove(x): x not in list
#→　if で確認を入れた
# 6 削除のボタンを認識がミス
#→　item の関数のミス

# 動いた　item controller view app の順番で作る　