import flet as ft
import sympy as sp
import datetime

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

class CalculatorApp(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.reset()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=32)
        self.expression = ft.Text(value="", color=ft.colors.GREY_500, size=24)
        self.history = self.load_history()
        self.history_list = ft.ListView(
            visible=False,
            height=200,
            auto_scroll=False,
            padding=10
        )
        self.current_expression = ""  
        self.last_was_equal = False  

        self.content = ft.Container(
            width=400,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[self.expression], alignment=ft.MainAxisAlignment.END),
                    ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                            ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                            ExtraActionButton(text="%", button_clicked=self.button_clicked),
                            ActionButton(text="/", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="7", button_clicked=self.button_clicked),
                            DigitButton(text="8", button_clicked=self.button_clicked),
                            DigitButton(text="9", button_clicked=self.button_clicked),
                            ActionButton(text="*", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="4", button_clicked=self.button_clicked),
                            DigitButton(text="5", button_clicked=self.button_clicked),
                            DigitButton(text="6", button_clicked=self.button_clicked),
                            ActionButton(text="-", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="1", button_clicked=self.button_clicked),
                            DigitButton(text="2", button_clicked=self.button_clicked),
                            DigitButton(text="3", button_clicked=self.button_clicked),
                            ActionButton(text="+", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="0", button_clicked=self.button_clicked, expand=2),
                            DigitButton(text=".", button_clicked=self.button_clicked),
                            ActionButton(text="=", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="(", button_clicked=self.button_clicked),
                            ExtraActionButton(text=")", button_clicked=self.button_clicked),
                            ExtraActionButton(text="√", button_clicked=self.button_clicked),
                            ExtraActionButton(text="⌫", button_clicked=self.button_clicked),  
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="sin", button_clicked=self.button_clicked),
                            ExtraActionButton(text="cos", button_clicked=self.button_clicked),
                            ExtraActionButton(text="tan", button_clicked=self.button_clicked),
                            ExtraActionButton(text="π", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(text="Mostrar Histórico", on_click=self.toggle_history),
                            ft.ElevatedButton(text="Limpar Histórico", on_click=self.clear_history),
                        ]
                    ),
                    self.history_list
                ]
            ),
        )

    def reset(self):
        self.operator = None
        self.operand1 = 0
        self.new_operand = False
        self.current_expression = ""  
        self.last_was_equal = False

    def format_number(self, num):
        if isinstance(num, sp.Number):
            num = float(num)
        if num.is_integer():
            return int(num)
        else:
            return f"{num:.10f}".rstrip("0").rstrip(".")

    def button_clicked(self, e):
        data = e.control.data

        if self.last_was_equal and data not in ("AC", "="):
            self.current_expression = ""
            self.expression.value = ""
            self.last_was_equal = False

        if data == "AC":
            self.current_expression = ""
            self.expression.value = ""
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "(", ")"):
            self.current_expression += data
            self.result.value = self.current_expression

        elif data in ("+", "-", "*", "/"):
            self.current_expression += f"{data}"
            self.result.value = self.current_expression

        elif data == "=":
            if self.current_expression:
                try:
                    expr = self.current_expression.replace("π", str(sp.pi))
                    sympy_result = sp.N(sp.sympify(expr))
                    self.expression.value = self.current_expression
                    self.result.value = self.format_number(sympy_result)
                    self.add_to_history(self.current_expression, self.result.value)
                    self.current_expression = ""
                    self.last_was_equal = True
                except Exception:
                    self.result.value = "Error"
                    self.expression.value = "Error"
                    self.current_expression = ""

        elif data == "+/-":
            if self.current_expression:
                if self.current_expression.endswith(")"):
                    i = len(self.current_expression) - 1
                    paren_count = 0
                    while i >= 0:
                        if self.current_expression[i] == ")":
                            paren_count += 1
                        elif self.current_expression[i] == "(":
                            paren_count -= 1
                            if paren_count == 0:
                                break
                        i -= 1
                    if i >= 0 and i + 1 < len(self.current_expression):
                        prefix = self.current_expression[i:i+2]
                        if prefix == "(-":
                            number = self.current_expression[i+2:-1]
                            self.current_expression = self.current_expression[:i] + "(+" + number + ")"
                        elif prefix == "(+":
                            number = self.current_expression[i+2:-1]
                            self.current_expression = self.current_expression[:i] + "(-" + number + ")"
                        else:
                            number = self.current_expression[i+1:-1]
                            self.current_expression = self.current_expression[:i] + "(-" + number + ")"
                else:
                    i = len(self.current_expression) - 1
                    while i >= 0 and (self.current_expression[i].isdigit() or self.current_expression[i] == "."):
                        i -= 1
                    last_number_start = i + 1
                    last_number = self.current_expression[last_number_start:]
                    if last_number and last_number.replace(".", "", 1).isdigit():
                        self.current_expression = self.current_expression[:last_number_start] + "(-" + last_number + ")"
                self.result.value = self.current_expression
                
        elif data == "%":
            parts = self.current_expression.split()
            if parts:
                last_part = parts[-1]
                try:
                    num = float(last_part)
                    parts[-1] = str(num / 100)
                    self.current_expression = " ".join(parts)
                    self.result.value = self.current_expression
                except ValueError:
                    pass

        elif data == "√":
            parts = self.current_expression.split()
            if parts:
                last_part = parts[-1]
                try:
                    num = float(last_part)
                    if num >= 0:
                        parts[-1] = f"sqrt({last_part})"
                        self.current_expression = " ".join(parts)
                        self.result.value = self.current_expression
                    else:
                        self.result.value = "Error"
                except ValueError:
                    pass

        elif data == "⌫":  
            if self.current_expression:
                self.current_expression = self.current_expression[:-1]  
                if not self.current_expression:  
                    self.result.value = "0"
                else:
                    self.result.value = self.current_expression

        elif data in ("sin", "cos", "tan"):
            self.current_expression += f"{data}("
            self.result.value = self.current_expression

        elif data == "π":
            self.current_expression += "π"
            self.result.value = self.current_expression

        self.update()

    def add_to_history(self, expression, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"expression": expression, "result": result, "time": timestamp}
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()
        self.save_history()
        if self.history_list.visible:
            self.toggle_history(None)

    def save_history(self):
        self.page.client_storage.set("calc_history", self.history)

    def load_history(self):
        history = self.page.client_storage.get("calc_history")
        return history if history is not None else []

    def toggle_history(self, e):
        self.history_list.visible = not self.history_list.visible
        if self.history_list.visible:
            self.history_list.controls.clear()
            for i, item in enumerate(self.history):
                history_item = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{i+1}. {item['expression']} = {item['result']}", expand=True),
                            ft.IconButton(
                                icon=ft.icons.INFO_OUTLINE,
                                tooltip=f"Realizado em: {item['time']}",
                            ),
                            ft.IconButton(
                                icon=ft.icons.COPY,
                                tooltip="Copiar resultado",
                                data=item['result'],
                                on_click=self.copy_to_clipboard
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                data=i,
                                on_click=self.delete_from_history
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
                self.history_list.controls.append(history_item)
        self.update()

    def copy_to_clipboard(self, e):
        result = e.control.data
        self.page.set_clipboard(str(result))

    def delete_from_history(self, e):
        idx = e.control.data
        if 0 <= idx < len(self.history):
            self.history.pop(idx)
            self.save_history()
            self.toggle_history(None)

    def clear_history(self, e):
        self.history = []
        self.save_history()
        self.toggle_history(None)

def main(page: ft.Page):
    page.title = "Calculadora Avançada"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp(page)
    page.add(calc)
    
#ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000) (Usar esta linha para deploy no replit)
ft.app(target=main) #(Usar esta linha para teste local)
