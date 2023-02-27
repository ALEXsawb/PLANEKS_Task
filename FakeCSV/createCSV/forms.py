from django import forms

TYPES = [('full name', 'Full name'),
         ('company', 'Company'),
         ('job', 'Job'),
         ('email', 'Email'),
         ('date', 'Date')]

COLUMN_SEPARATIONS = [(';', '(;)'), (',', '(,)'), ('\t', '(\t)'), (' ', '( )'), ('|', '(|)')]
HOLD_SEPARATION = (('"', '(")'), (';', '(;)'), ('|', '(|)'))


class CreateSchemas(forms.Form):
    name = forms.CharField(label='Name')
    delimiter = forms.ChoiceField(choices=COLUMN_SEPARATIONS)
    quotechar = forms.ChoiceField(choices=HOLD_SEPARATION)


class EmptySchemaColumn(forms.Form):
    column_name = forms.CharField(label='Column name')
    column_type = forms.ChoiceField(choices=TYPES)
    order = forms.IntegerField(label='Order', widget=forms.TextInput(attrs={'min': 0, 'type': 'number',
                                                                            'style': 'width: 150px;'}))
