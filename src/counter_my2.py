import flet as ft

def main(page:ft.Page):
    counter = 0 # 状態変数
    counter_text = ft.Text(value= str(counter),size=50)
    #変化量を変数に入れる
    def change_counter(change):
        # これをしないと　ローカルの変数だと思われる
        nonlocal counter
        counter += change
        counter_text.value = str(counter)
        page.update
    page.add(
        ft.Column(
            controls=[
                counter_text,
                ft.Row(
                    # ラムダ式を使う。
                    controls=[ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=lambda e:change_counter(1)),ft.FloatingActionButton(icon=ft.Icons.REMOVE,on_click=lambda e :change_counter(-1))],
                    alignment=ft.MainAxisAlignment.CENTER # ボタンの配置を決めている。
                )
            ],
            # コラムとローで動きが違うので注意する。
            alignment= ft.MainAxisAlignment.CENTER, # コラム内の縦方向中央
            horizontal_alignment= ft.CrossAxisAlignment.CENTER, #コラム内での横方向中央
            expand=True,
        )
    )

ft.run(main)