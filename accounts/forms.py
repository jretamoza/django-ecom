from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Escriba aquí',
        'class': 'form-control',
    })) # agregamos nuevos campos al formulario desde aca
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme aquí',
        'class': 'form-control',
    }))
    
    
    class Meta: 
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
        
    def __init__(self, *args, **kwargs):  # le damos clase a todos los campos al mismo tiempo
        super(RegistrationForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas ingresadas no coinciden."
            )
            
    def clean_email(self):
        email = self.cleaned_data['email']
        users = Account.objects.filter(email__iexact=email)
        if users:
            raise forms.ValidationError("Ya existe una cuenta con ese email. Intenta otro por favor")
        return email.lower()
    
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ("Solo archivos de imágenes"),}, widget=forms.FileInput)
    
    class Meta: 
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'