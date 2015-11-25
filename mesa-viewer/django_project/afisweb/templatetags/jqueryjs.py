from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def jqueryjs():
    if settings.LOCAL_JQUERY:
        js_string = '''
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery-1.5.1.min.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery-ui-1.8.13.custom.min.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.fancybox-1.2.6.pack.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.easing.1.3.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.layout.min-1.2.0.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.jbanner.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.cookie.js"></script>
        '''
    else:
        js_string = '''
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.fancybox-1.2.6.pack.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.easing.1.3.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.layout.min-1.2.0.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.jbanner.js"></script>
        <script type="text/javascript" src="''' + settings.STATIC_URL + '''js/jquery.cookie.js"></script>
        '''
    return js_string
