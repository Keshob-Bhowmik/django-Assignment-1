from django import forms
from event.models import Event, Participant, Category
class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'border border-gray-300 rounded-md px-3 py-2 w-full text-sm focus:outline-none focus:ring-2 focus:ring-rose-600',
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'w-full border border-gray-300 rounded-md px-3 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-rose-600',
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border border-gray-300 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-rose-600',
                'placeholder': 'yyyy-mm-dd',
            }),
            'time' : forms.TimeInput(attrs={
                'type' : 'time',
                'class' : 'border border-gray-300 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-rose-600',
            }),
            'category' : forms.Select(attrs={
                'class' : 'border border-gray-300 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-rose-600',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(EventModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None


class CreateCategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'border border-gray-300 rounded-md px-3 py-2 w-full text-sm focus:outline-none focus:ring-2 focus:ring-rose-600',
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'w-full border border-gray-300 rounded-md px-3 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-rose-600',
            })
        }

    def __init__(self, *args, **kwargs):
        super(CreateCategoryModelForm, self).__init__(*args, **kwargs)


class AddParticepantModelform(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'border border-gray-300 rounded-md px-3 py-2 w-full text-sm focus:outline-none focus:ring-2 focus:ring-rose-600',
            }),
            'email' : forms.EmailInput(attrs={
                'class' : 'border border-gray-300 rounded-md px-3 py-2 w-full text-sm focus:outline-none focus:ring-2 focus:ring-rose-600'
            }),
            'events' : forms.CheckboxSelectMultiple(attrs={
                
            })
        }

    def __init__(self, *args, **kwargs):
        super(AddParticepantModelform, self).__init__(*args, **kwargs)