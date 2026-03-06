import flet as ft

#カウンターアプリの作成
# 機能　カウンターが増えていく
# 状態　counter = 0 がスタート
# 部品　カウンター　と　±のボタン
# イベント　カウンターの数字の変更
# レイアウト　上にカウンター　下にボタン
def main(page: ft.Page):
    #初期確認
    # page.add(ft.Text("Hello"))
    number = 0 # 状態変数
    box = ft.Container(
        height=400,
        width=400,
        # これはだめ　container はtextを持たない。
        # text = 'number',
        # content = ft.Textでする。 これだと numberと表示される
        # content= ft.Text("number",color = "black"),
        content= ft.Text(str(number),color = "black"),
        bgcolor='blue',
        # alignment="center", おかしい。灰色になる。
        # horizontal_alignment = "center"
        # Alignment 大文字にする　container の中の真ん中になっていた。
        alignment=ft.Alignment.CENTER,
    )
    def pls(e):
        box.content.value=str(int(box.content.value) + 1)
        box.update()
    def mins(e):
        # box.content -=1 エラーが出た。文字列を変換する必要がある
        box.content.value = str(int(box.content.value)-1)
        box.update()
    page.floating_action_button = ft.Row(
        controls = [ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=pls),ft.FloatingActionButton(icon=ft.Icons.REMOVE,on_click=mins)],
        alignment= ft.MainAxisAlignment.CENTER
    )
    page.add(box)

ft.run(main)