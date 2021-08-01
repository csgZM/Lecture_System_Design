from django.contrib import admin
from lecture_system.models import Lecture_Message


# Register your models here.
class Lecture_MessageAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'Lecture_title', 'Lecture_Pname', 'Lecture_SN', 'Lecture_category', 'Lecture_Stime', 'Lecture_Etime')
    search_fields = ('Lecture_title', 'Lecture_Pname', 'id',)


admin.site.register(Lecture_Message, Lecture_MessageAdmin)
