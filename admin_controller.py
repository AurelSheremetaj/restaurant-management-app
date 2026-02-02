from model import Restaurant,Menu,Menu_Item,Table
from data_provider1 import DataProvider
import random
from database_controller import RestaurantDatabaseMAnager

class RestaurantManagerController:
    def __init__(self):
        # Initialize the database manager with your database credentials
        self.db_manager = RestaurantDatabaseMAnager(
            database_name="restaurant-app",
            user="postgres",
            password="2003",
            host="localhost",
            port=2022
        )
    
    def add_restaurant(self, restaurant_list, restaurant_data):
        # Add restaurant to database
        if len(restaurant_data) > 1:
            self.db_manager.add_restaurant(restaurant_data[0], restaurant_data[1])
        else:
            self.db_manager.add_restaurant(restaurant_data[0])
        # Refresh restaurant list from database
        restaurant_list.clear()
        restaurant_list.extend(self.db_manager.get_restaurant_list())
        # Return the newly added restaurant object
        for r in restaurant_list:
            if r.name == restaurant_data[0]:
                return r
        return None
    
    def delete_restaurant(self, restaurant_list, restaurant_data):
        restaurant_to_delete = None
        for restaurant in restaurant_list:
            if restaurant.name == restaurant_data[0]:
                restaurant_to_delete = restaurant
                break
        if restaurant_to_delete:
            self.db_manager.delete_restaurant(restaurant_to_delete.id)
            # Refresh restaurant list from database
            restaurant_list.clear()
            restaurant_list.extend(self.db_manager.get_restaurant_list())

    def update_restaurant(self, restaurant_list, restaurant_id, updated_restaurant_data):
        self.db_manager.update_restaurant(restaurant_id, updated_restaurant_data[0], updated_restaurant_data[1])
        # Refresh restaurant list from database
        restaurant_list.clear()
        restaurant_list.extend(self.db_manager.get_restaurant_list())
    
    #def update_restaurant(self, old_restaurant_data, new_restaurant_data,restaurant):
     #   self.delete_restaurant(restaurant,old_restaurant_data,new_restaurant_data)
      #  self.add_restaurant(restaurant,new_restaurant_data)        
  

from database_controller import MenuDatabaseManager, MenuItemDatabaseManager, TableDatabaseManager

class MenuItemManagerController:
    def __init__(self, connection):
        self.db_manager = MenuItemDatabaseManager(connection)

    def add_menuitem(self, menu, menu_item_data):
        # Add menu item to database
        self.db_manager.add_menu_item(
            menu_item_data[1],  # name
            menu_item_data[2],  # price
            menu_item_data[3],  # description
            menu_item_data[4],  # priority
            menu.menu_id       # menu_id
        )
        # Refresh menu item list from database
        menu.menu_item_list = self.db_manager.get_menu_items_by_menu(menu.menu_id)

    def delete_menuitem(self, menu, menu_item_name):
        menu_item_to_delete = None
        for menu_item in menu.menu_item_list:
            if menu_item.name == menu_item_name:
                menu_item_to_delete = menu_item
                break
        if menu_item_to_delete:
            self.db_manager.delete_menu_item(menu_item_to_delete.id)
            # Refresh menu item list from database
            menu.menu_item_list = self.db_manager.get_menu_items_by_menu(menu.menu_id)

    def update_menuitem(self, old_menu_item_name, new_menu_item_data, menu):
        menu_item_to_update = None
        for menu_item in menu.menu_item_list:
            if menu_item.name == old_menu_item_name:
                menu_item_to_update = menu_item
                break
        if menu_item_to_update:
            self.db_manager.update_menu_item(
                menu_item_to_update.id,
                new_menu_item_data[0],
                new_menu_item_data[1],
                new_menu_item_data[2],
                new_menu_item_data[3]
            )
            # Refresh menu item list from database
            menu.menu_item_list = self.db_manager.get_menu_items_by_menu(menu.menu_id)

class MenuManagerController:
    def __init__(self, connection):
        self.db_manager = MenuDatabaseManager(connection)

    def add_menu(self, restaurant, menu_data):
        # Add menu to database
        self.db_manager.add_menu(menu_data[0], restaurant.id)
        # Refresh menu list from database
        restaurant.menu_list = self.db_manager.get_menus_by_restaurant(restaurant.id)

    def delete_menu(self, restaurant, menu_data):
        menu_to_delete = None
        for menu in restaurant.menu_list:
            if menu.name == menu_data[0]:
                menu_to_delete = menu
                break
        if menu_to_delete:
            self.db_manager.delete_menu(menu_to_delete.menu_id)
            # Refresh menu list from database
            restaurant.menu_list = self.db_manager.get_menus_by_restaurant(restaurant.id)

    def update_menu(self, old_menu_data, new_menu_data, restaurant):
        menu_to_update = None
        for menu in restaurant.menu_list:
            if menu.name == old_menu_data[0]:
                menu_to_update = menu
                break
        if menu_to_update:
            self.db_manager.update_menu(menu_to_update.menu_id, new_menu_data[0])
            # Refresh menu list from database
            restaurant.menu_list = self.db_manager.get_menus_by_restaurant(restaurant.id)

class TableManagerController:
    def __init__(self, connection):
        self.db_manager = TableDatabaseManager(connection)

    def add_table(self, restaurant, table_data):
        # Add table to database
        seats = table_data[1]
        try:
            seats = int(seats)
        except ValueError:
            seats = 0
        self.db_manager.add_table(seats, restaurant.id)
        # Refresh table list from database
        restaurant.table_list = self.db_manager.get_tables_by_restaurant(restaurant.id)

    def delete_table(self, restaurant, table_data):
        table_to_delete = None
        for table in restaurant.table_list:
            if table.id == table_data[0]:
                table_to_delete = table
                break
        if table_to_delete:
            self.db_manager.delete_table(table_to_delete.id)
            # Refresh table list from database
            restaurant.table_list = self.db_manager.get_tables_by_restaurant(restaurant.id)

    def update_table(self, old_table_data, new_table_data, restaurant):
        table_to_update = None
        for table in restaurant.table_list:
            if table.id == old_table_data[0]:
                table_to_update = table
                break
        if table_to_update:
            self.db_manager.update_table(table_to_update.id, new_table_data[1])
            # Refresh table list from database
            restaurant.table_list = self.db_manager.get_tables_by_restaurant(restaurant.id)
