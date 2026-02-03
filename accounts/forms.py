from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from .models import Account,UserProfile

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder':'confirm password',
        }),
        label="Confirm Password"
    )

    class Meta:
        model = Account
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'phone_number',
            'password',
            'confirm_password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                    
        self.fields['first_name'].widget.attrs['placeholder']='Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last name'
        self.fields['email'].widget.attrs['placeholder']='Enter email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone number'
        self.fields['username'].widget.attrs['placeholder']='Enter username'
        self.fields['password'].widget=forms.PasswordInput(attrs={
            'placeholder':'Enter Password',
        })
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('phone_number', css_class='col-md-6'),
                Column('username', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('password', css_class='col-md-6'),
                Column('confirm_password', css_class='col-md-6'),
            ),
        )
    
    def clean(self):
        cleaned_data =super(RegisterForm,self).clean()
        
        password=cleaned_data['password']
        confirm_password=cleaned_data['confirm_password']
        
        if password!=confirm_password:
            raise forms.ValidationError('Passwords do not match')
        

class userForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('first_name','last_name','phone_number',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control' 
class userProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'Invalid':("Image fields only",)},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=('profile_picture','address_line_1','address_line_2','city','state','country')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            