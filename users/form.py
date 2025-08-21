# from django import forms
# from .models import CustomUser, Department

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     department = forms.ModelChoiceField(
#         queryset=Department.objects.all(),
#         empty_label="Select Department",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'user_type', 'phone_number', 'department', 'password']
#         widgets = {
#             'user_type': forms.Select(attrs={'class': 'form-control'}),
#             'phone_number': forms.TextInput(attrs={'placeholder': 'e.g. +237xxxxxxxx'}),
#         }

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])  # Encrypt password
#         if commit:
#             user.save()
#         return user
