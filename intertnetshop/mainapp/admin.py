from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import *
from django import forms
from django.forms import ModelChoiceField, ModelForm
from PIL import Image
from django.utils.safestring import mark_safe

class NotebookAdminForm(ModelForm):



    def __init__(self, *args , **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['image'].help_text = mark_safe('<span style="color:red; font-size:14px">Загружай изображения с минимальным разрешением {}x{}</span>'.format(
            *Product.MIN_RESOLUTION))

    def clean_image(self):
        image = self.cleaned_data["image"]
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должен превышать 3МБ!")
        if img.height > max_height or img.width > max_width:
            raise ValidationError("Загруженное изображение больше максимального!")
        if img.height < min_height or img.width < min_width:
            raise ValidationError("Загруженное изображение меньше минимального!")
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey(db_field, request , **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request , **kwargs)


admin.site.register(Category)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)



