from enum1 import UserRole,UserFeatures
from admin_view import MenuItemManagerContentPanel,MenuManagerContentPanel,TableManagerContentPanel,RestaurantManagerContentPanel
from datetime import datetime
from cook_view import OrderStatusContentpanel
from waiter_view import TableOrderContentPanel
class AuthorizationService:
    def get_user_feature_by_user_role(self,user_role):
        if user_role == UserRole.ADMIN:
            return [UserFeatures.RESTAURANT_MANAGER,
                UserFeatures.MENU_MANAGER,
                UserFeatures.MENU_ITEM_MANAGER,
                UserFeatures.TABLE_MANAGER,
                UserFeatures.SIGN_OUT]
            
        elif user_role == UserRole.WAITER:
            return [ UserFeatures.TABLE_ORDER,
                    UserFeatures.ORDER_STATUS,
                    UserFeatures.SIGN_OUT]
            
        elif user_role == UserRole.COOK:
            return [UserFeatures.ORDER_STATUS,
                    UserFeatures.SIGN_OUT]
            
        elif user_role is None:
            raise RuntimeError("The provided user role " + user_role + "is not supported")
        
        
class UserFeatureLabelResolver:
    user_feature_label_dict = None
    
    @staticmethod
    def get_user_feature_label(user_feature):
        return UserFeatureLabelResolver.__get_user_feature_label_dict().get(user_feature)
    
    
    @staticmethod
    def __get_user_feature_label_dict():
        if UserFeatureLabelResolver.user_feature_label_dict is None:
            UserFeatureLabelResolver.user_feature_label_dict = {
                UserFeatures.RESTAURANT_MANAGER: "Restaurant manager",
                UserFeatures.MENU_MANAGER: "Menu manager",
                UserFeatures.MENU_ITEM_MANAGER: "Menu item manager",
                UserFeatures.TABLE_MANAGER: "Table manager",
                UserFeatures.TABLE_ORDER: "Table order",
                UserFeatures.ORDER_STATUS: "Order status",
                UserFeatures.SIGN_OUT: "Sign out"

            }
        return UserFeatureLabelResolver.user_feature_label_dict
    
class UserFeatureContentPanelResolver:
    
    user_feauture_content_panel_map = None
    
    @staticmethod
    def get_user_feature_panel(user_feature):
        return UserFeatureContentPanelResolver.get_user_feature_content_panel_map().get(user_feature)
    
    @staticmethod
    def get_user_feature_content_panel_map():
        if UserFeatureContentPanelResolver.user_feauture_content_panel_map is None:
            UserFeatureContentPanelResolver.user_feauture_content_panel_map = {
                "Restaurant manager": RestaurantManagerContentPanel(),
                "Menu item manager": MenuItemManagerContentPanel(),
                "Menu manager": MenuManagerContentPanel(),
                "Table manager": TableManagerContentPanel(),
                "Order status" : OrderStatusContentpanel(order_list=[]),
                "Table order": TableOrderContentPanel(),
                    
            } 
            
        return UserFeatureContentPanelResolver.user_feauture_content_panel_map
    
    