from django.contrib import admin, messages
from django import forms
from .proxy import ExternalUserProxy
from dadfes.admin import DfesAdminModelMixin

class ExternalUserAdminForm(forms.ModelForm):
    class Meta:
        model = ExternalUserProxy
        fields = ['fullName', 'phone', 'email', 'role', 'gender', 'image', 'thumbnail', 'birthday', 'password', 'status']

@admin.register(ExternalUserProxy)
class ExternalUserAdmin(DfesAdminModelMixin, admin.ModelAdmin):
    form = ExternalUserAdminForm
    list_display = ('fullName', 'phone', 'email', 'role', 'gender', 'status', 'createdAt')
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
        return ExternalUserProxy.get_list()

    def get_object(self, request, object_id, *args, **kwargs):
        return ExternalUserProxy.get_by_id(object_id)

    def save_model(self, request, obj, form, change):
        data = ExternalUserProxy.save(obj)
        if data.id:
            obj.id = data.id

    def delete_model(self, request, obj):
        ExternalUserProxy.delete(obj)
