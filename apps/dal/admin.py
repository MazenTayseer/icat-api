from django.contrib import admin

from apps.dal.models import Answer, Assessment, Module, Question

# Register your models here.
admin.site.register(Module)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Answer)
