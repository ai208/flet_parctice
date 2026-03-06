from dataclasses import field
import flet as ft
# 計算アプリ　tutorial で行った。
def main(page: ft.Page):
    # page.add(ft.Text(value="Hello,world")) 確認できた。
    page.title = "Calc App"
    result = ft.Text(value="0",color=ft.Colors.WHITE,size=20) # size20が丁度いいくらい
    # 揃っていない。　コンテナを使う。
    # page.add(
    #     ft.Row(controls=[result]),
    #     ft.Row(
    #         controls=[
    #         ft.Button("AC"),
    #         ft.Button("+/-"),
    #         ft.Button("%"),
    #         ft.Button("/"),
    #         ]
    #     ),
    #   ft.Row(
    #       controls=[
    #             ft.Button("7"),
    #             ft.Button("8"),
    #             ft.Button("9"),
    #             ft.Button("*"),
    #             ],
    #   ),
    #   ft.Row(
    #       controls=[
    #         ft.Button("4"),
    #         ft.Button("5"),
    #         ft.Button("6"),
    #         ft.Button("-"),
    #       ],
    #   ),
    #   ft.Row(
    #       controls=[
    #         ft.Button("1"),
    #         ft.Button("2"),
    #         ft.Button("3"),
    #         ft.Button("+"),
    #       ]
    #   ),
    #   ft.Row(
    #       controls=[
    #         ft.Button("0"),
    #         ft.Button("."),
    #         ft.Button("="),
    #       ],
    #   ),
    # )
    #container version を作成する。　途中コラムを使った
    # page.add(
    #     ft.Container(
    #         width=350,
    #         bgcolor=ft.Colors.BLACK,
    #         border_radius=ft.BorderRadius.all(20),
    #         padding=20,
    #         # containerの時は、contentに配置する
    #         content=ft.Column(
    #             controls=[
    #             ft.Row(controls=[result],alignment=ft.MainAxisAlignment.END),
    #             #ボタンをすべて変えないといけない　Actionbuttonにしないといけない
    #             ft.Row(
    #                 controls=[
    #                 ft.Button("AC"),
    #                 ft.Button("+/-"),
    #                 ft.Button("%"),
    #                 ft.Button("/"),
    #                 ]
    #             ),
    #             ft.Row(
    #                 controls=[
    #                         ft.Button("7"),
    #                         ft.Button("8"),
    #                         ft.Button("9"),
    #                         ft.Button("*"),
    #                         ],
    #             ),
    #             ft.Row(
    #                 controls=[
    #                     ft.Button("4"),
    #                     ft.Button("5"),
    #                     ft.Button("6"),
    #                     ft.Button("-"),
    #                 ],
    #             ),
    #             ft.Row(
    #                 controls=[
    #                     ft.Button("1"),
    #                     ft.Button("2"),
    #                     ft.Button("3"),
    #                     ft.Button("+"),
    #                 ]
    #             ),
    #             ft.Row(
    #                 controls=[
    #                     ft.Button("0"),
    #                     ft.Button("."),
    #                     ft.Button("="),
    #                 ],
    #             ),],
    #         ),
    #     )
    # )
    # @デコレーター Calc buttonをベースにして全てのボタンを作る クラスを加工する
    @ft.control
    class CalcButton(ft.Button):
        # field はインポートして来た。
        expand: int = field(default_factory= lambda: 1)
    @ft.control
    class DigitButton(CalcButton):
        bgcolor : ft.Colors = ft.Colors.WHITE_24
        color : ft.Colors = ft.Colors.WHITE
    @ft.control
    class DigitButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.WHITE_24
        color: ft.Colors = ft.Colors.WHITE

    @ft.control
    class ActionButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.ORANGE
        color: ft.Colors = ft.Colors.WHITE

    @ft.control
    class ExtraActionButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
        color: ft.Colors = ft.Colors.BLACK

    # 計算ロジック　クラスでする　現在の値と前の数字と演算子の3つを保存しておく。 クラスで状態と関数を持っている状態になっている。
    # class Calculator:
    # def __init__(self, result_text: ft.Text):
    #     self.result = result_text
    #     self.current_input = ""   # 今入力している数字（文字列）
    #     self.previous_value = 0   # 前の数字
    #     self.operator = None      # 演算子 (+, -, *, /)

    # def button_clicked(self, e):
    #     data = e.control.content
    #     # 数字ボタンの場合
    #     if data in "0123456789.":
    #         self.current_input += data
    #         self.result.value = self.current_input
    #     # 演算子ボタンの場合
    #     elif data in "+-*/":
    #         if self.current_input:
    #             self.previous_value = float(self.current_input)
    #             self.current_input = ""
    #         self.operator = data
    #     # = ボタンの場合
    #     elif data == "=":
    #         if self.operator and self.current_input:
    #             try:
    #                 curr = float(self.current_input)
    #                 if self.operator == "+":
    #                     res = self.previous_value + curr
    #                 elif self.operator == "-":
    #                     res = self.previous_value - curr
    #                 elif self.operator == "*":
    #                     res = self.previous_value * curr
    #                 elif self.operator == "/":
    #                     res = self.previous_value / curr
    #                 self.result.value = str(res)
    #                 # 計算後の状態更新
    #                 self.previous_value = res
    #                 self.current_input = ""
    #                 self.operator = None
    #             except Exception:
    #                 self.result.value = "Error"
    #     # AC ボタン
    #     elif data == "AC":
    #         self.current_input = ""
    #         self.previous_value = 0
    #         self.operator = None
    #         self.result.value = "0"

    #     # UI 更新
    #     self.result.update()
    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.BorderRadius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment=ft.MainAxisAlignment.END),
                    ft.Row(
                        controls=[
                            ExtraActionButton(content="AC"),
                            ExtraActionButton(content="+/-"),
                            ExtraActionButton(content="%"),
                            ActionButton(content="/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="7"),
                            DigitButton(content="8"),
                            DigitButton(content="9"),
                            ActionButton(content="*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="4"),
                            DigitButton(content="5"),
                            DigitButton(content="6"),
                            ActionButton(content="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="1"),
                            DigitButton(content="2"),
                            DigitButton(content="3"),
                            ActionButton(content="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="0", expand=2),
                            DigitButton(content="."),
                            ActionButton(content="="),
                        ],
                    ),
                ]
            ),
        )
    )

# 安全でないらしい
# ft.run(main)
if __name__ == "__main__":
    ft.run(main)
