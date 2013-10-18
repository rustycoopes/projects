from django.contrib import admin
from sonos_jukebox_config.models import Configuration

class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']


admin.site.register(Configuration, ConfigurationAdmin)