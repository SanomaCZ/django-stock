from django.db import models
from django.contrib import admin
from django import forms

from sorl.thumbnail.admin.current import AdminImageWidget
from sorl.thumbnail.shortcuts import get_thumbnail

from stock.forms import OperationForm
from stock.models import Item, Operation


class OperationInlineAdmin(admin.TabularInline):
    model = Operation
    extra = 0
    readonly_fields = ('user', 'operation_type', 'pieces', 'attachment')

    def has_delete_permission(self, request, obj):
        return False


class OperationAdmin(admin.ModelAdmin):

    list_display = ('user', 'item', 'operation_type', 'ts')
    list_filter = ('user', 'ts')
    exclude = ('user',)

    form = OperationForm

    def save_form(self, request, form, change):
        if change:
            raise forms.ValidationError("Cannot edit existing operation")
        super(OperationAdmin, self).save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(OperationAdmin, self).save_model(request, obj, form, change)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail', 'pieces')
    search_fields = ('name', 'slug')
    readonly_fields = ('pieces', 'slug')
    inlines = [OperationInlineAdmin]

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    def thumbnail(self, obj):
        im = get_thumbnail(obj.photo, "100x100", crop='center')
        return '<a href="%s"><img src="%s" width="%d" height="%d"></a>' % (obj.photo.url, im.url, im.width, im.height)
    thumbnail.allow_tags = True


admin.site.register(Item, ItemAdmin)
admin.site.register(Operation, OperationAdmin)
