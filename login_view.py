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
                popup = Popup(title = 'Login successful',content = Label(text = "'You have logged in"),
                              size_hint = (None,None),size = (400,200))
                popup.open()
                
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
    
    