from django import forms
from event.models import Event, Participant, Category

class StyledForMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyed_style_widgets()
    default_classes ="w-full  border-2"

    def applyed_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "border-blue-500  border-2 bg-blue-100",
                    'placeholder' : f"enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : "border-blue-500  border-2 bg-blue-100",
                    'placeholder' : f"enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class' : "border-2",
                    'placeholder' : f"enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class' : "border-2 w-full",
                    
                })
            elif isinstance(field.widget, forms.PasswordInput):
                placeholder_text = "Enter your password"
                if field_name.lower() == "confirm_password":
                    placeholder_text = "Retype your password"
                field.widget.attrs.update({
                    'class': "border-2 w-full",
                    'placeholder': placeholder_text
                })

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
        super().__init__(*args, **kwargs)


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
        super().__init__(*args, **kwargs)


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
        super().__init__(*args, **kwargs)