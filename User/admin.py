from django.contrib import admin

# Register your models here.
from User.models import GetPublish, sign_publish, lecture_experience


class GetPublishAdmin(admin.ModelAdmin):
    list_display = ('username', 'reason', 'apply_time')
    search_fields = ("username",)


admin.site.register(GetPublish, GetPublishAdmin)


class sign_publishAdmin(admin.ModelAdmin):
    list_display = ('l_id', 'signPassword', 'p_id')
    search_fields = ("p_id", "l_id",)


admin.site.register(sign_publish, sign_publishAdmin)


class lecture_experienceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'l_id', 'title', 'content')
    search_fields = ("user_id", 'l_id',)


admin.site.register(lecture_experience, lecture_experienceAdmin)

admin.site.site_title = '讲座管理系统'

admin.site.site_header = "讲座管理系统后台界面"
