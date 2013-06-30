from django.contrib import admin
from stock.models import Item, Operation


class OperationInlineAdmin(admin.TabularInline):
    model = Operation
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'pieces')
    readonly_fields = ('pieces', 'slug')
    inlines = [OperationInlineAdmin]


admin.site.register(Item, ItemAdmin)
admin.site.register([Operation])
