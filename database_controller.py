import psycopg2
from model import Restaurant, Menu, Menu_Item, Table

class RestaurantDatabaseMAnager:
    def __init__(self,database_name,user,password,host,port):
        self.connection = psycopg2.connect(
            dbname=database_name,
            user = user,
            password = password,
            host = host,
            port = port
        )
        
        print("Database created successfully")
        
        self.cursor = self.connection.cursor()
        self.create_restaurant_database_table()
        
        self.add_restaurants()
        
    def create_restaurant_database_table(self):
        # Create restaurants table with address column if not exists
        query = """
        CREATE TABLE IF NOT EXISTS restaurants (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(20),
            address VARCHAR(100)
        )
        """
        self.execute_query(query)
        # Check if address column exists, if not add it
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='restaurants' AND column_name='address'")
        if not self.cursor.fetchone():
            alter_query = "ALTER TABLE restaurants ADD COLUMN address VARCHAR(100)"
            self.execute_query(alter_query)
        
        
    def add_restaurants(self):
        restaurant_list = [ "Restaurant 1" , "Restaurant 2 ", "Restaurant 3"]
        for restaurant in restaurant_list:
            self.add_restaurant(restaurant)
            
    def add_restaurant(self, restaurant_name, address=None):
        select_restaurant_query = (f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'")
        self.cursor.execute(select_restaurant_query)
        restaurant_result = self.cursor.fetchone()
        
        if restaurant_result:
            print("Restaurant already exists")
            
        else:
            if address:
                query = f"INSERT INTO restaurants (name, address) VALUES ('{restaurant_name}', '{address}')"
            else:
                query = f"INSERT INTO restaurants (name) VALUES ('{restaurant_name}')"
            self.execute_query(query)
            print("Restaurant created successfully")
        
        
    def get_restaurant_list(self):
        select_restaurant_query = "SELECT id, name, address FROM restaurants"
        self.cursor.execute(select_restaurant_query)
        restaurant_results = self.cursor.fetchall()
        restaurant_list = []
        menu_db_manager = MenuDatabaseManager(self.connection)
        for restaurant in restaurant_results:
            menu_list = menu_db_manager.get_menus_by_restaurant(restaurant[0])
            restaurant_list.append(Restaurant(restaurant[0], restaurant[1], restaurant[2], menu_list))
        return restaurant_list
        
        
    def execute_query(self,query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def delete_restaurant(self, restaurant_id):
        query = "DELETE FROM restaurants WHERE id = %s"
        self.execute_query(query, (restaurant_id,))
        print(f"Restaurant with id {restaurant_id} deleted successfully")

    def update_restaurant(self, restaurant_id, new_name, new_address):
        query = "UPDATE restaurants SET name = %s, address = %s WHERE id = %s"
        self.execute_query(query, (new_name, new_address, restaurant_id))
        print(f"Restaurant with id {restaurant_id} updated successfully")

class MenuDatabaseManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.create_menu_table()

    def create_menu_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS menus (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(50),
            restaurant_id UUID REFERENCES restaurants(id)
        )
        """
        self.execute_query(query)

    def add_menu(self, name, restaurant_id):
        query = "INSERT INTO menus (name, restaurant_id) VALUES (%s, %s)"
        self.execute_query(query, (name, restaurant_id))

    def get_menus_by_restaurant(self, restaurant_id):
        query = "SELECT id, name FROM menus WHERE restaurant_id = %s"
        self.cursor.execute(query, (restaurant_id,))
        results = self.cursor.fetchall()
        menus = []
        for row in results:
            # Swap arguments to match Menu constructor (name, menu_id, menu_item_list)
            menus.append(Menu(row[1], row[0], []))
        return menus

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def delete_menu(self, menu_id):
        query = "DELETE FROM menus WHERE id = %s"
        self.execute_query(query, (menu_id,))
        print(f"Menu with id {menu_id} deleted successfully")

    def update_menu(self, menu_id, new_name):
        query = "UPDATE menus SET name = %s WHERE id = %s"
        self.execute_query(query, (new_name, menu_id))
        print(f"Menu with id {menu_id} updated successfully")

class MenuItemDatabaseManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.create_menu_item_table()

    def create_menu_item_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS menu_items (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(50),
            price NUMERIC,
            description TEXT,
            priority VARCHAR(20),
            menu_id UUID REFERENCES menus(id)
        )
        """
        self.execute_query(query)

    def add_menu_item(self, name, price, description, priority, menu_id):
        query = """
        INSERT INTO menu_items (name, price, description, priority, menu_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_query(query, (name, price, description, priority, menu_id))

    def get_menu_items_by_menu(self, menu_id):
        query = "SELECT id, name, price, description, priority FROM menu_items WHERE menu_id = %s"
        self.cursor.execute(query, (menu_id,))
        results = self.cursor.fetchall()
        menu_items = []
        for row in results:
            menu_items.append(Menu_Item(row[0], row[1], row[2], row[3], row[4]))
        return menu_items

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def delete_menu_item(self, menu_item_id):
        query = "DELETE FROM menu_items WHERE id = %s"
        self.execute_query(query, (menu_item_id,))
        print(f"Menu item with id {menu_item_id} deleted successfully")

    def update_menu_item(self, menu_item_id, new_name, new_description, new_price, new_priority):
        query = """
        UPDATE menu_items
        SET name = %s, description = %s, price = %s, priority = %s
        WHERE id = %s
        """
        self.execute_query(query, (new_name, new_description, new_price, new_priority, menu_item_id))
        print(f"Menu item with id {menu_item_id} updated successfully")

class TableDatabaseManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.create_table_table()

    def create_table_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tables (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            seats INTEGER,
            restaurant_id UUID REFERENCES restaurants(id)
        )
        """
        self.execute_query(query)

    def add_table(self, seats, restaurant_id):
        query = f"INSERT INTO tables (seats, restaurant_id) VALUES ({seats}, '{restaurant_id}')"
        self.execute_query(query)

    def get_tables_by_restaurant(self, restaurant_id):
        query = f"SELECT id, seats FROM tables WHERE restaurant_id = '{restaurant_id}'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        tables = []
        for row in results:
            tables.append(Table(row[0], row[1], []))
        return tables

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def delete_table(self, table_id):
        query = "DELETE FROM tables WHERE id = %s"
        self.execute_query(query, (table_id,))
        print(f"Table with id {table_id} deleted successfully")

    def update_table(self, table_id, new_seats):
        query = "UPDATE tables SET seats = %s WHERE id = %s"
        self.execute_query(query, (new_seats, table_id))
        print(f"Table with id {table_id} updated successfully")
        
        