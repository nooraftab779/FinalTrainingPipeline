# from django.contrib import admin
# from .models import User
# from server.models import *
# import logging
#
#
# # Register your models here.
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('User_name', 'system_occupied')
#
#     def system_occupied(self, obj):
#         result = ServerReservation.objects.filter(user_id=obj.id)
#
#         for var in result:
#             if var.reservation_time < timezone.now() < var.end_time:
#                 return var.server_id
#         return None
#
#
#
# admin.site.register(User, UserAdmin)
