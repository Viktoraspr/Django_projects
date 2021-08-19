from django import forms


class CreateCustomer(forms.Form):
    company_code = forms.IntegerField(label='Company code:')
    customer = forms.CharField(label='Customer', max_length=200)
    representative = forms.CharField(label='Name/Surname', max_length=200)
    adress = forms.CharField(label='Address', max_length=200)
    country = forms.CharField(label='Coutry', max_length=200)
    email = forms.EmailField(label='Email')


types_of_scaff = ['Standart', 'Hanging', 'Mobile']


class CreateOrder(forms.Form):
    scaffolding_number = forms.CharField(required=False,
                                         label='Scaffolding number:',
                                         max_length=50)
    project_number = forms.IntegerField(label='Project No.', required=False)
    order_number = forms.CharField(label='Order Number', required=False)
    altitude = forms.CharField(label='Altitude', max_length=20, required=False)
    type_of_scaffoldin = forms.CharField(label='Type of scaffolding')
