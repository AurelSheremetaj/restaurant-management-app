from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.popup import Popup

from database_controller import RestaurantDatabaseMAnager
from enum1 import Status, UserRole


class OrderStatusContentpanel:
    def __init__(self, order_list=None, current_user_role=UserRole.COOK):
        self.selected_row = -1
        self.current_user_role = current_user_role

        # DB
        self.restaurant_database_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )

        # Data
        if order_list is not None:
            self.order_list = order_list
        else:
            # fetch nga DB nqs ekziston metoda
            self.order_list = (
                self.restaurant_database_manager.get_order_list()
                if hasattr(self.restaurant_database_manager, "get_order_list")
                else []
            )

        # UI refs (do krijohen te create_content_panel)
        self.split_layout_panel = None
        self.overview_label = None
        self.order_table = None

    # ---------------- UI BUILD ----------------
    def create_content_panel(self):
        # ✅ si admin_view: ruaj panelin si atribut
        self.split_layout_panel = GridLayout(cols=1, padding=10, spacing=20)

        # Header / dropdown (mund ta lesh thjesht button)
        self.split_layout_panel.add_widget(self._order_dropdown())

        # Overview label (ruaje si atribut qe ta perditesosh)
        self.overview_label = self._create_order_overview()
        self.split_layout_panel.add_widget(self.overview_label)

        # Table
        self.split_layout_panel.add_widget(self._create_order_table_panel())

        # Buttons
        self.split_layout_panel.add_widget(self._create_button_panel())

        return self.split_layout_panel

    def _order_dropdown(self):
        # e ke pas "Orders" – po e le te njejten
        button = Button(
            text="Orders",
            size_hint=(1, 0.1),
            background_color=(0, 0, 1, 1)
        )
        # nqs do dropdown real, e bejme me vone
        return button

    def _create_order_overview(self):
        # krijo label bosh, pastaj mbushe me text
        label = Label(
            text="",
            size_hint_y=None,
            height=30,
            color=(0, 0, 0, 1),
            halign="center",
            valign="middle",
        )
        self._recompute_overview_text(label)
        return label

    def _recompute_overview_text(self, label=None):
        if label is None:
            label = self.overview_label

        total_orders = len(self.order_list)
        queue_count = sum(1 for o in self.order_list if o.status == Status.QUEUE)
        in_progress_count = sum(1 for o in self.order_list if o.status == Status.IN_PROGRESS)
        ready_count = sum(1 for o in self.order_list if o.status == Status.READY)
        delivered_count = sum(1 for o in self.order_list if o.status == Status.DELIVERED)
        paid_count = sum(1 for o in self.order_list if o.status == Status.PAID)

        label.text = (
            f"Order overview: Total: {total_orders} | "
            f"Queue: {queue_count} | In Progress: {in_progress_count} | "
            f"Ready: {ready_count} | Delivered: {delivered_count} | Paid: {paid_count}"
        )

    def _create_order_table_panel(self):
        # krijo row_data nga lista aktuale
        table_row_data = self._build_table_row_data(self.order_list)

        self.order_table = MDDataTable(
            pos_hint={"center_x": 0.5, "center_y": 0},
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Table-Nr.", dp(40)),
                ("Status", dp(40)),
            ],
            row_data=table_row_data,
        )
        return self.order_table

    def _build_table_row_data(self, orders):
        table_row_data = []
        for order in orders:
            # nqs order.table_number eshte int -> e formaton si Table #1
            table_row_data.append(
                (f"Table #{order.table_number}", order.status.name.replace("_", " "))
            )
        return table_row_data

    def _create_button_panel(self):
        panel = GridLayout(cols=3, spacing=20, padding=0)

        update_button = Button(
            text="Update Status",
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0, 0, 1, 1),
        )
        revert_button = Button(
            text="Revert Status",
            size_hint=(None, None),
            size=(150, 40),
            background_color=(0, 1, 0, 1),
        )
        refresh_button = Button(
            text="Refresh",
            size_hint=(None, None),
            size=(150, 40),
            background_color=(1, 0, 0, 1),
        )

        update_button.bind(on_press=self.update_status)
        revert_button.bind(on_press=self.revert_status)
        refresh_button.bind(on_press=self.refresh)

        panel.add_widget(update_button)
        panel.add_widget(revert_button)
        panel.add_widget(refresh_button)

        return panel

    # ---------------- DATA UPDATE (si admin_view) ----------------
    def update_order_table_data(self, order_model_data):
        # ✅ si admin_view: vetem ndrysho row_data
        self.order_table.row_data = self._build_table_row_data(order_model_data)

    # ---------------- ACTIONS ----------------
    def refresh(self, instance=None):
        # ✅ mos e rinderto UI - vetem perditeso data
        if hasattr(self.restaurant_database_manager, "get_order_list"):
            self.order_list = self.restaurant_database_manager.get_order_list()
        else:
            # fallback: mbaj listen ekzistuese
            self.order_list = [o for o in self.order_list if o.status != Status.PAID]

        # update table + overview
        self.update_order_table_data(self.order_list)
        self._recompute_overview_text()

    def update_status(self, instance):
        selected_rows = self.order_table.get_row_checks()
        if not selected_rows:
            self._show_popup("No selection", "Please select a row to update.")
            return

        for row in selected_rows:
            index = row.index
            order = self.order_list[index]
            current_status = order.status

            # ✅ Cook logic (sipas specifikimit tipik)
            if self.current_user_role == UserRole.COOK:
                if current_status == Status.QUEUE:
                    new_status = Status.IN_PROGRESS
                elif current_status == Status.IN_PROGRESS:
                    new_status = Status.READY
                else:
                    self._show_popup("Invalid status change", f"Cook cannot update from {current_status.name}")
                    continue

            # ✅ Waiter logic (nqs e perdor edhe waiter)
            elif self.current_user_role == UserRole.WAITER:
                if current_status == Status.READY:
                    new_status = Status.DELIVERED
                elif current_status == Status.DELIVERED:
                    new_status = Status.PAID
                else:
                    self._show_popup("Invalid status change", f"Waiter cannot update from {current_status.name}")
                    continue

            else:
                new_status = self._next_status(current_status)

            # ruaje ne DB nqs ekziston metoda
            if hasattr(self.restaurant_database_manager, "update_order_status"):
                self.restaurant_database_manager.update_order_status(order.id, new_status)
            else:
                order.status = new_status  # fallback in-memory

        self.refresh()

    def revert_status(self, instance):
        selected_rows = self.order_table.get_row_checks()
        if not selected_rows:
            self._show_popup("No selection", "Please select a row to revert.")
            return

        for row in selected_rows:
            index = row.index
            order = self.order_list[index]
            current_status = order.status

            if self.current_user_role == UserRole.COOK:
                if current_status == Status.IN_PROGRESS:
                    new_status = Status.QUEUE
                elif current_status == Status.READY:
                    new_status = Status.IN_PROGRESS
                else:
                    self._show_popup("Invalid status revert", f"Cook cannot revert from {current_status.name}")
                    continue

            elif self.current_user_role == UserRole.WAITER:
                if current_status == Status.PAID:
                    new_status = Status.DELIVERED
                elif current_status == Status.DELIVERED:
                    new_status = Status.READY
                else:
                    self._show_popup("Invalid status revert", f"Waiter cannot revert from {current_status.name}")
                    continue

            else:
                new_status = self._previous_status(current_status)

            if hasattr(self.restaurant_database_manager, "update_order_status"):
                self.restaurant_database_manager.update_order_status(order.id, new_status)
            else:
                order.status = new_status

        self.refresh()

    # ---------------- HELPERS ----------------
    def _next_status(self, current_status):
        order = [Status.QUEUE, Status.IN_PROGRESS, Status.READY, Status.DELIVERED, Status.PAID]
        i = order.index(current_status) if current_status in order else 0
        return order[min(i + 1, len(order) - 1)]

    def _previous_status(self, current_status):
        order = [Status.QUEUE, Status.IN_PROGRESS, Status.READY, Status.DELIVERED, Status.PAID]
        i = order.index(current_status) if current_status in order else 0
        return order[max(i - 1, 0)]

    def _show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
