from django.contrib import admin

from .models import EditingRight, Organization, Worker


class EditingRightInLine(admin.TabularInline):
    model = Organization.editors.through
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("pk", "creator", "name", "address", "description")
    inlines = (EditingRightInLine,)
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "full_name",
        "position",
        "work_number",
        "private_number",
        "fax",
        "organization",
    )
    search_fields = ("full_name",)
    empty_value_display = "-пусто-"


@admin.register(EditingRight)
class EditingRightAdmin(admin.ModelAdmin):
    list_dispaly = ("pk", "editor", "organization")
    empty_value_display = "-пусто-"
