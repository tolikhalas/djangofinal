from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "Ім'я користувача")
    password = forms.CharField(label = "Пароль",widget = forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 50,label = "Ім'я користувача")
    password = forms.CharField(max_length=20,label = "Пароль",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label ="Повторіть пароль",widget = forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Паролі не збігаються")

        values = {
            "username" : username,
            "password" : password
        }
        return values


