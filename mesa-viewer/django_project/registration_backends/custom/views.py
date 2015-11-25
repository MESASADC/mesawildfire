# coding=utf-8
"""
views
"""
import json
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from registration_backends.custom.forms import CustomLoginForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login


@sensitive_post_parameters()
@csrf_protect
@never_cache
def custom_login(request, template_name='registration/login.html',
                 redirect_field_name=REDIRECT_FIELD_NAME,
                 authentication_form=CustomLoginForm,
                 current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            # Here we return JSON so that the newly ajax-ified login form
            # knows to reload the page (or redirect to redirect_to value)
            return HttpResponse(json.dumps({
                'success': True,
                'redirect_to': redirect_to
            }), content_type='application/json')
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)