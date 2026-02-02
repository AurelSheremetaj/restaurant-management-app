from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from database_controller import RestaurantDatabaseMAnager


class TableOrderContentPanel(BoxLayout):
    vat_rate = 0.18  # 18% VAT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.size_hint = (1, 1)

        self.selected_row = -1
        self.selected_menu_item = None

        # List of dicts: {product, quantity, price}
        self.order_items = []

        self.restaurant_db_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )

        self.menu_items = self._fetch_menu_items()

        # UI create once
        self._build_ui()

    def create_content_panel(self):
        return self

    def _fetch_menu_items(self):
        # Fetch menu items from the database using MenuItemDatabaseManager
        try:
            menu_item_db_manager = self.restaurant_db_manager.menu_item_db_manager
        except AttributeError:
            from database_controller import MenuItemDatabaseManager
            menu_item_db_manager = MenuItemDatabaseManager(self.restaurant_db_manager.connection)
            self.restaurant_db_manager.menu_item_db_manager = menu_item_db_manager

        try:
            menu_items = []
            restaurants = self.restaurant_db_manager.get_restaurant_list()
            for restaurant in restaurants:
                for menu in restaurant.menu_list:
                    items = menu_item_db_manager.get_menu_items_by_menu(menu.menu_id)
                    menu_items.extend(items)
            return menu_items
        except Exception as e:
            self._show_popup("Database Error", f"Failed to fetch menu items: {str(e)}")
            return []

    # ---------------- UI ----------------
    def _build_ui(self):
        self.clear_widgets()

        main_layout = GridLayout(cols=2, spacing=10, padding=10)
        main_layout.size_hint = (1, None)
        main_layout.bind(minimum_height=main_layout.setter("height"))

        # Left panel: Menu Selection
        left_panel = BoxLayout(orientation="vertical", size_hint_x=0.5)

        menu_button = Button(
            text="▼  Menu Selection",
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        menu_button.bind(on_release=self._open_menu_dropdown)
        left_panel.add_widget(menu_button)

        self.menu_table = self._create_menu_table()
        left_panel.add_widget(self.menu_table)

        main_layout.add_widget(left_panel)

        # Right panel: Order Overview
        right_panel = BoxLayout(orientation="vertical", size_hint_x=0.5)

        order_overview_label = Label(
            text="Order Overview",
            size_hint_y=None,
            height=40,
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        right_panel.add_widget(order_overview_label)

        self.order_table = self._create_order_table()
        right_panel.add_widget(self.order_table)

        # Price summary labels
        self.subtotal_label = Label(text="Sub-Total: 0.00 €", size_hint_y=None, height=30, italic=True)
        self.vat_label = Label(text=f"VAT ({int(self.vat_rate * 100)}%): 0.00 €", size_hint_y=None, height=30)
        self.total_label = Label(text="Total: 0.00 €", size_hint_y=None, height=30, bold=True)

        right_panel.add_widget(self.subtotal_label)
        right_panel.add_widget(self.vat_label)
        right_panel.add_widget(self.total_label)

        # Buttons panel (2x2) - si në foto
        buttons_panel = GridLayout(
            cols=2,
            padding=0,
            spacing=10,
            size_hint_y=None,
            height=(40 * 2 + 10)
        )

        add_button = Button(text="Add", background_color=(0.2, 0.4, 0.8, 1), size_hint_y=None, height=40)
        delete_button = Button(text="Delete", background_color=(0.8, 0.2, 0.2, 1), size_hint_y=None, height=40)
        print_button = Button(text="Print Invoice", background_color=(0.2, 0.8, 0.2, 1), size_hint_y=None, height=40)
        order_button = Button(text="Order", background_color=(0.2, 0.4, 0.8, 1), size_hint_y=None, height=40)

        add_button.bind(on_release=self._add_item_to_order)
        delete_button.bind(on_release=self._delete_item_from_order)
        print_button.bind(on_release=self._print_invoice)
        order_button.bind(on_release=self._place_order)

        buttons_panel.add_widget(add_button)
        buttons_panel.add_widget(delete_button)
        buttons_panel.add_widget(print_button)
        buttons_panel.add_widget(order_button)

        right_panel.add_widget(buttons_panel)

        main_layout.add_widget(right_panel)

        # ScrollView FIX
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(main_layout)
        self.add_widget(scroll)

    def _create_menu_table(self):
        table_data = []
        for item in self.menu_items:
            table_data.append((item.name, f"{item.price:.2f} €"))

        menu_table = MDDataTable(
            size_hint=(1, 1),
            column_data=[
                ("Product", dp(40)),
                ("Price", dp(30))
            ],
            row_data=table_data,
            use_pagination=True,
            rows_num=10,
            check=True
        )
        menu_table.bind(on_row_press=self._on_menu_row_press)
        return menu_table

    def _create_order_table(self):
        order_table = MDDataTable(
            size_hint=(1, 1),
            column_data=[
                ("Product", dp(40)),
                ("Quantity", dp(30)),
                ("Price", dp(30))
            ],
            row_data=[],
            use_pagination=True,
            rows_num=10,
            check=True
        )
        order_table.bind(on_row_press=self._on_order_row_press)
        return order_table

    # ---------------- Events ----------------
    def _open_menu_dropdown(self, instance):
        # (Në këtë projekt menu-table është visible, prandaj s’kemi dropdown real)
        pass

    def _on_menu_row_press(self, instance_table, row):
        self.selected_row = int(row.index / len(instance_table.column_data))
        if 0 <= self.selected_row < len(self.menu_items):
            self.selected_menu_item = self.menu_items[self.selected_row]

    def _on_order_row_press(self, instance_table, row):
        self.selected_row = int(row.index / len(instance_table.column_data))

    def _add_item_to_order(self, instance):
        if not self.selected_menu_item:
            self._show_popup("Selection Error", "Please select a menu item to add.")
            return

        # if exists -> increase quantity
        for order_item in self.order_items:
            if order_item["product"] == self.selected_menu_item.name:
                order_item["quantity"] += 1
                order_item["price"] = order_item["quantity"] * float(self.selected_menu_item.price)
                self._refresh_order_table()
                self._update_price_summary()
                return

        # else -> add new
        self.order_items.append({
            "product": self.selected_menu_item.name,
            "quantity": 1,
            "price": float(self.selected_menu_item.price)
        })
        self._refresh_order_table()
        self._update_price_summary()

    def _delete_item_from_order(self, instance):
        if self.selected_row == -1 or self.selected_row >= len(self.order_items):
            self._show_popup("Selection Error", "Please select an order item to delete.")
            return

        del self.order_items[self.selected_row]
        self.selected_row = -1
        self._refresh_order_table()
        self._update_price_summary()

    # ---------------- Updates (si admin_view: update row_data + labels) ----------------
    def _refresh_order_table(self):
        row_data = []
        for item in self.order_items:
            row_data.append((item["product"], str(item["quantity"]), f"{item['price']:.2f} €"))
        self.order_table.row_data = row_data

    def _update_price_summary(self):
        subtotal = sum(float(item["price"]) for item in self.order_items)
        vat = subtotal * self.vat_rate
        total = subtotal + vat

        self.subtotal_label.text = f"Sub-Total: {subtotal:.2f} €"
        self.vat_label.text = f"VAT ({int(self.vat_rate * 100)}%): {vat:.2f} €"
        self.total_label.text = f"Total: {total:.2f} €"

    def _print_invoice(self, instance):
        if not self.order_items:
            self._show_popup("Order Empty", "No items in the order to print.")
            return

        invoice_text = "Invoice:\n"
        for item in self.order_items:
            invoice_text += f"{item['product']} x{item['quantity']} - {item['price']:.2f} €\n"

        subtotal = sum(float(item["price"]) for item in self.order_items)
        vat = subtotal * self.vat_rate
        total = subtotal + vat
        invoice_text += f"\nSub-Total: {subtotal:.2f} €\nVAT ({int(self.vat_rate*100)}%): {vat:.2f} €\nTotal: {total:.2f} €"

        self._show_popup("Invoice", invoice_text)

    def _place_order(self, instance):
        if not self.order_items:
            self._show_popup("Order Empty", "No items in the order to place.")
            return

        try:
            # Këtu pastaj lidhe me DB: save order + table_nr, etj.
            self._show_popup("Order Placed", "The order has been placed successfully.")

            self.order_items.clear()
            self._refresh_order_table()
            self._update_price_summary()
        except Exception as e:
            self._show_popup("Database Error", f"Failed to place order: {str(e)}")

    def _show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 300)
        )
        popup.open()
