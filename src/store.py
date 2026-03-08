import flet as ft
import uuid
# ストアアプリの作成
# UI について　売っているもの(UI) 籠に入っているもの,合計(Controller)
# 上にあるリストがあってプラス　と　マイナス　のボタンで　その下に購入した商品の一覧が表示される。　id はいるのか？　表示順番は？　
from dataclasses import dataclass
@dataclass
class Item:
    id :str # 同じ商品で値段が違うものが存在するのでid を付けた方がいい
    name:str
    price : int
    count : int = 0
    # 次するときは、賞味期限など追加してみる 賞味期限で割引など

#購入しているアイテムを入れる
class BuyController:
    def __init__(self):
        # データはここで持つ
        self.all_item = []
        self.buy_item = {}
    def add_new_item(self,name,price):
        id = str(uuid.uuid4())
        self.all_item.append(id,name,price,0)
    def add_item(self,id):
        if id in self.buy_item:
            self.buy_item[id].count += 1
        else:
            self.buy_item[id].count = 1
    def reduce_item(self,id):
        if id in self.buy_item: # あるとき以外は、変化させない　マイナスにならせない。
            self.buy_item[id].count -=1
            if self.buy_item[id].count == 0:
                del self.buy_item[id]
    def delete_item(self,id):
        if id in self.buy_item:
            del self.buy_item[id]
    def get_all_item(self):
        return list(self.all_item.values())
    def get_buy_item(self):
        return list(self.buy_item.values)

    def sum_price(self):
        sum = 0
        for b in self.buy_item:
            now= b.count * b.price
            # if now > 10000 or b.count > 10:
                # now *= rate # 係数を関数にした方がいい # rateは誰が決めるのか？　item ? 店側が決める？　どこが決めるのか？　 割引はなしでする。
            sum += now # 割引とか考えられる
        return sum
@ft.control
class StoreItem(ft.Row):
    # 名前　値段　＋　－　消去　 というイメージ
    def __init__(self,item ,on_add,on_reduce,on_delete):
        super().__init__()
        # self.name = name
        # self.price = price item を受ける
        self.item = item #オブジェクトで受け取る
        self.on_add = on_add
        self.on_reduce = on_reduce
        self.on_delete = on_delete
        self.add_button = ft.IconButton(icon= ft.Icons.ADD,on_click=self._on_add)
        self.reduce_button = ft.IconButton(icon= ft.Icons.REMOVE,on_click=self._on_reduce)
        self.delete_button = ft.IconButton(icon= ft.Icons.DELETE,on_click=self._on_delete)
        self.controls = [
            ft.Text(value= self.item.name),
            self.add_button,
            self.reduce_button,
            self.delete_button,
        ]
    def _on_add(self,e):
        self.on_add(self.item.id)
    def _on_reduce(self,e):
        self.on_reduce(self.item.id)
    def _on_delete(self,e):
        self.on_delete(self.item.id)

@ft.control
class StoreView(ft.Column):
    def __init__(self,controller,rate): # 割引 チケット
        super().__init__()
        self.controller = controller
        self.all_item_list = ft.Column()
        self.buy_item_list = ft.Column()
        # self.total_price = self.controller.sum_price()
        text = self.change_status()
        self.status = ft.Text(value=text)
        self.controls = [
            self.all_item_list,
            self.buy_item_list,
            self.status,
        ]
    def refresh(self):
        self.all_item_list.clear()
        for b in self.controller.get_all_item():
            now_item = Item(
                item= b,
                on_add=self.on_add,
                on_reduce=self.on_reduce,
                on_delete=self.on_delete,
            )
            self.all_item_list.append(now_item)
        self.buy_item_list.clear()

        for b in self.controller.get_buy_item:
            now_item = Item(
                item = b,
                on_add=self.on_add,
                on_reduce=self.on_reduce,
                on_delete=self.on_delete,
            )
            self.buy_item_list.append(now_item)
        self.total_price = self.controller.sum_price()
        # if self.total_price == 0:
        #     self.status.value = 'カートに何もなにも入っていません。'
        # else:
        #     self.status.value = f'現在の合計金額は {self.total_price}円です。'
        self.status.value = self.change_status()
    def change_status(self):
        self.total_price = self.controller.sum_price()
        if self.total_price == 0:
            return 'カートに何もなにも入っていません。'
        else:
            return f'現在の合計金額は {self.total_price}円です。'
    def on_add(self,id):
        self.controller.add_item(id)
        self.refresh()
    def on_reduce(self,id):
        self.controller.reduce_item(id)
        self.refresh()
    def on_delete(self,id):
        self.controller.delete_item(id)
        self.refresh()


def main(page:ft.Page):
    # page.add(ft.Text(value="Hello"))

if __name__=="__main__":
    ft.run(main)