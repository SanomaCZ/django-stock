from django.contrib import admin
from stock.models import Item, Operation


class OperationInlineAdmin(admin.TabularInline):
    model = Operation
    extra = 0
    readonly_fields = ('user', 'type', 'pieces', 'attachment')

    def has_delete_permission(self, request, obj):
        return False


class OperationAdmin(admin.ModelAdmin):
    pass


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'pieces')
    readonly_fields = ('pieces', 'slug')
    inlines = [OperationInlineAdmin]


admin.site.register(Item, ItemAdmin)
admin.site.register([Operation])
