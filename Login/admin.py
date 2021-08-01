from django.contrib import admin
from Login.models import Register_UserInfo, UserToken, Reserved_Lecture, Listened_Lecture, Published_Lecture


# Register your models here.
class Register_UserInfoAdmin(admin.ModelAdmin):
    list_display = ('Username', 'PassWord', 'PhoneNumber', 'Email', 'nikename')
    search_fields = ('Username', 'PhoneNumber', 'Email')


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'publish_power', 'user_id_id')
    search_fields = ('token', 'user_id_id', 'publish_power',)


class Reserved_LectureAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'lecture_id',)
    search_fields = ('user_id', 'lecture_id')


class Listened_LectureAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'lecture_id',)
    search_fields = ('user_id', 'lecture_id',)


class Published_LectureAdmin(admin.ModelAdmin):
    list_display = ('user_id_id', 'lecture_id',)
    search_fields = ('user_id_id', 'lecture_id',)


admin.site.register(Reserved_Lecture, Reserved_LectureAdmin, )
admin.site.register(Listened_Lecture, Listened_LectureAdmin, )
admin.site.register(Published_Lecture, Published_LectureAdmin, )

admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(Register_UserInfo, Register_UserInfoAdmin)
