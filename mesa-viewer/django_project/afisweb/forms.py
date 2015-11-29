from afisweb.models import *
#from afisweb.filefield_extension_whitelist import *
from django import forms

class InputFileForm(forms.Form):
  """ Let the user specify a zip file containing a shapefile. """
  file = forms.FileField(label="Path to .zip file containing the shapefile",
                      required=True,
                      #help_text="Quick tip: use the Browse button to locate the file",
                      error_messages={'required':
                      ''' Invalid path. Please browse again. '''}
                      )
  
