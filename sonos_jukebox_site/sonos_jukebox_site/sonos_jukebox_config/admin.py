from django.contrib import admin
from sonos_jukebox_config.models import Configuration
from sonos_jukebox_config.models import JukeboxShortCut

class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']



class JukeboxShortCutAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'type']


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(JukeboxShortCut, JukeboxShortCutAdmin)