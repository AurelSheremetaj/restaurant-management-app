
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from login_controller import LoginController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import sys
from utils import UserFeatureContentPanelResolver,UserFeatureLabelResolver

from utils import AuthorizationService,UserFeatureContentPanelResolver,UserFeatureLabelResolver

class TwoPanelLayoutApp(MDApp):
    def build(self):
        Window.size = (900,500)
        screen = Screen()
        screen.add_widget(self._create_split_layout_panel())
        return screen
    
    from kivy.uix.boxlayout import BoxLayout

    def _create_split_layout_panel(self):
        self.split_layout_panel = BoxLayout(orientation='horizontal')
        #self.split_layout_panel = GridLayout(spacing = 2)
        self.split_layout_panel.size_hint_x = 1
        self.split_layout_panel.size_hint_y = 1
        self.split_layout_panel.add_widget(self._create_navigation_bar_panel())
        self.split_layout_panel.add_widget(self._create_content_panel())
        return self.split_layout_panel
    
    
    def _create_navigation_bar_components(self):
        self.button_list = []
         
        user_role = LoginController.get_logged_in_user().user_role
        authorization_service = AuthorizationService()
        self.user_features = authorization_service.get_user_feature_by_user_role(user_role)
        
        for feature in self.user_features:
            button  = Button(text = UserFeatureLabelResolver.get_user_feature_label(feature),background_color =(0,1,1,1),
                            color = (1,1,1,1),
                            font_size = 18,
                            size_hint = (1,None))
            button.size = (300,60)
            self.button_list.append(button)
            
        return self.button_list
    
    
    
    def _create_navigation_bar_panel(self):
        navigation_bar_panel = GridLayout(cols = 1, spacing = 20)
        navigation_bar_panel.size_hint_x = None
        navigation_bar_panel.width = 300
        button_list = self._create_navigation_bar_components()
        for button in button_list:
            if button.text != "Sign out":
                button.bind(on_press = self._change_content_panel_label)
            else:
                button.bind(on_press = self._sign_out)
            navigation_bar_panel.add_widget(button)
        return navigation_bar_panel
        
    def _create_content_panel(self):
        self.content_panel = GridLayout(cols=1,spacing = 20)
        self.content_panel.size_hint_x = 1
        self.content_panel.size_hint_y = 1
        self.content_panel_content = Label(
            text = "WELCOME",color = (65,189,173)
        )
        self.content_panel.add_widget(self.content_panel_content)
        return self.content_panel
        
    def _change_content_panel_label(self,instance):
        # Instead of clearing all widgets, update only the content panel
        # Remove old content panel widget
        if hasattr(self, 'content_panel') and self.content_panel in self.split_layout_panel.children:
            self.split_layout_panel.remove_widget(self.content_panel)
        
        user_feature_panel_creator = (
            UserFeatureContentPanelResolver.get_user_feature_panel(instance.text)
        )
        if user_feature_panel_creator is None:
            popup = Popup(
                title="Feature Not Found",
                content=Label(text=f"No panel found for feature: {instance.text}"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()
            return
        
        self.content_panel = user_feature_panel_creator.create_content_panel()
        
        self.split_layout_panel.add_widget(self.content_panel)
        for button in self.button_list:
            if button.text == instance.text:
                button.background_color = (0.9, 0.5, 0.5, 1)
            else:
                button.background_color = (0,0,1,1)
            
        
        
    def _sign_out(self,instance):
        sys.exit(0)        

class LoginAP(MDApp):
    username_input = None
    password_input = None   
    
    def build(self):
        Window.size  = (500,600)
        screen_manager = ScreenManager()
        screen = Screen()
        self.screen = screen
        screen.add_widget(self._create_login_components())
        self.screen_manager = screen_manager
        screen_manager.add_widget(screen)
        
        return screen_manager
    
    def _create_login_components(self):
        layout = GridLayout(cols = 1,padding = 150,spacing = 30)
        
        login_label = MDLabel(text = "LOGIN FORM",font_size  ="50sp",halign = "center")
        layout.add_widget(login_label)
        
        self._create_username_components()
        layout.add_widget(self.username_input)
        
        self._create_password_components()
        layout.add_widget(self.password_input)
        
        
        view_password_button = MDIconButton(
            icon = "eye-off",on_release=self.toggle_password_visibility
        )
        
        layout.add_widget(view_password_button)
        
        login_button = self._create_button_component()
        layout.add_widget(login_button)
        
        return layout
        
        
    def _create_username_components(self):
        self.username_input = MDTextField(hint_text = "Username")
        
    def _create_password_components(self):
        self.password_input = MDTextField(password = True,hint_text = "Password")
        self.password_input.bind(
            on_text_validate = self.login_with_provided_user_credentials
        )
        
        
    def toggle_password_visibility(self,instance):
        if self.password_input.password:
            self.password_input.password = False
            instance.icon = "eye"
            
        else:
            self.password_input.password = True
            instance.icon = "eye-off"
            
    def _create_button_component(self):
        login_button = Button(
            text = "Login",
            size_hint = (None,None),
            size=(100,50),
            background_color = (0,0.7,0.9,1)
        )
        
        login_button.bind(on_press = self.login_with_provided_user_credentials)
        return login_button
    
    def login_with_provided_user_credentials(self,instance):
        username = self.username_input.text
        password = self.password_input.text
        
        if self._is_credentials_provided(username,password):
            LoginController.login_user(username,password)
            user = LoginController.get_logged_in_user()
            if user is None:
                popup = Popup(
                    title = "Login Failed",
                    content = Label(text="Invalid username or password."),
                    size_hint = (None,None),
                    size = (400,200),
                )
                
                self.username_input.text = ""
                self.password_input.text = ""
                popup.open()
            else:
                two_panel_layout_screen = TwoPanelLayoutApp().build()
                self.screen_manager.remove_widget(self.screen)
                self.screen_manager.add_widget(two_panel_layout_screen)
                
                                
    def _is_credentials_provided(self,username,password):
        if LoginController.is_string_none_or_blank(username):
            popup = Popup(title = 'Credentials missing',content = Label(text='Please provide your username.'),
                        size_hint = (None,None),size = (400,200))
            popup.open()
            return False
        elif LoginController.is_string_none_or_blank(password):
            popup = Popup(title = 'Credentials missing',content = Label(text='Please provide your password.'),
                    size_hint = (None,None),size = (400,200))
            popup.open()
            return False
        return True         
        
        
LoginAP().run()
    
    