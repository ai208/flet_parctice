# ひと通り学んだ　自分で作って見る 極力見ないで
# class のtodo appを作る。
import flet as ft
@ft.control
class Todoapp(ft.Column):
    def init(self): # __init__ としない。
        self.new_task = ft.TextField(hint_text="タスクを入力してください。",expand=True)
        self.task_view = ft.Column()
        self.width = 600
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=self.add_clicked),
                ]
            ),
            self.task_view, # 下段？　イメージができないです。
        ]
    def add_clicked(self,e): # eも渡す。
        if self.new_task.value!= "":
            self.task_view.controls.append(ft.Checkbox(label=self.new_task.value))
            self.new_task.value =""
            self.update() # pageではなくてself


def main(page:ft.Page):
    # page.add(ft.Text(value="hello")) 確認〇
    page.title = "to-do-app"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    todo = Todoapp()
    page.add(todo)


if __name__ == "__main__":
    ft.run(main)