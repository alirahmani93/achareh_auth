from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Configuration

admin.site.register(Configuration)


@admin.action(description='Change status Reverse')
def change_status(model_admin, request, queryset):
    for obj in queryset:
        obj.is_active = not obj.is_active
        obj.save()


@admin.action(description='Change status to False')
def change_status_false(model_admin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='Change status to True')
def change_status_true(model_admin, request, queryset):
    queryset.update(is_active=True)


class BaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['__str__', "is_active", 'updated_time', 'created_time', ]
    list_filter = ["is_active", 'updated_time', 'created_time', ]
    search_fields = ["id", "uuid", ]

    save_on_top = True

    list_select_related = True
    list_per_page = 100
    list_max_show_all = 200

    save_as = True
    save_as_continue = True
    preserve_filters = True

    # Actions
    actions_on_top = True
    actions_on_bottom = True
    actions = [change_status, change_status_false, change_status_true]

    def get_readonly_fields(self, request, obj=None):
        all_fields = ['uuid', 'created_time', 'updated_time']
        return all_fields


class BaseInlineAdmin:
    extra = 0
    model = None
    min_num = None
    max_num = None
    verbose_name = None
    verbose_name_plural = None
    can_delete = True
    show_change_link = True


class BaseTabularInline(BaseInlineAdmin, admin.TabularInline):
    pass


class BaseStackedInline(BaseInlineAdmin, admin.StackedInline):
    pass
