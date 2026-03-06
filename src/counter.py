import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)
    message = ft.Text("Hello")
    # ボタンのロジック
    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        #カウンターを更新する　大規模アプリ
        counter.update()
        #ページを更新する　小規模アプリ
        # page.update()
    # incrementを参考にdecreaseも書いた
    def decrease_click(e):
        counter.data -= 1
        counter.value = str(counter.data)
        #カウンターを更新する　大規模アプリ
        counter.update()
        # ページを更新する　小規模アプリ
        # page.update()
    # このように書いたらできない。 floating action button は一つだけしかできない
    # page.button = ft.FloatingActionButton(
    #     icon=ft.Icons.ADD, on_click=increment_click
    # )
    # page.floating_action_button = ft.FloatingActionButton(
    #     icon=ft.Icons.ADD, on_click=decrease_click
    # )
    # ボタンの作成　ボタンは本文の上にあるという状態になっている。　本文の一部にしたい場合は、page addに入れる
    page.floating_action_button = ft.Row(
        controls=[ft.FloatingActionButton(icon=ft.Icons.ADD,on_click=increment_click),ft.FloatingActionButton(icon=ft.Icons.REMOVE,on_click=decrease_click)],
        alignment=ft.MainAxisAlignment.END, # Row / Column の時は、MainAxisAlin start center end

    )
    # 本文を作っている。
    page.add(
        # SafeAreaとは？
        ft.SafeArea(
            expand=True,
            # メッセージの表示　ボタンはある　
            # content = ft.Container(
            #     content = message,
            #     alignment = ft.Alignment.CENTER
            # ),
            # カウンターの表示
            content=ft.Container(
                content=counter,
                alignment=ft.Alignment.CENTER,
            ),
        )
    )


ft.run(main)
