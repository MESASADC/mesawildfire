# coding=utf-8
"""
templatetags.openlayersjs
"""
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def openlayersjs():
    if settings.LOCAL_OPENLAYERS:
        js_string = '''
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/OpenLayers-2.13.1/OpenLayers.js"></script>
        <script type="text/javascript" charset="utf-8" src="''' + settings.STATIC_URL + '''js/ZoomBar.js">	</script>
        <script type="text/javascript" charset="utf-8" src="''' + settings.STATIC_URL + '''js/ScaleBar.js"> </script>
        <script type="text/javascript" charset="utf-8" src="''' + settings.STATIC_URL + '''js/LoadingPanel.js"> </script>
        '''
    else:
        js_string = '''
        <script type="text/javascript" src="http://www.openlayers.org/api/OpenLayers.js"></script>
        <script type="text/javascript" charset="utf-8" src="''' + settings.STATIC_URL + '''js/ZoomBar.js">	</script>
        <script type="text/javascript" charset="utf-8" src="''' + settings.STATIC_URL + '''js/ScaleBar.js"> </script>
        <script type="text/javascript" charset="utf-8" src="''' + settings.STATIC_URL + '''js/LoadingPanel.js"> </script>
        '''
    return js_string
