from django.contrib import admin
from . import models
from django.apps import apps
# Register your models here.

models = apps.get_app_config("data_sync").get_models()

[admin.site.register(model) for model in models]
