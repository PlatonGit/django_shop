from django.contrib import admin
from web.models import *
from django.forms import ModelChoiceField, ModelForm, ValidationError
from PIL import Image


class NotebookAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Minimal picture resolution - {} x {}'.format(*Product.MIN_RESOLUTION)

    
    def clean_image(self):
        image = Image.open(self.cleaned_data['image'])
        
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        
        print('image size -', self.cleaned_data['image'].size)
        if self.cleaned_data['image'].size > Product.MAX_FILE_SIZE:
            raise ValidationError('Image\'s size is bigger than allowed 3 MB!')

        if image.height < min_height or image.width < min_width:
            raise ValidationError('Image\'s resolution is less than allowed!')
        
        if image.height > max_height or image.width > max_width:
            raise ValidationError('Image\'s resolution is larger than allowed!')
        
        return self.cleaned_data['image']


class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'), label='Category')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and not instance.sd:
            self.fields['sd_volume'].widget.attrs.update({
                'readonly': True, 'style': 'display: none;'
            })


    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume'] = None
        return self.cleaned_data



# class SmartphoneAdminForm(ModelForm):
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text = 'Minimal picture resolution - {} x {}'.format(*Product.MIN_RESOLUTION)

    
#     def clean_image(self):
#         image = Image.open(self.cleaned_data['image'])
        
#         min_height, min_width = Product.MIN_RESOLUTION
#         max_height, max_width = Product.MAX_RESOLUTION
        
#         if image.height < min_height or image.width < min_width:
#             raise ValidationError('Image\'s resolution is less than allowed')
        
#         if image.height > max_height or image.width > max_width:
#             raise ValidationError('Image\'s resolution is larger than allowed')
        
#         return self.cleaned_data['image']


class SmartphoneAdmin(admin.ModelAdmin):
    
    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'), label='Category')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartTVAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Minimal picture resolution - {} x {}'.format(*Product.MIN_RESOLUTION)

    
    def clean_image(self):
        image = Image.open(self.cleaned_data['image'])
        
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        
        if image.height < min_height or image.width < min_width:
            raise ValidationError('Image\'s resolution is less than allowed')
        
        if image.height > max_height or image.width > max_width:
            raise ValidationError('Image\'s resolution is larger than allowed')
        
        return self.cleaned_data['image']


class SmartTVAdmin(admin.ModelAdmin):
    form = SmartTVAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smarttvs'), label='Category')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HeadphonesAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Minimal picture resolution - {} x {}'.format(*Product.MIN_RESOLUTION)

    
    def clean_image(self):
        image = Image.open(self.cleaned_data['image'])
        
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        
        if image.height < min_height or image.width < min_width:
            raise ValidationError('Image\'s resolution is less than allowed')
        
        if image.height > max_height or image.width > max_width:
            raise ValidationError('Image\'s resolution is larger than allowed')
        
        return self.cleaned_data['image']


class HeadphonesAdmin(admin.ModelAdmin):
    form = HeadphonesAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='headphones'), label='Category')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(SmartTV, SmartTVAdmin)
admin.site.register(Headphones, HeadphonesAdmin)
