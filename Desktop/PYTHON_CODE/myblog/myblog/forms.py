form django import forms

class ContactForm(forms.Form):
    CITY = [
        ['TP', 'Taipei'],
        ['TY', 'Taoyuang'],
        ['TC', 'Taichung'],
        ['TN', 'Tainan'],
        ['KS', 'Kaohsiung'],
        ['NA', 'Other'],
    ]

    user_name = forms.CharField(label='您的姓名', max_length=50, initial='葉柏漢')
    user_city = forms.ChoiceField(label='居住城市', choices=CITY)
    user_school = forms.BooleanField(label='是否就學', required=False)
    user_email = forms.EmailField(label='電子郵件')
    user_city = forms.CharField(label='您的意見', widget=forms.Textarea)