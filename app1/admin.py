from django.contrib import admin

# Register your models here.

from .models import Question
from .models import Picture, PictureTag

admin.site.register(Question)
admin.site.register(Picture)
admin.site.register(PictureTag)