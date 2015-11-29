"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.utils.unittest import TestCase
from django.utils import unittest 
from afisweb.models import *
from afisweb.views import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

# test functions

class getLayersListTest( unittest.TestCase ):
    def test_getLayersList( self ):
        """ Tests if the function collects correctly data from db. """
        #@TODO create fake http request
        #myRequest = HttpRequest()
        #myObjects = getLayersList( myRequest )
        
        self.failUnlessEqual(1+1, 2)

class getUsersNonDeletedLayersTest( TestCase ):
  def test_anonymous():
    from django.http import HttpRequest
    from django.contrib.auth.models import User
    myRequest = HttpRequest()
    myUser = User()
    myUser.username = 'anonymous'
    myRequest.user = myUser;
    getUsersNonDeletedLayers(myRequest)
