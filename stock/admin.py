from django.core.urlresolvers import reverse
from django.db import models
from django.contrib import admin
from django.forms.widgets import Widget
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.conf import settings

from sorl.thumbnail.admin.current import AdminImageWidget
from sorl.thumbnail.shortcuts import get_thumbnail

from stock.forms import OperationForm
from stock.models import Item, Operation


class LinkWidget(Widget):

    def render(self, name, value, attrs=None):
        if value:
            return mark_safe('<a href="%s%s">%s</a>' % (settings.MEDIA_URL, value, str(value).split("/")[-1]))
        return ''


class OperationInlineAdmin(admin.TabularInline):
    model = Operation
    extra = 0
    readonly_fields = ('ts', 'user', 'operation_type', 'pieces')

    formfield_overrides = {
        models.FileField: {'widget': LinkWidget},
    }

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request):
        return False

    ordering = ('-ts',)


class OperationAdmin(admin.ModelAdmin):

    list_display = ('user', 'item', 'operation_type', 'ts')
    list_filter = ('user', 'ts', 'operation_type')
    search_fields = ('item__name', 'item__slug')
    exclude = ('user',)

    form = OperationForm

    def get_form(self, request, obj=None, **kwargs):
        if not obj and 'item' in request.GET:
            self.add_form_template = 'add_item_operation.html'
        else:
            self.add_form_template = None
        return super(OperationAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(OperationAdmin, self).save_model(request, obj, form, change)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail', 'pieces', 'add_operation')
    search_fields = ('name', 'slug')
    readonly_fields = ('pieces',)
    inlines = [OperationInlineAdmin]
    change_list_template = 'item_listing.html'

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    def thumbnail(self, obj):
        im = get_thumbnail(obj.photo, "100x100", crop='center')
        return '<a href="%s" class="fancybox"><img src="%s" width="%d" height="%d"></a>' % (obj.photo.url, im.url, im.width, im.height)
    thumbnail.allow_tags = True

    def add_operation(self, obj):
        url = reverse('admin:%s_%s_add' % ('stock', 'operation'), current_app=self.admin_site.name)
        return '<a href="%s?item=%s" id="add_id_operation" onclick="return showAddAnotherPopup(this);">%s</a><span id="id_operation"></span>' % (url, obj.pk, _("Add new operation"))
    add_operation.allow_tags = True

admin.site.register(Item, ItemAdmin)
admin.site.register(Operation, OperationAdmin)
