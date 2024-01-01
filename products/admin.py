from django.contrib import admin
from django import forms
from .proxy import ProductProxy
from dadfes.admin import DfesAdminModelMixin

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = ProductProxy
        fields = ['code', 'title', 'subhead', 'description', 'type', 'image', 'thumbnail', 'order', 'price', 'stock', 'status']

@admin.register(ProductProxy)
class ProductAdmin(DfesAdminModelMixin, admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('code', 'title', 'subhead', 'type', 'price', 'stock', 'status', 'createdAt')
    list_filter = ('status', 'createdAt')
    ordering = ('createdAt',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_list(self, request, page_num, list_per_page):
        #   search = request.GET.get('q')
        #   order_by = request.GET.get('o')
        #   some_list_filter = request.GET.get('some_list_filter')
        return ProductProxy.get_list()

    def get_object(self, request, object_id, *args, **kwargs):
        return ProductProxy.get_by_id(object_id)

    def save_model(self, request, obj, form, change):
        data = ProductProxy.save(obj)
        if data.id:
            obj.id = data.id

    def delete_model(self, request, obj):
        ProductProxy.delete(obj)
