from django.contrib import admin

from .models import MeterPoint, Meter, MeterReading


class MeterReadingAdmin(admin.ModelAdmin):
    list_display = [
        "reading",
        "time_of_reading",
        "meter",
    ]


admin.site.register(MeterPoint)
admin.site.register(Meter)
admin.site.register(MeterReading, MeterReadingAdmin)
