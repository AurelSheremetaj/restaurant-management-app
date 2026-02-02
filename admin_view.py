import random
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField
from data_provider1 import DataProvider
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from admin_controller import RestaurantManagerController,MenuItemManagerController,MenuManagerController,TableManagerController
from model import Restaurant,Menu,Menu_Item,Table
from kivy.uix.popup import Popup
from database_controller import RestaurantDatabaseMAnager
import hashlib

class RestaurantManagerContentPanel:
    def __init__(self):
        self.selected_row = -1
        self.restaurant_database_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )
        self.restaurant_manager_controller = RestaurantManagerController()
        self.restaurant_list = self.restaurant_database_manager.get_restaurant_list()
        self.selected_restaurant = None
        self.name_input = ""
        self.address_input = ""
    
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_restaurant_management_input_data_panel())
        split_layout_panel.add_widget(self._create_restaurant_list_panel())
        return split_layout_panel
    
    
    def _create_restaurant_management_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1,padding = 30,spacing = 20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        
        self.restaurant_name_input = MDTextField(multiline = True,font_size = '18sp',hint_text = 'Restaurant name')
        input_data_component_panel.add_widget(self.restaurant_name_input)
        
        self.restaurant_address_input = MDTextField(multiline = True,font_size = '18sp',hint_text = 'Restaurant address')
        input_data_component_panel.add_widget(self.restaurant_address_input)
        
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel
    
    def _create_restaurant_list_panel(self):
        content_panel = GridLayout(cols =1,spacing = 10)
        content_panel.add_widget(self._create_restaurant_dropdown())
        content_panel.size_hint_x= None
        content_panel.width = 1200
        content_panel.add_widget(self._create_restaurant_table_panel())
        return content_panel
    
    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols =3,spacing = 10,padding = 0)
        add_button = Button(text ='Add',size_hint = (None,None),size=(100,40),background_color = (0,0,128))
        update_button = Button(text ='Update',size_hint = (None,None),size = (100,40),background_color = (255,0,255))
        delete_button = Button(text='Delete',size_hint = (None,None),size = (100,40),background_color =(128,0,0)) 
        
        add_button.bind(on_press = self.add_restaurant)
        update_button.bind(on_press = self.update_restaurant)
        delete_button.bind(on_press = self.delete_restaurant)
        
        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_button)
        button_component_panel.add_widget(delete_button)
        
        return button_component_panel
    
    def  _create_restaurant_table_panel(self):
        table_panel = GridLayout(cols=1,padding = 10,spacing = 0)
        self.restaurant_table = self.create_table()
        
        self.restaurant_table.bind(on_check_press = self._checked)
        self.restaurant_table.bind(on_row_press = self._on_row_press)
        
        table_panel.add_widget(self.restaurant_table)
        return table_panel
    
    def _create_restaurant_dropdown(self):
        button = Button(text='Restaurant List',size_hint= (1,0.1),background_color = (0,0,1,1) )
        button.bind(on_release = self.show_menu)
        return button
    
    #def create_table(self):
     #   table_row_data = []
        
        self.restaurant = self.restaurant_list[0]
                
        
        
        for restaurant in self.restaurant_list:
            
            table_row_data.append((restaurant.id, restaurant.name, restaurant.address))
            
        self.restaurant_table = MDDataTable(
            pos_hint = {'center_x':0.5,'center_y':0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("ID", dp(40)),
                ("Restaurant name", dp(40)),
                ("Restaurant address", dp(30))
            ],
            row_data = table_row_data
        )
        return self.restaurant_table
    
    

    def _id4(self, uuid_value: str) -> str:
        h = hashlib.md5(str(uuid_value).encode()).hexdigest()
        num = int(h[:8], 16) % 9000 + 1000
        return str(num)


    def create_table(self):
        table_row_data = []

        for restaurant in self.restaurant_list:
            short_id = self._id4(restaurant.id)

            table_row_data.append((short_id, restaurant.name, restaurant.address))

        self.restaurant_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
         check=True,
         use_pagination=True,
         rows_num=10,
         column_data=[
              ("ID", dp(25)),                 # mund ta ngushtosh pak
              ("Restaurant name", dp(45)),
              ("Restaurant address", dp(45)),
         ],
         row_data=table_row_data
        )
        return self.restaurant_table

    
    def show_menu(self,button):
        menu_item = []
        restaurant_list = self.restaurant_list
        
        for restaurant in restaurant_list:
            menu_item.append(
                {
                    "viewclass": "OneLineListItem",
                    "text":restaurant.name,
                    "on_release": lambda r=restaurant: self._restaurant_data_table(r)
                    }
                )
            
        self.dropdown = MDDropdownMenu(
            caller = button,
            items = menu_item,
            width_mult = 5,
            max_height = dp(150), 
        )       
        self.dropdown.open()
   
    def _restaurant_data_table(self,restaurant):
        self.restaurant = restaurant
        table_row_data = []
        restaurants = self.restaurant_list[0]
        for restaurant in restaurants:
            table_row_data.append((restaurant.id,restaurant.name,restaurant.address))
            self.restaurant_table_row_data = table_row_data
        
   
    def _checked(self, instance_table, current_row):
    # gjej index-in e rreshtit në table
        try:
            idx = instance_table.row_data.index(current_row)
        except ValueError:
            return

    # merre restaurant-in real (me UUID) nga lista
        self.selected_restaurant = self.restaurant_list[idx]

        self.restaurant_name_input.text = self.selected_restaurant.name
        self.restaurant_address_input.text = str(self.selected_restaurant.address or "")

   
    #def _checked(self,instance_table,current_row):
     #   self.selected_restaurant = Restaurant(current_row[0],current_row[1],current_row[2],[])
        
      #  self.restaurant_name_input.text  = self.selected_restaurant.name
       # self.restaurant_address_input.text = self.selected_restaurant.address
        
        
        
    def _on_row_press(self,instance,row):
        self.selected_row = int(row.index / len(instance.column_data))
        
        
    def add_restaurant(self,instance):
        name = self.restaurant_name_input.text 
        address = self.restaurant_address_input.text
        
        restaurant_data = []
        restaurant_data.append(name)
        restaurant_data.append(address)
        
        
        if self._is_data_valid(restaurant_data):
            # use data provider to get list of restaurants and pass in add_restaurant method as parameter
            new_restaurant = self.restaurant_manager_controller.add_restaurant(
                self.restaurant_list, restaurant_data
            )
            self.restaurant_table.row_data.append([new_restaurant.id,new_restaurant.name,new_restaurant.address])
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content = Label(text = "Provide mandatory data to add a new restaurant"),
                size_hint = (None,None),
                size = (400,200)
            )
            popup.open()
    
            
    def update_restaurant(self,instance):
        if self.selected_row != - 1:
            name = self.restaurant_name_input.text
            address = self.restaurant_address_input.text
            
            
            updated_restaurant_data = [name,address]
            
        if self._is_data_valid(updated_restaurant_data):
            self.restaurant_manager_controller.update_restaurant(self.restaurant_list,self.selected_restaurant.id,updated_restaurant_data)
            table_row_data = []
            restaurant_list = self.restaurant_list
            for restaurant in restaurant_list:
                table_row_data.append([restaurant.id,restaurant.name,restaurant.address])
            self.restaurant_table.row_data = table_row_data
            self._clear_input_text_fields()
            
 
            
    def delete_restaurant(self,instance):
        
        if self.selected_row != -1:
            restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]
            
            del self.restaurant_table.row_data[self.selected_row]
            self.restaurant_manager_controller.delete_restaurant(self.restaurant_list, restaurant_to_remove)
            
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title= "Invalid data",
                content = Label(text = "Select any row to delete"),
                size_hint = (None,None),
                size = (400,200)
            )   
            popup.open()
       
    def _clear_input_text_fields(self):
        self.restaurant_name_input.text = ""
        self.restaurant_address_input.text = ""
        self.selected_row = -1
        
    def _is_data_valid(self,restaurant_data):
        return(
            restaurant_data[0] != ""
            and restaurant_data[1] != ""
        )    
class MenuItemManagerContentPanel:
    def __init__(self):
        self.restaurant_database_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )
        self.menuitem_manager_controller = MenuItemManagerController(self.restaurant_database_manager.connection)
        self.restaurant_list = self.restaurant_database_manager.get_restaurant_list()
        self.restaurant = self.restaurant_list[0] if self.restaurant_list else None
        self.menu = self.restaurant.menu_list[0] if self.restaurant and self.restaurant.menu_list else None
        self.restaurant_selector = None
        self.menu_selector = None
        self.selected_menuitem = None
        self.selected_row = -1

    
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols = 2)
        split_layout_panel.add_widget(self._create_menu_item_manager_input_data_panel())
        split_layout_panel.add_widget(self._create_management_app())
        return split_layout_panel
    
    def _create_menu_item_manager_input_data_panel(self):
        input_data_component_panel = GridLayout(cols = 1,padding =30,spacing = 20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        
        self.id_input = MDTextField(multiline = False,font_size = '18sp',hint_text = 'Menu Item Id')
        input_data_component_panel.add_widget(self.id_input)
        self.name_input = MDTextField(multiline = False,font_size = '18sp',hint_text = 'Menu Item name')
        input_data_component_panel.add_widget(self.name_input)
        self.price_input = MDTextField(multiline = False,font_size = '18sp',hint_text = 'Menu Item price')
        input_data_component_panel.add_widget(self.price_input)
        input_data_component_panel.add_widget(self._create_priority_input_data_panel())
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel
    
    def _create_priority_input_data_panel(self):
        priority_input_label = GridLayout(cols = 2,spacing = 20)
        priority_input_label.size_hint = (None,None)
        priority_options = ["Meal","Drink"]
        self.priority_checkboxes = {}
        
        for priority in priority_options:
            checkbox = CheckBox(group = 'priority',active = False,color = (0,0,0,1) )
            checkbox_label = Label(text = priority,color = (0,0,0,1))
            priority_input_label.add_widget(checkbox)
            priority_input_label.add_widget(checkbox_label)
            self.priority_checkboxes[priority] = checkbox
        return priority_input_label

    def _checked(self, instance_table, current_row):
        self.selected_menu_item = Menu_Item(
            current_row[0], current_row[1], current_row[2], "", ""
        )

        self.id_input.text= str(self.selected_menu_item.id)
        self.name_input.text = str(self.selected_menu_item.name)
        self.price_input.text= str(self.selected_menu_item.price)

        # Set priority checkboxes based on selected menu item priority
        for priority, checkbox in self.priority_checkboxes.items():
            checkbox.active = (priority == getattr(self.selected_menu_item, 'priority', ''))
        
    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index/len(instance.column_data))


    def _create_management_app(self):
        content_panel = GridLayout(cols = 1,spacing = 10)
        content_panel.size_hint_x = None
        content_panel.width = 800
        content_panel.add_widget(self._create_restaurant_dropdown())
        content_panel.add_widget(self._create_menu_dropdown())
        # TODO add menu as parameter
        # TODO get menu from selected restaurant 
        if self.menu is not None:
            content_panel.add_widget(self._create_table(self.menu))
        else:
            # Add an empty placeholder or label if no menu is available
            content_panel.add_widget(Label(text="No menu available"))
        return content_panel
    
    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols = 3,padding = 0,spacing = 10)
        add_button  = Button(text = 'Add',size_hint = (None,None),size =(100,40),background_color = (0,0,128) )
        add_button.bind(on_release=self._add_menu_item)
        update_button = Button(text = 'Update',size_hint = (None,None),size = (100,40),background_color = (255,0,255))
        update_button.bind(on_release=self._update_menuitem)
        delete_button = Button(text = 'Delete',size_hint = (None,None),size = (100,40),background_color = (128,0,0))
        delete_button.bind(on_release=self._delete_menuitem)
        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)
        return buttons_component_panel
    
    
    def _create_restaurant_dropdown(self):
        button = Button(text = 'Restaurant Selection',size_hint = (1,0.1),background_color =(0,0,0,1))
        button.bind(on_release = self._open_restaurant_dropdown)
        return button
    
    def _open_restaurant_dropdown(self,button):
        menu_item = []
        restaurant_list = self.restaurant_list
        
        for restaurant in restaurant_list:
            menu_item.append(
                {
                    "viewclass": "OneLineListItem",
                    "text":restaurant.name,
                    "on_release": lambda r=restaurant: self.on_restaurant_selection(r)
                    }
                )
            
        self.menu_selector = MDDropdownMenu(
            caller = button,
            items = menu_item,
            width_mult = 5,
            max_height = dp(150), 
        )       
        self.menu_selector.open()

    def on_restaurant_selection(self, restaurant):
        self.restaurant = restaurant
        self.menu_selector.dismiss()
        self.update_menu_list(restaurant)
        
         
        
    def _create_menu_dropdown(self):
        button = Button(text = 'Menu Selection',size_hint = (1,0.1),background_color =(1,1,1,1))
        button.bind(on_release = self._show_menu_list)
        return button
    
    def _show_menu_list(self, button):
        menu_items = []
        # Collect menu items from all restaurants
        for restaurant in self.restaurant_list:
            for menu in restaurant.menu_list:
                for menu_item in menu.menu_item_list:
                    menu_items.append(
                        {
                            "viewclass": "OneLineListItem",
                            "text": f"ID: {menu_item.id} | Name: {menu_item.name} | Price: {menu_item.price}",
                            "on_release": lambda mi=menu_item: self._on_menu_item_select(mi)
                        }
                    )
            
        self.menu_selector = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=8,
            max_height=dp(200), 
        )       
        self.menu_selector.open()

    def _on_menu_item_select(self, menu_item):
        self.menu_selector.dismiss()
        self.selected_menu_item = menu_item
        self.id_input.text = str(menu_item.id)
        self.name_input.text = menu_item.name
        self.price_input.text = str(menu_item.price)
        if hasattr(self, 'menu_selection_button'):
            self.menu_selection_button.text = f"{menu_item.name} (${menu_item.price})"

    def _create_menu_dropdown(self):
        button = Button(
            text='Menu Selection',
            size_hint=(1, 0.1),
            background_color=(1, 1, 1, 1)
        )
        button.bind(on_release=self._show_menu_list)
        self.menu_selection_button = button
        return button
        
    def _create_table(self,menu):
        table_row_data = []
        
        if menu is None:
            # Return an empty table if menu is None
            self.menu_item_table = MDDataTable(
                pos_hint = {'center_x':0.5,'center_y':0.5},
                check = True,
                use_pagination = True,
                rows_num = 10,
                column_data=[
                    ("Id", dp(40)),
                    ("Name", dp(30)),
                    ("Price", dp(30)) 
                ],
                row_data = []
            )
            return self.menu_item_table
        
        menu_item_list = menu.menu_item_list
        
        for menu_item in menu_item_list:
            # Generate random 4-digit number
            random_id = str(random.randint(1000, 9999))
            table_row_data.append((random_id,menu_item.name,menu_item.price))
        
        self.menu_item_table = MDDataTable(
            pos_hint = {'center_x':0.5,'center_y':0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data=[
                ("Id", dp(40)),
                ("Name", dp(30)),
                ("Price", dp(30)) 
            ],
            row_data = table_row_data
        )
    
        self.menu_item_table.bind(on_check_press = self._checked)
        self.menu_item_table.bind(on_row_press = self._on_row_press)
        return self.menu_item_table
    
    def _checked(self, instance_table, current_row):
        self.selected_menu_item = Menu_Item(
            current_row[0], current_row[1], current_row[2], "", ""
        )

        self.id_input.text= str(self.selected_menu_item.id)
        self.name_input.text = str(self.selected_menu_item.name)
        self.price_input.text= str(self.selected_menu_item.price)
        
        
    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index/len(instance.column_data))

    def _clear_input_text_fields(self):
        self.name_input.text = ""
        self.price_input.text = ""
        self.selected_row = -1
        # Clear priority checkboxes
        for checkbox in self.priority_checkboxes.values():
            checkbox.active = False

    def _get_selected_priority(self):
        for priority, checkbox in self.priority_checkboxes.items():
            if checkbox.active:
                return priority
        return None

    def _is_data_valid(self, task_data):
        return (
            task_data[0] != ""
            and task_data[1] != ""
            and task_data[2] != ""
        )


    def _add_menu_item(self, instance):
        if self.menu is None:
            self._show_error_popup("No menu selected", "Please select a menu before adding a menu item.")
            return

        id = self.id_input.text
        name = self.name_input.text
        price_text = self.price_input.text
        description = ""  # No input field for description, set empty or add input field if needed
        priority = self._get_selected_priority()

        try:
            price = float(price_text)
        except ValueError:
            self._show_error_popup("Invalid data", "Price must be a numeric value")
            return

        menu_item_data = [id, name, price, description, priority]

        if self._is_data_valid(menu_item_data[:3] + ["dummy"]):  # to satisfy _is_data_valid expecting 3 elements
            self.menuitem_manager_controller.add_menuitem(self.menu, menu_item_data)

            self.menu_item_table.row_data.append([id, name, price])

            self._clear_input_text_fields()

        else:
            self._show_error_popup("Invalid data", " Provide mandatory data to add a new Menu item")
            
    def _update_menuitem(self, instance):
        if self.selected_row != -1: 

            name = self.name_input.text
            price_text = self.price_input.text
            priority = self._get_selected_priority()
            # id = self.id_input.text

            try:
                price = float(price_text)
            except ValueError:
                self._show_error_popup("Invalid data", "Price must be a numeric value")
                return

            menu_item_data = [name, price, priority]

            if self._is_data_valid(menu_item_data[:2] + ["dummy"]):  # to satisfy _is_data_valid expecting 3 elements
                menu_item_to_remove = self.menu_item_table.row_data[self.selected_row]

                del self.menu_item_table.row_data[self.selected_row]

                self.menuitem_manager_controller.update_menuitem(menu_item_to_remove[0], menu_item_data, self.menu)
                self.menu_item_table.row_data.append([name, price, priority])

                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to update the Menu Item")

        else:
                self._show_error_popup("Invalid data", "Select any row to update")
                
    def _delete_menuitem(self, instance):
        if self.selected_row != -1:
            menuitem_to_remove = self.menu_item_table.row_data[self.selected_row]

            del self.menu_item_table.row_data[self.selected_row]
            self.menuitem_manager_controller.delete_menuitem(self.menu, menuitem_to_remove[0])

            self._clear_input_text_fields()

        else:
            self._show_error_popup("Invalid data", "Select any row to delete")
            
    def _show_error_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
        
    def update_menu_list(self, restaurant):

        menu_items = []
        menus = restaurant.menu_list
        for menu in menus:
            menu_items.append({"viewclass": "OneLineListItem", "text": menu.name,
                            "on_release": lambda m=menu: self.update_menuitem_table(m)})

        self._show_menu_list(None)
        self.menu_selector.items = menu_items
        self.menu_selector.dismiss()
        if menus:
            self._update_data_table(menus[0])
        else:
            # Clear the menu item table if no menus exist
            if hasattr(self, 'menu_item_table'):
                self.menu_item_table.row_data = []
        
        
    def _update_data_table(self, menu):
        self.menu = menu
        table_row_data = []
        menuitems = menu.menu_item_list 

        for menu_item in menuitems:
            table_row_data.append(
                (menu_item.id, menu_item.name, menu_item.price)
            )

        self.menu_item_table.row_data = table_row_data


class MenuManagerContentPanel:
    def __init__(self):
        self.selected_row = -1
        self.restaurant_database_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )
        self.menu_manager_controller = MenuManagerController(self.restaurant_database_manager.connection)
        self.restaurant_list = self.restaurant_database_manager.get_restaurant_list()
        # Remove local variable assignment
        # menu_manager_controller = MenuItemManagerContentPanel()
        
        
        
        
        
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_menu_management_panel())
        return split_layout_panel
    
    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1,padding =30,spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400
        
        #menu name
        self.name_input = MDTextField(mode = "rectangle",size_hint = (0.9,0.1),hint_text = 'Menu name')
        input_data_component_panel.add_widget(self.name_input)
        self.menu_section_input = MDTextField(mode = "rectangle",size_hint = (0.9,0.1),hint_text = "Menu section")
        input_data_component_panel.add_widget(self.menu_section_input)
        
        input_data_component_panel.add_widget(self._create_button_component_panel())
        return input_data_component_panel
    
    def _create_menu_management_panel(self):
        content_panel = GridLayout(cols=1,spacing = 10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel
    
    def _create_button_component_panel(self):
        button_component_panel = GridLayout(cols=3,padding = 0,spacing = 10)
        add_button = Button(text = "Add" ,size_hint = (None, None),size=(100,40),background_color = (0,0,128))
        delete_button = Button(text = "Delete" ,size_hint = (None, None),size=(100,40),background_color = (255,0,255))
        update_button = Button(text = "Update" ,size_hint = (None, None),size=(100,40),background_color = (128,0,0))
        add_button.bind(on_press = self._add_menu)
        delete_button.bind(on_press = self._delete_menu)
        update_button.bind(on_press = self._update_menu)
        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(delete_button)
        button_component_panel.add_widget(update_button)
        return button_component_panel
    
    def _create_table_panel(self):
        table_panel = GridLayout(cols=1,padding = 10,spacing = 0)
        self.menu_table  = self.create_table()
        table_panel.add_widget(self.menu_table)
        self.menu_table.bind(on_check_press = self._checked)
        self.menu_table.bind(on_row_press = self._on_row_press)
        
        return table_panel
    
    def _create_restaurant_selector(self):
        button = Button(text = "Menu list",size_hint = (1,0.1),background_color = (0,1,8,1))
        button.bind(on_release = self.show_menu)
        return button
    
    def create_table(self):
        table_row_data = []
        self.restaurant = self.restaurant_list[0]
        menus = self.restaurant.menu_list
        
        for menu in menus:
            # Format menu_id to last 4 digits
            short_menu_id = str(menu.menu_id)[-4:]
            table_row_data.append((menu.name, short_menu_id))
            
        self.menu_table = MDDataTable(
            pos_hint = {'center_x':0.5,'center_y':0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("Name",dp(40)),
                ("Menu Selection",dp(30))
            ],
            row_data = table_row_data
            
        )
        return self.menu_table
    def show_menu(self,button):
        menu_items = []
        restaurant_list = self.restaurant_list
        
        for restaurant in restaurant_list:
            menu_items.append({"viewclass":"OneLineListItem",
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r),
                               }
                              )
        self.dropdown = MDDropdownMenu(
            caller = button,
            items = menu_items,
            width_mult = 5,
            max_height = dp(150),
        )
        self.dropdown.open()
        
    def _checked(self,instance_table,curent_row):
        selected_menu = Menu(curent_row[0],curent_row[1],[])
        self.name_input.text = str(selected_menu.name)
        # self.menu_section_input.text = str(selected_menu.menu_section)  # Removed because Menu has no menu_section attribute
        
        
    def _on_row_press(self,instance,row):
        self.selected_row = int(row.index/len(instance.column_data))
        
    def _update_data_table(self,restaurant):
        self.restaurant = restaurant
        
        table_row_data = []
        menus = restaurant.menu_list
        for menu in menus:
            table_row_data.append(
                (menu.name, menu.menu_id)
            )
        self.menu_table.row_data = table_row_data
        
    def _add_menu(self,instance):
        
        name = self.name_input.text
        menu_selection = self.menu_section_input.text
        
        menu_data = []
        menu_data.append(name)
        menu_data.append(menu_selection)
        
        if self._is_data_valid(menu_data):
            self.menu_manager_controller.add_menu(
                self.restaurant,menu_data
            )
            self.menu_table.row_data.append((name,menu_selection))
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content = Label(text= "Provide mandatory data to add a new Menu"),
                size_hint = (400,200),
            )
            popup.open()
            
    def _update_menu(self,instance):
            if self.selected_row  != -1:
                name = self.name_input.text
                menu_selection = self.menu_section_input.text 
                
                menu_data = []
                menu_data.append(name)
                menu_data.append(menu_selection)
                
                if self._is_data_valid(menu_data):
                    menu_to_remove = self.menu_table.row_data[self.selected_row]
                    
                del self.menu_table.row_data[self.selected_row]
                self.menu_manager_controller.delete_menu(
                    self.restaurant,menu_to_remove
                )
                self.menu_manager_controller.add_menu(
                    self.restaurant,menu_data
                )
                self.menu_table.row_data.append([name,menu_selection])
                self._clear_input_text_fields()
            else:
                popup = Popup(
                    title = "Invalid data",
                    content = Label(text = "Provde mandatory data to uodate the Menu"),
                    size_hint = (None,None),
                    size = (400,200)
                )
                popup.open()
    
    def _delete_menu(self,instance):
        if self.selected_row  != -1:
            menu_to_remove = self.menu_table.row_data[self.selected_row]
            
            del self.menu_table.row_data[self.selected_row]
            self.menu_manager_controller.delete_menu(
                self.restaurant,menu_to_remove
            )
            
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content = Label(text ="Select any row to delete"),
                size_hint = (None,None),
                size = (400,200),
            )
            popup.open()
            
    def _clear_input_text_fields(self):
        self.name_input.text = " "
        self.menu_section_input.text = " "
        self.selected_row = -1
        
    def _is_data_valid(self,menu_data):
        return(
            menu_data[0]  != " "
            and menu_data[1] != "" 
        )
        
class TableManagerContentPanel:
    def __init__(self):
        self.selected_row = -1
        self.restaurant_database_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )
        self.table_manager_controller = TableManagerController(self.restaurant_database_manager.connection)
        self.restaurant_list = self.restaurant_database_manager.get_restaurant_list()
    
    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_table_input_data_panel())
        # Add a vertical layout to hold the buttons and table management panel
        right_panel = GridLayout(cols=1, spacing=10)
        right_panel.size_hint_x = None
        right_panel.width = 1200
        # Add both buttons to the right panel
        right_panel.add_widget(self._create_restaurant_selector())
        right_panel.add_widget(self._create_table_list_button())
        right_panel.add_widget(self._create_table_management_panel())
        split_layout_panel.add_widget(right_panel)
        return split_layout_panel
    
    def _create_table_input_data_panel(self):
        input_data_component_panel =GridLayout(cols = 1,padding= 30,spacing = 20)
        input_data_component_panel.size_hint_x  = None
        input_data_component_panel.width = 400
        
        self.id_input = MDTextField(mode = "rectangle",size_hint = (0.9,0.1),hint_text = "Table Id")
        input_data_component_panel.add_widget(self.id_input)
        self.seats_input = MDTextField(mode = "rectangle",size_hint = (0.9,0.1),hint_text = "Table seats")
        input_data_component_panel.add_widget(self.seats_input)
        
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel
    
    def _create_table_management_panel(self):
        content_panel = GridLayout(cols = 1,spacing = 10)
        # Removed duplicate restaurant selector button to avoid two "Select a restaurant" buttons
        # content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x  = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def show_restaurant_list(self, button):
        menu_items = []
        for restaurant in self.restaurant_list:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": restaurant.name,
                "on_release": lambda r=restaurant: self.update_data_table(r)
            })
        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=5,
            max_height=dp(150),
        )
        self.dropdown.open()
    
    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols = 2,padding = 0,spacing = 40)
        add_button = Button(text = "Add",size_hint = (None,None),size = (100,40),background_color = (0,0,255))
        update_button = Button(text = "Update",size_hint = (None,None),size = (100,40),background_color = (255,0,255))
        delete_button = Button(text = "Delete",size_hint = (None,None),size = (100,40),background_color = (128,0,0))
        update_button.bind(on_press = self._update_table)
        add_button.bind(on_press = self._add_table)
        delete_button.bind(on_press = self._delete_table)
        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_button)
        button_component_panel.add_widget(delete_button)
        return button_component_panel
    
    def _create_table_panel(self):
        table_panel = GridLayout(cols =1,padding = 10,spacing = 0)
        self.table_table = self.create_table()
        table_panel.add_widget(self.table_table)
        self.table_table.bind(on_check_press = self._checked)
        self.table_table.bind(on_row_press = self._on_row_press)
        
        return table_panel
    

    def _create_restaurant_selector(self):
        button = Button(text = "Select a restaurant", size_hint = (1,0.1),background_color = (0,0,0,1))
        button.bind(on_release = self.show_restaurant_list)
        return button 
    
    def _create_table_list_button(self):
        button = Button(text = "Table list" , size_hint = (1,0.1),background_color = (8,8,0,1))
        button.bind(on_release=self.show_table_list)
        return button

    def show_table_list(self, button):
        menu_items = []
        if self.restaurant:
            for table in self.restaurant.table_list:
                seats_count = len(table.seats_list) if table.seats_list else 0
                menu_items.append({
                    "viewclass": "OneLineListItem",
                    "text": f"Table {table.id} - Seats: {seats_count}",
                    "on_release": lambda t=table: self.select_table(t)
                })
            self.dropdown = MDDropdownMenu(
                caller=button,
                items=menu_items,
                width_mult=5,
                max_height=dp(150),
            )
            self.dropdown.open()

    def select_table(self, table):
        self.dropdown.dismiss()
        self.id_input.text = str(table.id)
        seats_count = len(table.seats_list) if table.seats_list else 0
        self.seats_input.text = str(seats_count)
        # Optionally update selected_row or other UI elements if needed
    
    def create_table(self):
        table_row_data = []
        self.restaurant = self.restaurant_list[0]
        tables = self.restaurant.table_list
        
        for table in tables:
            # Generate random 4-digit number
            random_id = str(random.randint(1000, 9999))
            table_row_data.append((random_id,table.seats))
            
        self.table_table = MDDataTable(
            pos_hint = {"center_x":0.5,"center_y":0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("ID",dp(40)),
                ("Seats",dp(30))
            ],
            row_data = table_row_data
        )
        return self.table_table
        
    def show_data(self,button):
        table_items = []
        restaurant_list = self.restaurant_list
        
        for restaurant in restaurant_list:
            table_items.append({"viewclass": "OneLineListItem",
                                "text":restaurant.name,
                                "on_release":lambda r = restaurant: self._update_data_table(r)
                                }
                               )
            self.dropdown = MDDropdownMenu(
            caller = button,
            items = table_items,
            width_mult = 5,
            max_height = dp(150),
            )
            self.dropdown.open()
        
    def _checked(self,instance_table,current_row):
        selected_table = Table(current_row[0],current_row[1], [])
        self.id_input.text = str(selected_table.id)
        # seats_list is a list, display its length or a string representation
        self.seats_input.text = str(len(selected_table.seats_list)) if selected_table.seats_list else "0"
        
    def _on_row_press(self,instance,row):
        self.selected_row = int(row.index/len(instance.column_data))
        
    def update_data_table(self,restaurant):
        self.restaurant = restaurant
        
        table_row_data = []
        tables = restaurant.table_list
        for table in tables:
            seats_count = len(table.seats_list) if table.seats_list else 0
            table_row_data.append(
                (table.id,seats_count)
            )
        self.table_table.row_data = table_row_data
            
    def _add_table(self,instance):
        id =  self.id_input.text
        seats = self.seats_input.text
        
        table_data = []
        table_data.append(id)
        table_data.append(seats)
        
        if self._is_data_valid(table_data):
            self.table_manager_controller.add_table(
                self.restaurant,table_data
            )
            self.table_table.row_data.append((id,seats))
            self._is_clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content = Label(text = "Provide mandatory data to add a new Table ID"),
                size_hint = (None,None),
                size =(400,200),
            )
            popup.open()
            
    def _update_table(self,instance):
        if self.selected_row != -1:
            id = self.id_input.text
            seats = self.seats_input.text
            
            table_data = []
            table_data.append(id)
            table_data.append(seats)
            
            if self._is_data_valid(table_data):
                table_to_remove = self.table_table.row_data[self.selected_row]
                del self.table_table.row_data[self.selected_row]
                self.table_manager_controller.delete_table(
                    self.restaurant,table_to_remove
                )
                self.table_manager_controller.add_table(
                    self.restaurant,table_data
                )
                self.table_table.row_data.append([id,seats])
                self._is_clear_input_text_fields()
            else:
                popup = Popup(
                    title = "Invalid data",
                    content = Label(text = "Provide mandatory data to update the Table"),
                    size_hint = (None,None),
                    size = (400,200),
                )
                popup.open()
                
    def _delete_table(self,instance):
        if self.selected_row != -1:
            table_to_remove = self.table_table.row_data[self.selected_row]
            
            del self.table_table.row_data[self.selected_row]
            self.table_manager_controller.delete_table(
                self.restaurant,table_to_remove
            )
            self._is_clear_input_text_fields()
        else:
            popup = Popup(
                title = "Invalid data",
                content = Label(text = "Select any row to delete"),
                size_hint = (None,None),
                size = (400,200)
        )
            popup.open()
            
    def _is_clear_input_text_fields(self):
        self.id_input.text = " "
        self.seats_input.text = " "
        self.selected_row = -1
        
    def _is_data_valid(self,table_data):
        return(
            table_data[0] != " "
            and table_data [1] != " "
        )