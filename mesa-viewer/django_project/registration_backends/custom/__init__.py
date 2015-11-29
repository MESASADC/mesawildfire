from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

from registration import signals
from registration.forms import RegistrationFormUniqueEmail
from django import forms
from registration.models import RegistrationProfile

from django.utils.translation import ugettext as _


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}


class CustomRegistrationForm(RegistrationFormUniqueEmail):

    first_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs_dict),
                                label=_("First Name"),
                                )

    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs_dict),
                                label=_("Last Name"),
                                )

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data.get('email')
        self._errors.pop('username', None)
        return super(RegistrationFormUniqueEmail, self).clean()


class CustomBackend(object):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.

    Customization: username field is not shown on the form, username is
    set to the same value as email address. First and last names also
    captured.
    """
    def register(self, request, **kwargs):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        email, password, first_name, last_name = kwargs['email'], kwargs['password1'], kwargs['first_name'], kwargs['last_name']
        """
        Create and immediately log in a new user.

        If the submitted email address (username) is longer than 30 chars,
            truncate.
        
        """
        # We need to truncate long usernames (email addresses) so that they
        # fit into the Django User models' username field. We also force the
        # email address to lower case.
        # NOTE: this is a pretty hacky quick fix!! George
        username = email[:30].lower()

        User.objects.create_user(username, email, password)
        
        # authenticate() always has to be called before login(), and
        # will return the user we just created.
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        if not new_user is None:
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.

        """
        activated = RegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)
        return activated

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        """
        Return the custom form class used for user registration.

        """
        return CustomRegistrationForm

    def post_registration_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        return ('/', (), {})

    def post_activation_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        account activation.

        """
        return ('registration_activation_complete', (), {})
