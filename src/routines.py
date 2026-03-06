# アプリの機能：習慣化するためのアプリ
# 毎日することをチェックする
import flet as ft
#Routeine所有する状態 name と 完了したか？(chackbox)を使う　(doneとするよりもチェックボックスのほうが楽)
@ft.control
class Routine(ft.Column):
    def __init__(self, name):
        super().__init__() # 初期化テンプレ
        self.name = name
        self.checkbox = ft.Checkbox(label=name) # ラベルはチェックボックスの説明

def main(page:ft.Page):
    # page.add(ft.Text("Hello"))　起動確認〇
    routines = []#直接コラムに入れるようにしたが、nameが消えるので戻した。
    new_routine = ft.TextField(hint_text="新しいルーティンを追加してください。")
    def add_clicked(e):
        if new_routine.value!="":
            routine = Routine(new_routine.value)
            # routines.controls.append(routine) リストにオブジェクトを入れるから、コントロールはいらない
            routines.append(routine) #データとして追加
            print(routine.name)
            routines_view.controls.append(routine.checkbox) # UIに追加　二段階になっている。チェックボックスが追加される
            # こっちだでもできた。こっちは、新しく作っている。
            # routines_view.controls.append(ft.Checkbox(label=routine.name))
            new_routine.value ="" #初期化する
            page.update()
    # todo_version2の考え方を使った。
    routines_view = ft.Column()
    view = (ft.Column(
        controls=[
        ft.Row(
            controls=[
                new_routine,
                ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=add_clicked)
            ], # Row Colum の後はcontrols = [],とする
        ),
        routines_view,#ルーティンリストのオブジェクトとのcheckboxを追加する　コントロールはリスト
        ],
    ))
    # page.add(routines.checkbox) 間違いを　オブジェクトのリストなので、checkboxを持っていない。
    page.add(view)

ft.run(main)