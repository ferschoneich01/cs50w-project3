from django import forms
from .models import Item, Meal, Meal_Type, Size, Meal_Addition, Price

class OrderForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('meal', 'meal_type', 'size', 'meal_addition')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # establecer menús desplegables como vacíos hasta que se seleccione una comida del primer menú desplegable 
        self.fields['meal_type'].queryset = Meal_Type.objects.none()
        self.fields['size'].queryset = Size.objects.none()
        self.fields['meal_addition'].queryset = Meal_Addition.objects.none()

        # si se ha seleccionado una comida del menú desplegable
        if 'meal' in self.data:
            try:
                meal_id = int(self.data.get('meal'))
                self.fields['meal_type'].queryset = Meal_Type.objects.filter(meal_id=meal_id).order_by('meal')
            except (ValueError, TypeError):
                pass 
        
        # si se ha seleccionado un typo de comida del menú desplegable 
        if 'meal_type' in self.data:
            try:
                meal_type = int(self.data.get('meal_type'))
                self.fields['size'].queryset = Size.objects.filter(meal_type=meal_type).order_by('size')
                self.fields['meal_addition'].queryset = Meal_Addition.objects.filter(meal_type=meal_type).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['size'].queryset = self.instance.meal_type.size_set.order_by('size')
            self.fields['meal_addition'].queryset = self.instance.meal_type.meal_addition_set.order_by('name')

    # validar los ingredientes y obtener el total del precio de la orden
    def clean_meal_addition(self):
        meal_addition = self.cleaned_data['meal_addition']
        meal_type = self.cleaned_data['meal_type']
        size = self.cleaned_data['size']
        meal = str(self.cleaned_data['meal'])

        # si es seleccionada pizza debe escoger los ingredientes
        if 'Pizza' in meal:
            if '1 ingrediente' in str(meal_type):
                if len(meal_addition) != 1:
                    raise forms.ValidationError('Debes seleccionar 1 ingrediente')
            if '2 ingredientes' in str(meal_type):
                if len(meal_addition) != 2:
                    raise forms.ValidationError('Debes seleccionar 2 ingrediente')
            if '3 ingredientes' in str(meal_type):
                if len(meal_addition) != 3:
                    raise forms.ValidationError('Debes seleccionar 3 ingrediente')

        # obtenga el precio para el tipo de comida seleccionado
        meal_price = Price.objects.filter(meal_type=meal_type, size=size)
        total_price = float()
        for item in meal_price:
            total_price = float(item.price)
        
        # si el tipo de comida es un sub, agregue el costo de cualquier adición al precio total
        if 'Sub' in meal:
            for item in meal_addition:
                total_price = total_price + float(item.price)
                
        return meal_addition
