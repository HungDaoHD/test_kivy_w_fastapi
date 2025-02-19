from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests


# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000"


class NumericInput(TextInput):
    """ Custom input field to allow only numbers """
    def insert_text(self, substring, from_undo=False):
        if substring.isdigit():
            return super().insert_text(substring, from_undo)


class MenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs, padding=10, spacing=10, **kwargs)

        self.selected_items = {}

        # Title
        self.title = Label(text="Select Drinks and Enter Quantity", size_hint_y=None, height=50, bold=True)
        self.add_widget(self.title)


        self.label = Label(text="Loading menu...", size_hint_y=None, height=40)
        self.add_widget(self.label)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=2, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        # Submit Button
        self.submit_button = Button(text="Submit Order", size_hint_y=None, height=50, on_press=self.submit_order)
        self.add_widget(self.submit_button)

        self.load_menu()





    def load_menu(self):
        try:
            response = requests.get(f"{API_URL}/menu")

            if response.status_code == 200:
                menu_items = response.json()["menu"]

                self.grid.clear_widgets()

                for item in menu_items:

                    # Checkbox with item name
                    item_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
                    checkbox = CheckBox(size_hint_x=None, width=30)
                    label = Label(text=f"{item['name']} - {item['price']}₫", size_hint_x=1)
                    item_box.add_widget(checkbox)
                    item_box.add_widget(label)

                    # Numeric input for quantity
                    quantity_input = NumericInput(hint_text="Qty", multiline=False, size_hint_y=None, height=40)
                    quantity_input.opacity = 0
                    quantity_input.disabled = True

                    # Store reference
                    self.selected_items[item['id']] = {
                        'checkbox': checkbox,
                        'name': item['name'],
                        'price': item['price'],
                        'quantity': quantity_input,
                    }

                    checkbox.bind(active=lambda cb, value, q=quantity_input: self.toggle_quantity(q, value))

                    # Add to grid
                    self.grid.add_widget(item_box)
                    self.grid.add_widget(quantity_input)


                self.label.text = "Menu Loaded"
            else:

                self.label.text = "Error loading menu"

        except Exception as e:
            self.label.text = f"Error: {e}"



    @staticmethod
    def toggle_quantity(quantity_input, is_checked):
        """ Show numeric input when checkbox is checked, hide otherwise """
        if is_checked:
            quantity_input.opacity = 1  # Show input box
            quantity_input.disabled = False  # Enable input box
        else:
            quantity_input.opacity = 0  # Hide input box
            quantity_input.disabled = True  # Disable input box
            quantity_input.text = ""  # Clear text when unchecked




    def submit_order(self, instance):

        order_list = list()

        for item_id, widgets in self.selected_items.items():
            if widgets["checkbox"].active:  # If checked

                quantity = widgets["quantity"].text
                item_name = widgets["name"]

                if quantity.isdigit() and int(quantity) > 0:

                    order_list.append({'item_id': item_id, 'quantity': int(quantity)})


        if order_list:
            try:
                response = requests.post(f"{API_URL}/order", json=order_list)

                if response.status_code == 200:

                    str_order = str()
                    total_price = int()

                    order_list = response.json()['lst_order']


                    for item in order_list:
                        str_order += f"{item['quantity']} x {self.selected_items[item['item_id']]['name']}: {self.selected_items[item['item_id']]['price'] * item['quantity']}\n"
                        total_price += self.selected_items[item['item_id']]['price'] * item['quantity']


                    self.label.text = f"Ordered Item: \n{str_order} Total: {total_price}"
                else:
                    self.label.text = "Order Failed"

            except Exception as e:
                self.label.text = f"Error: {e}"
        else:
            print("No items selected!")




class MyApp(App):
    def build(self):
        return MenuScreen()


if __name__ == "__main__":
    MyApp().run()
