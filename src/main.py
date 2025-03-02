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
        self.history_list = ft.Column(visible=False)
        self.last_was_equal = False  # Novo controle para após o "="
       
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
                            ExtraActionButton(text="x²", button_clicked=self.button_clicked),
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

    def format_number(self, num):
        try:
            if isinstance(num, (int, float)) and num % 1 == 0:
                return int(num)
            return f"{float(num):,.10f}".replace(",", " ").rstrip("0").rstrip(".")
        except (ValueError, TypeError):
            return str(num)

    def calculate(self, operand1, operand2, operator):
        try:
            if operator == "+":
                return self.format_number(operand1 + operand2)
            elif operator == "-":
                return self.format_number(operand1 - operand2)
            elif operator == "*":
                return self.format_number(operand1 * operand2)
            elif operator == "/":
                if operand2 == 0:
                    return "Error"
                return self.format_number(operand1 / operand2)
        except Exception:
            return "Error"

    def button_clicked(self, e):
        data = e.control.data
       
        # Se o último clique foi "=" e um novo botão é clicado, limpa a expressão
        if self.last_was_equal and data != "AC":
            self.expression.value = ""
            self.last_was_equal = False
           
        if data == "AC":
            self.expression.value = ""
            self.result.value = "0"
            self.reset()
           
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "(", ")"):
            if self.result.value == "0" or self.result.value == "Error":
                self.result.value = data
            else:
                self.result.value += data
            self.expression.value += data
            self.new_operand = False
           
        elif data in ("+", "-", "*", "/"):
            if self.new_operand:  # Substitui o operador anterior se já houver um
                self.expression.value = self.expression.value[:-1] + data
            else:
                self.expression.value += f" {data}"
            if self.operator and not self.new_operand:
                self.result.value = self.calculate(
                    float(self.operand1), float(self.result.value), self.operator
                )
            self.operator = data
            self.operand1 = float(self.result.value) if self.result.value != "Error" else 0
            self.new_operand = True
           
        elif data == "=":
            if self.expression.value:
                full_expression = self.expression.value.strip()
                try:
                    sympy_result = sp.N(sp.sympify(full_expression))
                    self.result.value = self.format_number(sympy_result)
                    self.expression.value = f"{full_expression} = {self.result.value}"
                    self.add_to_history(full_expression, self.result.value)
                    self.reset()
                    self.last_was_equal = True
                except Exception:
                    self.result.value = "Error"
                    self.expression.value = "Error"
                   
        elif data == "+/-":
            try:
                current = float(self.result.value)
                if current > 0:
                    self.result.value = f"-{self.result.value}"
                elif current < 0:
                    self.result.value = str(abs(current))
                # Atualiza a expressão
                if self.expression.value:
                    parts = self.expression.value.split()
                    if parts and parts[-1] not in ("+", "-", "*", "/"):
                        parts[-1] = self.result.value
                        self.expression.value = " ".join(parts)
                    else:
                        self.expression.value += f" {self.result.value}"
            except ValueError:
                pass
               
        elif data == "%":
            try:
                self.result.value = self.format_number(float(self.result.value) / 100)
                if self.expression.value:
                    parts = self.expression.value.split()
                    if parts and parts[-1] not in ("+", "-", "*", "/"):
                        parts[-1] = self.result.value
                        self.expression.value = " ".join(parts)
                    else:
                        self.expression.value += f" {self.result.value}"
            except ValueError:
                self.result.value = "Error"
               
        elif data == "√":
            try:
                self.result.value = self.format_number(sp.sqrt(float(self.result.value)))
                if self.expression.value:
                    parts = self.expression.value.split()
                    if parts and parts[-1] not in ("+", "-", "*", "/"):
                        parts[-1] = f"√({parts[-1]})"
                        self.expression.value = " ".join(parts)
                    else:
                        self.expression.value += f" √({self.result.value})"
            except ValueError:
                self.result.value = "Error"
               
        elif data == "x²":
            try:
                self.result.value = self.format_number(float(self.result.value) ** 2)
                if self.expression.value:
                    parts = self.expression.value.split()
                    if parts and parts[-1] not in ("+", "-", "*", "/"):
                        parts[-1] = f"({parts[-1]})²"
                        self.expression.value = " ".join(parts)
                    else:
                        self.expression.value += f" ({self.result.value})²"
            except ValueError:
                self.result.value = "Error"
               
        self.update()

    def add_to_history(self, expression, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"expression": expression, "result": result, "time": timestamp}
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()
        self.save_history()

    def save_history(self):
        self.page.client_storage.set("calc_history", self.history)

    def load_history(self):
        history = self.page.client_storage.get("calc_history")
        return history if history is not None else []

    def toggle_history(self, e):
        self.history_list.visible = not self.history_list.visible
        if self.history_list.visible:
            self.history_list.controls = [
                ft.Row(
                    [
                        ft.Text(f"{i+1}. {item['expression']} = {item['result']}"),
                        ft.IconButton(icon=ft.icons.COPY, on_click=lambda _, r=item['result']: self.page.set_clipboard(r)),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda _, idx=i: self.delete_from_history(idx))
                    ]
                )
                for i, item in enumerate(self.history)
            ]
        self.update()

    def delete_from_history(self, idx):
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

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000)