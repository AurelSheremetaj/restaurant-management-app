class User:
    def __init__ (self,username,password,user_role):
        self.__username = username
        self.__password = password
        self.__user_role = user_role
        
    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self,value):
        self.__username = value
        
    @property
    def passowrd(self):
        return self.__password
    @passowrd.setter
    def password(self,value):
        self.__password = value
        
    @property
    def user_role(self):
        return self.__user_role
    @user_role.setter
    def user_role(self,user_role):
        self.__user_role = user_role

class Restaurant:
    def __init__ (self,id,name,address,menu_list,table_list=None):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__menu_list = menu_list
        self.__table_list = table_list if table_list is not None else []
        
    @property
    def id(self):
       return self.__id
    @id.setter
    def id(self,value):
       self.__id = value
   
    @property
    def name(self):
        return self.__name
    @name.setter 
    def name(self,value):
        self.__name = value
        
    @property 
    def address(self):
        return self.__address
    @address.setter
    def address(self,value):
        self.__address = value
        
    @property
    def menu_list(self):
        return self.__menu_list
    @menu_list.setter
    def  menu_list(self,value):
        self.__menu_list = value

    @property
    def table_list(self):
        return self.__table_list
    @table_list.setter
    def table_list(self, value):
        self.__table_list = value
        

        
class Menu:
    def __init__(self, name,menu_id,menu_item_list):
        self.__name = name
        self.__menu_id = menu_id
        self.__menu_item_list = menu_item_list
        
    @property
    def name(self):
        return self.__name
    @name.setter
    def name (self,value):
        self.__name = value
        
    @property
    def menu_id(self):
        return self.__menu_id
    @menu_id.setter
    def menu_id(self,value):
        self.__menu_id = value
        
    @property 
    def menu_item_list(self):
        return self.__menu_item_list
    
    @menu_item_list.setter
    def menu_item_list(self,value) :
        self.__menu_item_list = value
        
        
class Menu_Item:
    def __init__(self, id,name,price,description,priority):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__priority = priority
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value):
        self._id = value
    
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,value):
        self.__name = value
        
    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self,value):
        self.__price = value
        
    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self,value):
        self.__description = value
    
    @property
    def priority(self):
        return self.__priority
    @priority.setter
    def priority(self,value):
        self.__priority = value
        
class Table: 
    def __init__(self,id,name,seats_list):
        self.__name = name
        self.__id = id
        self.__seats_list = seats_list
        
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,value):
        self.__name = value
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value):
        self.__id = value
        
    @property
    def seats_list(self):
        return self.__seats_list
    @seats_list.setter
    def seats_list(self,value):
        self.__seats_list = value
        
class Seats:
    def __init__(self,id,quantity):
        self.__id = id
        self.__quantity = quantity
        
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value):
        self.__id = value
        
        
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self,value):
        self.__quantity = value
    
    