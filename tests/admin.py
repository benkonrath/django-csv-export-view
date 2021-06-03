from django.contrib import admin

from csv_export.views import CSVExportView

from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    actions = ("export_car_csv",)

    def export_car_csv(self, request, queryset):
        view = CSVExportView(queryset=queryset, fields="__all__")
        return view.get(request)

    export_car_csv.short_description = "Export CSV for selected Car records"
