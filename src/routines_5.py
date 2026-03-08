#コメント　2026年3月8日　現在　動作確認完了
# 次にすること　1. 追加機能　(更新できるようにする 累計記録にする　jsonが必要かもしれません,date を使うのでモデルの変更が必要の可能性がある)
#

import flet as ft
import uuid
# 最後はmvcを意識して記述する。
# M model # UIのことは知らない
# class Routine:
#     def __init__(self,id,name,done=False):
#         self.id = id
#         self.name = name
#         self.done = done
# データクラスを使って書ける こっちのほうが完結
from  dataclasses import dataclass
@dataclass
class Routine:
    id :str
    name : str
    done : bool = False

# データを保存しておく　データの中身の変更はしない　更新するだけ
class RoutineController:
    def __init__(self):
        self.routines = {} #modelをリストで管理
    #追加
    def add_item(self,name):
        id = str(uuid.uuid4()) #関数にしないと消える
        self.routines[id] = Routine(id,name)
    def delete_item(self,id):
        del self.routines[id]
    #変わったものを更新するだけ　変更は別のところがする
    def toggle_change(self,id,done):
        self.routines[id].done = done

    #これは？ 取り出し　viewから直接触らないようにするlistの方がいい？
    def get_routines(self):
        # return self.routines.values()
        return list(self.routines.values())

    #完了を数える values とは？ dict の　valueを取り出す
    def count_done(self):
        return sum(r.done for r in self.routines.values())

    #全タスク数のカウント
    def count_total_task(self):
        return len(self.routines)

#Routine item UIの最小単位
@ft.control
class RoutineItem(ft.Row):
    # 名前と完了　(それを変更するコールバック関数)
    def __init__(self,routine,on_delete,on_toggle):
        super().__init__()
        # self.name = name
        # self.done = done
        self.routine = routine #routine objectを受け取る
        self.on_delete = on_delete
        self.on_toggle = on_toggle
        self.checkbox = ft.Checkbox(
            label = routine.name,
            value = routine.done,
            on_change= self._on_toggle,
        )
        self.controls = [
            self.checkbox,
            ft.IconButton(icon=ft.Icons.DELETE,on_click=self._on_delete),
        ]
    def _on_delete(self,e):
        self.on_delete(self.routine) #変更対象
    def _on_toggle(self,e):
        self.on_toggle(self.routine,self.checkbox.value) #まだ伝わっていない
#RoutineList UIの箱 入力を受け取る　→　コントローラーに伝える
@ft.control
class RoutineView(ft.Column):
    def __init__(self,controller):
        super().__init__()
        # self.controller = RoutineController() 作らない　受け取る　依存関係　アプリから受け取る
        self.controller = controller
        done = self.controller.count_done()
        total = self.controller.count_total_task()
        self.status = ft.Text(value= f'本日の完了タスク : {done} /{total}') # UIなので、ここに置く　計算はコントローラー
        self.new_routine = ft.TextField(hint_text="タスクを入力してください。")
        self.button = ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=self._add_clicked)
        self.input_row = ft.Row(
            controls= [self.new_routine, self.button]
        )
        self.list = ft.Column()
        self.controls = [
            self.status,
            self.input_row,
            self.list,
        ]
        self.refresh() #一応やっておく
    def _add_clicked(self,e): # イベントは必ずe
        if self.new_routine.value.strip()!="":
            self.controller.add_item(self.new_routine.value)
            self.new_routine.value = ""
            self.refresh()
    def refresh(self):
        self.list.controls.clear()
        for r in self.controller.get_routines(): # values は? dict のkey:value こっちを取る
            item = RoutineItem(
                routine= r,
                on_delete= self.on_delete,
                on_toggle= self.on_toggle

            )
            self.list.controls.append(item)
        done = self.controller.count_done()
        total = self.controller.count_total_task()
        self.status.value = f'本日の完了タスク : {done} /{total}' #こうしないと更新されない
    #コントローラーを変化する
    def on_delete(self,routine):
        # del self.controller.routines[routine.id] 消去はcontrollerでする
        self.controller.delete_item(routine.id)
        self.refresh()
    def on_toggle(self,routine,done):
        self.controller.toggle_change(routine.id,done)
        self.refresh()

@ft.control
class RoutineApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.controller = RoutineController()
        self.view = RoutineView(self.controller)
        self.title = ft.Text(value="ルーティンアプリMVC version")
        self.controls = [
            self.title,
            self.view,
        ]






def main(page:ft.Page):
    # page.add(ft.Text(value = "Hello"))
    app = RoutineApp()
    page.add(app)


if __name__ =="__main__":
    ft.run(main)

# 1. リストが一つしかでない idの重複が原因
