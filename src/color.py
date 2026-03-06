import flet as ft
# flet app の作成手順 機能 → 状態 → UI部品 → イベント → レイアウト
#1 何を作るかを決める
#2 状態を決める
#3 部品を作る
#4 イベントを作る
#5 レイアウトを組む

#シンプルに言うとFletは：

# ① 状態を持つ
# ② 状態を変える関数を書く
# ③ それをUIに配置する

# 1.最小構成 まずはこれを作る
# def main(page: ft.Page):
#     page.add(ft.Text("Hello"))


# 2.状態を持たせる　しかし、これだと画面と繋がっていない
# def main(page: ft.Page):
#     color = "white"
# 3. 画面の部品に変数を持たせる
# def main(page: ft.Page):
#     # Container width heightが必要である。
#     box = ft.Container(
#         width=200,
#         height=200,
#         bgcolor="black"
#     )
#     page.add(box)
def main(page: ft.Page):
    color = "green"
    box = ft.Container(
        height=200,
        width=200,
        bgcolor= color
    )
    # 4. ボタンを作る
    def color_change_red(e):
        # colorを変えるのではなく、box オブジェクトを変更する必要がある。
        # color = "red"
        box.bgcolor ="red"
        box.update()
        # 緑を追加した。
    def color_change_green(e):
        box.bgcolor = "green"
        box.update()
    #ボタンが一つしかない。
    # page.floating_action_button= ft.FloatingActionButton(content="赤色",on_click=color_change_red)
    #右下のボタン
    page.floating_action_button = ft.Row(
        controls=[ft.FloatingActionButton(content="赤色",on_click=color_change_red),ft.FloatingActionButton(content="緑色",on_click=color_change_green)],
        # Row の時は、　MainAxis  とつける必要がある。 中央に持ってきた
        alignment= ft.MainAxisAlignment.CENTER,
    )
    # ft.floating は右下
    # appbar は上　他にも置き場所がある　見切れている。良くない。
    # page.appbar =  ft.AppBar(
    # 効果がない　expnad
    #     expand= True,
    #     #title 左寄席　action 右寄せ
    #     title=ft.Text("色変更アプリ"),
    #     # controls ではない。
    #     actions =[
    #         ft.IconButton(icon=ft.Icons.FAVORITE, on_click=color_change_red),
    #         ft.IconButton(icon=ft.Icons.BATTERY_FULL, on_click=color_change_green),
    #     # appbar はalignmentはない alignmentはコンテナ用
    #     # alignment= ft.Alignment.CENTER,
    #     ]
    # )
    # 上のボタン　移動させれる　row control mainaxisalignmentを使う。
    page.appbar =  ft.AppBar(
        title=ft.Row(
        # controls ではない。
        controls =[
            ft.IconButton(icon=ft.Icons.FAVORITE, on_click=color_change_red),
            ft.IconButton(icon=ft.Icons.BATTERY_FULL, on_click=color_change_green),
        ],
        #通常は右寄り
        alignment= ft.MainAxisAlignment.START,
        # 広げられる変化は分からない。
        expand=True

        ),
    )
    #5.レイアウトを組む
    page.add(box)




ft.run(main)