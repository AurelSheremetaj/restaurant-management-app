from model import Restaurant,Menu,Menu_Item,Table,Seats,User
from enum1 import Priority,UserRole,UserFeatures
from generator import UniqueIDGenerator
import random

class UserDataProvider:
    def __init__ (self):
        self.__user_list =[]
        self._create_user_list()
        
    def _create_user_list(self):
        user1 = User("1","1",UserRole.ADMIN)
        user2 = User("2","2",UserRole.COOK)
        user3 = User("3","3",UserRole.COOK)
        user4 = User("4","4",UserRole.WAITER)
        self.__user_list.append(user1)
        self.__user_list.append(user2)
        self.__user_list.append(user3)
        self.__user_list.append(user4)
        
        
    
    @property
    def user__list(self):
        return self.__user_list
    
    
class DataProvider:
    def __init__ (self):
        self.__restaurants = []
        self._create_restaurant_lists()
        
    def _create_restaurant_lists(self):
        
        unique_id1 = random.randint(1,100)
        unique_id1 = UniqueIDGenerator.generate_id()
        restaurant1_menu_list = self._create_restaurant1_menu()
        restaurant1 = Restaurant(unique_id1,"Restaurant 1","Rruga 1",restaurant1_menu_list)
        
        unique_id2 = random.randint(1,100)
        unique_id2 = UniqueIDGenerator.generate_id()
        restaurant2_menu_list = self._create_restaurant2_menu()
        restaurant2 = Restaurant(unique_id2,"Restaurant 2 ","Rruga 2",restaurant2_menu_list)
        
        unique_id3 = random.randint(1,100)
        unique_id3 = UniqueIDGenerator.generate_id()
        restaurant3_menu_list = self._create_restaurant3_menu()
        restaurant3 = Restaurant(unique_id3,"Restaurant 3","Rruga 3",restaurant3_menu_list)
        
        
        self.__restaurants.append(restaurant1)
        self.__restaurants.append(restaurant2)
        self.__restaurants.append(restaurant3)
        
    
  
    
    
    def _create_restaurant1_menu(self):
        menu_list = []
        menu_list.append(Menu("goodies","01",self.menu_item_list_for_menu1()))
        menu_list.append(Menu("meat","02",self.menu_item_list_for_menu2()))
        menu_list.append(Menu("seafood","03",self.menu_item_list_for_menu3()))
        return menu_list
    
    def _create_restaurant2_menu(self):
        menu1 = Menu("goodies","04",self.menu_item_list_for_menu1())
        menu2 = Menu("meat","05",self.menu_item_list_for_menu2())
        menu3 = Menu("seafood","06",self.menu_item_list_for_menu3())
        
        menu_list = [menu1,menu2,menu3]
        return menu_list
    
    def _create_restaurant3_menu(self):
        menu1 = Menu("goodies","07",self.menu_item_list_for_menu1())
        menu2 = Menu("meat","08",self.menu_item_list_for_menu2())
        menu3 = Menu("seafood","09",self.menu_item_list_for_menu3())
        
        menu_list = [menu1,menu2,menu3]
        return menu_list
    
    def menu_item_list_for_menu1(self):
        menu_item = [
            Menu_Item("1","pizza","12$","margarita pizza",Priority.EXPENSIVE),
            Menu_Item("2","hamburger","6$","chicken hamburger",Priority.NORMAL),
            Menu_Item("3","pasta","4$","white pasta",Priority.CHEAP)
        ]
        return menu_item
        
    def menu_item_list_for_menu2(self):
        menu_item = [
            Menu_Item("4","steak","30$","medium rare",Priority.EXPENSIVE),
            Menu_Item("5","osso buco","20$","no onions",Priority.NORMAL),
            Menu_Item("3","chicken breast","10$","baked",Priority.CHEAP)
        ]
        return menu_item
        
    def menu_item_list_for_menu3(self):
        menu_item = [
            Menu_Item("7","shrimp","15$","grilled",Priority.EXPENSIVE),
            Menu_Item("8","salmon","10$","smoked",Priority.NORMAL),
            Menu_Item("9","octopus","7$","fried",Priority.CHEAP)
        ]
        return menu_item
        
    @property
    def restaurant_list(self):
        return self.__restaurants
        
  