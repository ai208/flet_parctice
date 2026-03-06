from dataclasses import field #version 4
from typing import Callable # version 4

import flet as ft

# taskの追加　version 4
@ft.control
class Task(ft.Column):
    task_name: str = "" # 型ヒント?
    on_task_delete: Callable[["Task"],None] = field(default=lambda task :None)
    # f: Callable[[], None]  # 引数なし、戻り値なしの関数 Callableは型ヒント　わかりやすくなる。
    # f = lambda: print("Hello")
    # f()  # "Hello" が出力される
    def init(self):
        self.display_task = ft.Checkbox(value=False,label=self.task_name)
        self.edit_name = ft.TextField(expand=1) #編集のフォーム
        # 通常の時は、編集と削除がある。
        self.display_view = ft.Row(
            controls=[
                self.display_task,
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit to-do",
                            on_click= self.edit_clicked,
                        ),
                        ft.IconButton(
                            icon= ft.Icons.DELETE_OUTLINE,
                            tooltip="delete to-do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        #編集用は更新用になっている。
        self.edit_view = ft.Row(
            visible=False,
            controls=[
                self.edit_name, # 編集のフォーム
                ft.IconButton(
                    icon=ft.Icons.DONE_ALL_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="update todo",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view,self.edit_view] # 通常時と編集時　の二つ持っている。
    def edit_clicked(self,e):
        self.edit_name.value = self.display_task.label # 表示されている値を編集へ渡す
        self.display_view.visible = False # 非編集の時用
        self.edit_view.visible = True # 編集の時用
        self.update()
    def save_clicked(self,e):
        self.display_task.label = self.edit_name.value # 編集の値表示にする
        self.display_view.visible = True #非編集用
        self.edit_view.visible = False #編集の時用
        self.update()
    def delete_clicked(self,e):
        self.on_task_delete(self)

#他のところでも使えるように、クラスにしておく。 version 3
@ft.control
class Todoapp(ft.Column):

    def init(self): #初期化 インスタンス
        self.new_task = ft.TextField(hint_text="やることを入力してください。",expand=True)
        self.tasks = ft.Column()
        self.width = 600
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=self.add_clicked),
                ]
            ),
            self.tasks,
        ] # ui のオブジェクトというイメージ
    def add_clicked(self,e):
        if self.new_task.value != "": # 値の確認をする
            task = Task(task_name = self.new_task.value, on_task_delete = self.task_delete)
            self.tasks.controls.append(task)#追加する
            self.new_task.value = "";#初期化
            self.update() # 更新を忘れない
    def task_delete(self,task): # 消去の関数
        self.tasks.controls.remove(task)
        self.update()

def main(page :ft.Page):
    # page.add(ft.Text(value="Hello")) 確認用
    ### version 1
    # TextField で外部からの入力を受け取る
    # new_task = ft.TextField(hint_text="やることを入力してください。")
    # pageにチェックボックスを追加する関数 first version
    # def add_clicked(e):
    #     if new_task.value != "": # 空でないときのみ追加
    #         page.add(ft.Checkbox(label=new_task.value))
    #         print(new_task.value) # コンソールで確認用
    #         new_task.value = ""
    #         page.update # 更新は忘れない。
    # # ボタンを押したら関数を実行する。
    # page.add(new_task,ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=add_clicked))


    ###version 2 newtask をtaskviewにまとめてから表示した。
    # def add_clicked(e):
    #     if new_task.value != "": # 空でないときのみ追加
    #         #入力をtask_view.controls に入れる
    #         tasks_view.controls.append(ft.Checkbox(label=new_task.value))
    #         print(new_task.value) # コンソールで確認用
    #         new_task.value = ""
    #         page.update()
    # 追加していくコード　view とtask_view ? を使っている。
    # tasks_viewに情報が入っている　それをコラムにする こっちのほうがまとまりがある。
    # コラム　上に　チェックボックス　下に　tasks_view
    # tasks_view = ft.Column()
    # view = ft.Column(
    #     width=600,
    #     controls=[
    #         ft.Row(
    #             controls=[
    #                 new_task,
    #                 ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=add_clicked),
    #             ]
    #         ), # コラムの一行目
    #         tasks_view, #コラムの二行目
    #     ]
    # )
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.add(view)

    #### version 3 クラスを使った。
    page.title = "To-do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER #水平方向へ揃える
    page.update() # なぜ、必要か？ -> 変更した時、更新されない場合がある。
    todo = Todoapp() #呼び出し
    page.add(todo)
    # add の後は、update()されるから必要ない

    #### version 4 デリートと編集の追加

ft.run(main)