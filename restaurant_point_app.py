from data_provider1 import DataProvider

class RestaurantPointAPP:
    def start(self):
        self.restaurant_list = []
        self.data_provider = DataProvider()
        self.restaurant_list = self.data_provider.restaurant_list
        
        
        
        for restaurant in self.restaurant_list:
            print("----------------------------------------")
            print("List of menus in" + " " + restaurant.name + " in " + restaurant.address)
            print("======================================")
            
            for menu in restaurant.menu_list:
                print(menu.name + "," + " ID:" + menu.menu_id )
                print("----------------------------------------------")
                
                for menu_item in menu.menu_item_list:
                    print( menu_item.id + "," + menu_item.name + "," + menu_item.price + "," + menu_item.description + "," +menu_item.priority.value)
                    print("-----------------------------------------------------------------")
                    

               
                
restaurant_point_app = RestaurantPointAPP()
restaurant_point_app.start()