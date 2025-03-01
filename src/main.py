import flet as ft
import sympy as sp

class CalcButton(ft.ElevatedButton):
	def __init__(self, text, button_clicked, expand=1):
		super().__init__()
		self.text = text
		self.expand = expand
		self.on_click = button_clicked
		self.data = text

class DigitButton(CalcButton):
	def __init__(self, text, button_clicked, expand=1):
		CalcButton.__init__(self, text, button_clicked, expand)
		self.bgcolor = ft.colors.WHITE24
		self.color = ft.colors.WHITE

class ActionButton(CalcButton):
	def __init__(self, text, button_clicked):
		CalcButton.__init__(self, text, button_clicked)
		self.bgcolor = ft.colors.ORANGE
		self.color = ft.colors.WHITE

class ExtraActionButton(CalcButton):
	def __init__(self, text, button_clicked):
		CalcButton.__init__(self, text, button_clicked)
		self.bgcolor = ft.colors.BLUE_GREY_100
		self.color = ft.colors.BLACK

class CalculatorApp(ft.Container):
	def __init__(self):
		super().__init__()
		self.reset()

		self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
		self.expression = ft.Text(value="", color=ft.colors.GREY_500, size=24)
		self.width = 350
		self.bgcolor = ft.colors.BLACK
		self.border_radius = ft.border_radius.all(20)
		self.padding = 20
		self.content = ft.Column(
			controls=[
				ft.Row(controls=[self.expression], alignment=ft.MainAxisAlignment.END),
				ft.Row(controls=[self.result], alignment="end"),
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
						DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
						DigitButton(text=".", button_clicked=self.button_clicked),
						ActionButton(text="=", button_clicked=self.button_clicked),
					]
				),
			]
		)

	def button_clicked(self, e):
		data = e.control.data
		if data == "AC":
			self.expression.value = ""
			self.result.value = "0"
			self.reset()
		elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
			if self.result.value == "0" or self.result.value == "Error":
				self.result.value = data
			else:
				self.result.value += data
			self.expression.value += data
		elif data in ("+", "-", "*", "/"):
			self.expression.value += f" {data}"
			if self.operator:
				self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
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
					self.reset()
				except Exception:
					self.result.value = "Error"
					self.expression.value = "Error"
		elif data == "%":
			self.result.value = self.format_number(float(self.result.value) / 100)
			self.expression.value += "%"
		elif data == "+/-":
			if float(self.result.value) > 0:
				self.result.value = "-" + self.result.value
			elif float(self.result.value) < 0:
				self.result.value = str(abs(float(self.result.value)))
			self.expression.value = self.result.value
		self.update()

	def format_number(self, num):
		try:
			if isinstance(num, (int, float)) and num % 1 == 0:
				return int(num)
			return f"{float(num):,.10f}".replace(",", " ").rstrip("0").rstrip(".")
		except (ValueError, TypeError):
			return str(num)

	def calculate(self, operand1, operand2, operator):
		if operator == "+":
			return self.format_number(operand1 + operand2)
		elif operator == "-":
			return self.format_number(operand1 - operand2)
		elif operator == "*":
			return self.format_number(operand1 * operand2)
		elif operator == "/":
			if operand2 == 0:
				return "Error"
			else:
				return self.format_number(operand1 / operand2)

	def reset(self):
		self.operator = None
		self.operand1 = 0
		self.new_operand = False

def main(page: ft.Page):
	page.title = "Calc App"
	calc = CalculatorApp()
	page.add(calc)

ft.app(target=main)
