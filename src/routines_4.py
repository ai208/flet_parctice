import flet as ft
import uuid
# ICVモデルを使って実装する　Item Controller View の3つ
# item(モデル) →　View(描写) → Controller(データ) の3つで行う。
# AIに教えてもらった。 #Single Source of Truth を意識して書いた
@ft.control
class RoutineItem(ft.Row):
    # UI の最小単位
    # name タスクの名前, done 完了状態, on_delete 消去コールバック関数 i->v, on_toggle チェック切り替えコールバック　i → v 二つの情報(name,done)とこれを変更するコールバック関数
    # on_toggle の使い方？　checkbox の　on_change 初見
    def __init__(self,id,name,done,on_delete,on_toggle):
        super().__init__()
        self.id = id # idを付ける　消去
        self.name = name
        self.on_delete = on_delete
        self.on_toggle = on_toggle
        self.checkbox = ft.Checkbox(
            label=name,
            value = done,
            on_change= self._toggle_done #関数をもつ
        )
        self.controls = [
            self.checkbox,
            ft.IconButton(icon=ft.Icons.DELETE,on_click=self._on_delete),
        ]
        # i -> v に情報を伝える
    def _on_delete(self,e):
        self.on_delete(self)
    def _toggle_done(self,e):
        self.on_toggle(self,self.checkbox.value) #doneを変更する

# controller データ管理 name と　done をもつ　この二つの情報
class RoutineController:
    def __init__(self):
        self.routines = []
    def add_item(self,name):
        #{辞書になった}
        self.routines.append({
            "id":str(uuid.uuid4()),
            "name":name,
            "done":False,
        })
    def remove_item(self,id): # idでする ルーティンアプリとして、idは適切なのか？　入力のときに重複があった時伝えた方がいい気がする。いったんidでやってみる。　後で変える。全探索をしない方法もある    self.items[id] = {
    #     "id": id,
    #     "name": name,
    #     "done": False
    # } とすればいい。
        # 1.消去法 nameのとき
        # for r  in self.routine: 全部消える　入力の時に重複確認　or id をつける
        #     if self.routines["name"] == name:
        #         self.routines.remove(r)
        #         break
        # 2.リストの作り直し方法　nameのとき
        # self.routines = [ for r in self.routines if self.name != name]
        for r in self.routines:
            if r["id"] == id:
                self.routines.remove(r)
                break
    def toggle_change(self,id,done):#Single Source of Truth
            for r in self.routines:
                # if self.routines["id"] ==id:
                #     self.routines["done"] ^= done # ^ が使える？　1-done とする
                if r["id"] == id:
                    r["done"] = done #状態を保存するだけ、変更はitemでやっている
    def count_total_task(self):
        return len(self.routines)
    def count_done(self):
        return sum(1 for r in self.routines if r["done"]==True)


@ft.control # コントローラーがもつ情報をviewにする
class RoutineView(ft.Column):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
    def refresh(self):
        self.controls.clear() # これがないと増殖する
        for r in self.controller.routines:
            item = RoutineItem(
                id = r["id"],
                name = r["name"],
                done = r["done"],
                on_delete= self._on_delete,
                on_toggle= self._on_toggle,
            )
            self.controls.append(item)
        self.update()
    def _on_delete(self,item):
        self.controller.remove_item(item.id) #コントローラーはidを持たない　リスト
        self.refresh()
    def _on_toggle(self,item,done): # doneは必要　itemは状態を持たない　item UI controller 状態
        self.controller.toggle_change(item.id,done)
        self.refresh()

#app
@ft.control
class RoutineApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.controller = RoutineController() #コントローラー
        self.list_view = RoutineView(self.controller) # ビュー
        self.title = ft.Text(value ="ルーティンアプリ_ICV-version")
        self.status = ft.Text(value="完了 : 0 / 0")
        self.new_routine = ft.TextField(hint_text="タスクを入力してください。")
        self.button = ft.FloatingActionButton(icon=ft.Icons.ADD,on_click= self.clicked_add)
        self.input_row = ft.Row(
            controls= [
                self.new_routine,
                self.button,
            ]
        )
        self.controls = [
            self.title,
            self.status,
            self.input_row,
            self.list_view,
        ]

    def clicked_add(self,e):
        if(self.new_routine.value.strip()!=""):# controller に行く
            self.controller.add_item(self.new_routine.value) #コントローラーの更新
            self.update_status()
            self.list_view.refresh() #ヴューの更新
            self.new_routine.value =""
    def update_status(self):
        done = self.controller.count_done()
        total = self.controller.count_total_task()
        self.status.value = f'完了 : {done} / {total}'
        self.update()

def main(page:ft.Page):
    app = RoutineApp()
    page.add(app)

if __name__ =="__main__":
    ft.run(main)


# 1. 灰色になった　Text にした　
# 2. refreshはいるいらない？　 refreshの場所が色々なところになっている。
#更新ができていないです。