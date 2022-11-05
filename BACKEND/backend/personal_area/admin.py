from django.contrib import admin
from personal_area.models import PersonalData

admin.register(PersonalData)

@admin.register(PersonalData)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "lastname")