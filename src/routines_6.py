# routine_5 から開始する。　

import flet as ft
import uuid
import json
from datetime import date
# 最後はmvcを意識して記述する。
# M model # UIのことは知らない
# class Routine:
#     def __init__(self,id,name,done=False):
#         self.id = id
#         self.name = name
#         self.done = done
# データクラスを使って書ける こっちのほうが完結
from  dataclasses import dataclass,field
@dataclass
class RoutineModel:
    id :str
    name : str
    done : bool = False
    total_done : int = 0 # Routein に関連することはこっちがもつ
    last_done_date : date | None = None # 最初　と　チェックをも出した時はNoneが入る 完了したら　=date.today() とする # dataはjson で持てないからstrにする
@dataclass
class UserModel:
    username :str
    login_streak : int
    # total_done : int　完了は　ルーチンモデルの方が持つべき
    last_login : date | None = None
    routines : list[RoutineModel] = field(default_factory = list) # pythonの罠の回避

#アプリの状態 のみにする
class AppModel:
    def __init__(self,repository): # dataclass で引数を取る方法
        # self.filename = filename storageに渡す
        # self.storage = storage # こっちにデータの保存を任せる　   repository に渡す
        self.repository = repository
        self.user : UserModel | None = None
    # user_model : class
    # # routines_model : class # userが持つ
    # all_data : list # は　userに入っている
    # filename : str
    def save(self): # アプリは状態のみ　データの保存
        # with open(self.filename,"w",encoding="utf-8") as f: しない　storage に送る
        #     json.dump(self.all_data,f,ensure_ascii = False,indent = 2)
        # self.storage.save(self.user)
        self.repository.save(self.user)

    def load(self):
        # try:storage に任せる 引っ張てくる
        #     with open(self.filename,"r",encoding="utf-8") as f:
        #         self.all_data =json.load(f)
        # except FileNotFoundError:
        #     self.all_data = []
        # self.user = self.storage.load() storageをしない
        self.repository.load()

# Service storage 直接にならないようにする。
# class Routine_Repository:　# いらない今回は
#     def __init__(self,storage):
#         self.storage = storage
#     def save_user(self,user):
#         self.storage.save(user)
#     def load_user(self):
#         return self.storage.load()
class User_Repository:
    def __init__(self,storage):
        self.storage = storage
    def save_user(self,user):
        self.storage.save(user)
    def load_user(self):
        return self.storage.load()

#データの保存専門
class JsonStorage:
    def __init__(self,filename :str):
        self.filename = filename
    def save(self,user):
        data = self.user_to_dict(user)
        with open(self.filename,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,ident = 2)
    def load(self):
        try:
            with open(self.filename,"r", encoding="utf-8") as f:
                data = json.load(f)
                return self.dict_to_user(data)
        except FileNotFoundError:
            return None
    # モデルをdict(json) に変換しないといけない data は　str に変換する必要がある
    def user_to_dict(self,user):
        routines = []
        for r in user.routines:
            routines.append({
                "id":r.id,
                "name":r.name,
                "done":r.done,
                "total_done":r.total_done,
                "last_done_date":r.last_done_date.isoformat() if r.last_done_date else None # dat をstr にしてjson にできるようにした。
            })
        return {
            "username" : user.username,
            "login_streak":user.login_streak,
            "last_login":user.last_login.isoformat() if user.last_login else None,
            "routines":routines
        }
    def dict_to_user(self,data): #読み取り
        routines = []
        for r in data["routines"]:
            routines.append(
                RoutineModel(
                    id = r["id"],
                    name = r["name"],
                    dne = r["name"],
                    total_done= r["total_done"],
                    last_done_date= date.fromisoformat(r["last_done_date"]) if r["last_done_date"] else None
                )
            )
        return UserModel(
            username=data["username"],
            login_streak=data["login_streak"],
            last_login=date.fromisoformat(data["last_login"]) if data["last_login"] else None,
            routines= routines
        )


# データを保存しておく　データの中身の変更はしない　更新するだけ
class RoutineController: #操作だけをする　Service に送る
    def __init__(self,app_model,service): # model とサービスにつながっている
        super().__init__()
        self.app = app_model
        self.service = service
        # self.routines = {} #modelをリストで管理 二重管理になる コントローラーは操作をするだけ
    #追加
    def add_item(self,name):
        id = str(uuid.uuid4()) #関数にしないと消える
        routine = RoutineModel(id,name)
        self.app.user.routines.append(routine)
    def delete_item(self,id):
        # del self.routines[id]
        self.app.user.routines = [
            r for r in self.app.user.routines
            if r.id != id
        ] # このロジックが不明
    #変わったものを更新するだけ　変更は別のところがする
    # def toggle_change(self,id,done): サービスに送る
    #     # self.routines[id].done = done
    #     for r in self.app.user.routines:
    #         if r.id == id:
    #             r.done = done
    def toggle_change(self,routine:RoutineModel,done :bool):
        if done:
            self.service.complete_routine(routine)
        else:
            self.service.undo_routine(routine)

    #これは？ 取り出し　viewから直接触らないようにするlistの方がいい？
    def get_routines(self):
        # return self.routines.values()
        # return list(self.routines.values())
        return self.app.user.routines

    #完了を数える values とは？ dict の　valueを取り出す サービスに送る
    # def count_done(self):
    #     return sum(r.done for r in self.app.user.routines)

    #全タスク数のカウント サービスへ
    # def count_total_task(self):
    #     return len(self.app.user.routines)

# user コントローラーも必要になる 一つのモデルに一つ 作成と更新
class UserController: # 操作をする
    def __init__(self,app_model):
        super().__init__()
        self.app = app_model
    def create_user(self,username):
        self.app.user = UserModel(username=username)
    # def update_login(self): # サービスに送る
    #     today = date.today()
    #     user = self.app.user
    #     if user.last_login != today:
    #         user.login_streak += 1
    #     user.last_login = today

# service ビジネスロジック　の担当
class User_Service:
    def __init__(self):
        pass
    def update_login(self,user): # userのロジックなので、userがいる
        today = date.today()
        if user.last_login != today:
            user.login_streak +=1
        user.last_login = today

class Routine_Service:
    def __init__(self):
        pass
    def complete_routine(self,routine):
        if not routine.done:
            routine.done = True
            routine.total_done += 1
            routine.last_done_date = date.today()

    def undo_routine(self,routine):
        if routine.done:
            routine.done = False
            routine.total_done -= 1
            routine.last_done_date = None
    def count_done(self,routine):
        return sum(r.done for r in routine) # r.done = True の時が1 だからこれを合計すればいい
    def count_total_task(self,routine):
        return len(routine)




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
        self.title = ft.Text(value="ルーティンアプリMVC version 機能追加version")
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
