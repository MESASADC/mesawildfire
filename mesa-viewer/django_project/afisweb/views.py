from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.core.mail import send_mail, mail_admins
from django.template.loader import get_template

from django.db import connection, transaction, connections

from afisweb.models import *
from afisweb.forms import *

# to serialize PlaceNames into JSON format, as required by Places
# autocompletion javascript thingy
from django.core import serializers
from django.utils import simplejson

from afisweb.getFeaturesFromZipFile import *
from django.utils.html import escapejs
from django.views.decorators.csrf import ensure_csrf_cookie

from settings import *
from afisweb.renderDecorator import renderWithContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.conf import settings
from django.template import RequestContext
from django.db.models import Q
from django.db.models import Count

import logging
import urllib  # for fetching fire stats and getFeatureInfo
import urllib2
from django_project.afisweb.models import LegendGroup
import os
import sys
import time  # for normalising dates from jquery input
import datetime  # for normalising dates from jquery input
import re

from xml.dom import minidom
import re
import json


from browsercap import BrowserCapabilities

CountryMap = {
    # country code: (longitude, latitude, zoom)
    'AO': (18, -11.5, 6),
    'BW': (24, -22, 6),
}
# renderWithContext is explained in renderDecorator.py


def landingPage(theRequest):
    browser_string = ''
    try:
      bc = BrowserCapabilities()
      browser = bc(theRequest.META.get('HTTP_USER_AGENT'))
      try_old_browser = theRequest.GET.get('try_old_browser')
      browser_string = browser.name() + ' ' + str(browser.version())
      if not (try_old_browser == 'true') and (browser.name() == 'IE') and (int(browser.version()[0]) <= 6):
          params['browser_ok'] = False
          return render_to_response("browser_problem.html", params)
    except:
      logging.warn("exception while trying to determine browser version")
      

    params = {'myUseGoogleFlag': settings.USE_GOOGLE, 'browser_ok': True, 'browser':
              browser_string, 'autorefresh': bool('true' == theRequest.GET.get('autorefresh', 'false'))}

    lat = theRequest.GET.get('lat', None)
    lon = theRequest.GET.get('lon', None)
    zoom = theRequest.GET.get('zoom', None)
    country = theRequest.GET.get('country', '').upper()

    # from middleware.request_object_access import get_request_object
    # params["host"] = str(get_request_object().get_host())

    if lat is not None and lon is not None:
        try:
            params['lat'] = float(lat)
            params['lon'] = float(lon)
        except:
            pass
    elif country in CountryMap:
        params['lon'], params['lat'], params['zoom'] = CountryMap[country]

    if zoom is not None:
        try:
            params['zoom'] = int(zoom)
        except:
            pass
    # Get advertisement based on URL hostname, if any
    urlhost = theRequest.get_host()
    fsdic = None
    for dic in FIRE_STATS_MODIS:
        if "hostre" in dic and dic['hostre'].search(urlhost):
            fsdic = dic
            break
    if fsdic and "advert" in fsdic and fsdic["advert"]:
        params['advertisement'] = fsdic["advert"]
    # Deprecate settings.FIRE_STATS_MODIS;
    # Include <div id="overpass_info"></div> based on urlhost
    # Use ajax qi/next_overpass to periodically refresh
    if "africa" in urlhost.lower():
        params['display_overpass_info'] = True
    return render_to_response("index.html", params, RequestContext(theRequest))

def help(theRequest):
    return render_to_response("help.html")


def disclaimer(theRequest):
    return render_to_response("disclaimer.html")


def partners(theRequest):
    return render_to_response("partners.html")


def addBackdropLayers(theRequest):
    return render_to_response('backdropLayers.js',
                              {'myUseGoogleFlag': settings.USE_GOOGLE},
                              context_instance=RequestContext(theRequest),
                              mimetype="application/javascript")


def addDataLayers(theRequest):
    """Returns a javascript function to add layers to the map according to user preferences."""
    myObjects = getUsersNonDeletedLayers(theRequest)
    return render_to_response('dataLayers.js',
                              {'myObjects': myObjects},
                              context_instance=RequestContext(theRequest),
                              # mimetype="text/html" )
                              mimetype="application/javascript")

# renderWithContext is explained in renderDecorator.py


@renderWithContext('legend.html')
def showLegend(theRequest):
    """Returns the legend containing layers according to user preferences."""
    myObjects = getUsersNonDeletedLayers(theRequest)
    logging.debug("User has %s non deleted layers" % len(myObjects))

    myLegends = getUniqueLegendGroups(myObjects)
    logging.debug("User has %s layer groups" % len(myLegends))

    return ({'myObjects': myObjects, 'myLegends': myLegends})


def showFireStats_pre20111107(theRequest):
    logging.info("Show fire stats called")
    # modis
    count48mod = getSAFireCount('MODIS', 48, False)
    if not count48mod:
        count48mod = 'No'
    count24mod = getSAFireCount('MODIS', 'today', False)
    if not count24mod:
        count24mod = 'No'
    count24modlocal = getSAFireCount('MODIS', 'today', True)
    if not count24modlocal:
        count24modlocal = 'No'
    # msg
    count48msg = getSAFireCount('msg_abba', 48, False)
    if not count48msg:
        count48msg = 'No'
    count24msg = getSAFireCount('msg_abba', 'today', False)
    if not count24msg:
        count24msg = 'No'
    count24msglocal = getSAFireCount('msg_abba', 'today', True)
    if not count24msglocal:
        count24msglocal = 'No'

    str48mod = "<b>" + str(
        count48mod) + "</b> MODIS fire detections in Southern Africa the last <b>48 hours</b>. "
    str24mod = "<b>" + str(
        count24mod) + "</b> MODIS fire detections in Southern Africa <b>today</b>. "
    strlocalmod = "<br/><b>" + str(
        count24modlocal) + "</b> MODIS fire detections in your area (<10km) <b>today</b>.<br/>"

    str48msg = "<b>" + str(
        count48msg) + "</b> MSG fire detections in Southern Africa the last <b>48 hours</b>. "
    str24msg = "<b>" + str(
        count24msg) + "</b> MSG fire detections in Southern Africa <b>today</b>. "
    strlocalmsg = "<br/><b>" + str(
        count24msglocal) + "</b> MSG fire detections in your area (<10km) <b>today</b>.<br/>"

    return HttpResponse(str48mod + str24mod + strlocalmod + str48msg + str24msg + strlocalmsg)

def getRegionalParams(theRequest):
    "Fetch regional parameters based on hostname in request"
    urlhost = theRequest.get_host()
    for dic in FIRE_STATS_MODIS:
        if "hostre" in dic and dic['hostre'].search(urlhost):
            return dic
    return {}

def showFireStats(theRequest):
    logging.debug("Show fire stats called")

    try:
        timezoneoffset_min = int(urllib.unquote(theRequest.COOKIES.get(
            'timezoneoffset', '0')))  # should have been set in afis.js
    except Exception, err:
        logging.warning("showFireStats: invalid tzo cookie value '%s': %s" %
            (theRequest.COOKIES.get('timezoneoffset', 'NOCOOKIE'), err))
        timezoneoffset_min = 0

    fsdic = getRegionalParams(theRequest)
    colorize = lambda color, dtval: '<font color="%s">%s</font>' % (color, dtval.strftime('%Y-%m-%d %H:%M'))
    respdic = {}
    eta = last_eta = None # datetime values in user's timezone
    if "next" in fsdic and fsdic["next"]:
        try:
            eta, last_eta = get_overpass_datetime(
                'fire_modis_next_pass'+fsdic["ext"],
                fsdic["next"],
                tzo_min=timezoneoffset_min,
                latency_min=30)
            respdic['modis_next_update'] = colorize('green', eta)
        except Exception, err:
            respdic['modis_next_update'] = '<font color="red">%s</font>'%err
    if "prev" in fsdic and fsdic["prev"]:
        try:
            eta = get_overpass_datetime(
                'fire_modis_previous_pass'+fsdic["ext"],
                fsdic["prev"],
                tzo_min=timezoneoffset_min,
                cachettl=FIRE_STATS_CACHE_TTL)[0]
            # If last-update time is older than previous predicted value
            if last_eta and eta < last_eta:
                color = 'red'
            else:
                color = 'green'
            respdic['modis_last_update'] = colorize(color, eta)
        except Exception, err:
            respdic['modis_last_update'] = '<font color="red">%s</font>'%err
    logging.debug("respdic=%s" % respdic)
    return render_to_response("fireStats.html", respdic)

def redirect_mapserver_request(theRequest, params=''):
    """ This is to work around jQuery load() restricting cross-site URL
        It fetches MODIS swath image from the mapserver CGI
        which is running on a different web server.

        Example IMG SRC URL to fetch latest true-colour swath
        http://afis.meraka.org.za/cgi-bin/mapserv?map=/opt/mapserver/modis.map&mode=map&layers=modis_tc_0
    """
    full_url = "%s?%s" % (settings.AFIS_MAPSERVER_URL, params)
    return HttpResponse('<a href="%(url)s" target="_popup"><img width="200px" height="200px" src="%(url)s"></img></a>' % {"url": full_url})


@renderWithContext('layermanager.html')
def showLayerManager(theRequest):
    """Returns the layer manager i.e. the side-by-side list of available and chosen layers for the user legend."""
    myDeletedObjects = getUsersDeletedLayers(theRequest)
    myNonDeletedObjects = getUsersNonDeletedLayers(theRequest)
    logging.info("User has %s deleted layers" % len(myDeletedObjects))
    logging.info("User has %s active layers" % len(myNonDeletedObjects))
    return ({'myDeletedObjects': myDeletedObjects, "myNonDeletedObjects": myNonDeletedObjects})


def getAnonymousUser(request):
    """Returns the name of the anonymous user based on the hostname (for localisation purposes)."""
    afisHost = request.get_host()
    if afisHost.startswith('southernafrica.'):
        return 'anonymous_southernafrica'
    else:
        return 'anonymous'

# helper method not exposed as a view


def getAllUserLayers(theRequest):
    """ Get users layers - both deleted and non-deleted ones. """
    if theRequest.user.username is not "":
        logging.info("Username: " + theRequest.user.username)
        # recall the status of layers at previous login
        myObjects = addDefaultLayersForUser(theRequest)
    return myObjects

def getUsersDeletedLayers(theRequest):
    """ Get users layers - only ones marked as deleted though.
        Anonymous users cant manage layers
    """
    if theRequest.user.username == "":
        theRequest.user.username = getAnonymousUser(theRequest)
    logging.info("Username: " + theRequest.user.username)
    # recall the status of layers at previous login
    myObjects = addDefaultLayersForUser(theRequest)
    if len(myObjects) > 0:
        myObjects = myObjects.exclude(is_deleted=False)
    return myObjects

# helper method not exposed as a view

def getUniqueLegendGroups(UserWMSLayers):
    """ Filter for unique legend groups
    """
    myLegendGroupsValues = UserWMSLayers.values('wmslayer__legend_group__pk','wmslayer__legend_group__order','wmslayer__legend_group__title')
    myLegendGroups = myLegendGroupsValues.annotate(count=Count('wmslayer__legend_group'))
    myLegendGroupsFiltered = myLegendGroups.filter(count__gt=0).order_by('wmslayer__legend_group__order')

    return myLegendGroupsFiltered


def getUsersNonDeletedLayers(theRequest):
    """ Get users layers - only ones NOT marked as deleted though.
        Anonymous users cant manage layers
    """
    myAnonymousFlag = False
    if theRequest.user.username == "":
        myAnonymousFlag = True
        theRequest.user.username = getAnonymousUser(theRequest)
    logging.info("Username: " + theRequest.user.username)
    myObjects = addDefaultLayersForUser(theRequest)

    if myAnonymousFlag:
        logging.info("Checking for session layers")
        mySessionLayers = theRequest.session.get('queryLayers', False)
        if mySessionLayers:
            logging.info("Session layers found")
            # only show the user their own created date query layers
            # for logical or operations you need to use two Q objects see
            # https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-
            # lookups-with-q-objects
            myObjects = myObjects.filter(Q(
                id__in=mySessionLayers) | Q(is_default=True))
        else:
            logging.info("No session layers")
            # user has no session so remove all ephemeral layers
            myObjects = myObjects.filter(is_default=True)
    return myObjects


def addDefaultLayersForUser(theRequest):
    """Clones the anonymous/template user's layers to this user"""
    afisHost = theRequest.get_host()
    theUser = theRequest.user
    if afisHost.startswith('southernafrica.'):
        template_user = 'template_southern_africa'
    else:
        template_user = 'template'

    if theRequest.user.is_authenticated():
        fexp = Q(user=theRequest.user)
    else:
        fexp = Q(user__username=theRequest.user.username)
    # Get existing wmslayer_id of user
    existing_wmslayer_ids = UserWmsLayer.objects.filter(fexp).values('wmslayer')
    # Get wmslayer_id of template, excluding layers user already has
    myObjects = UserWmsLayer.objects \
        .filter(user__username=template_user) \
        .filter(is_default=True) \
        .exclude(wmslayer__in=existing_wmslayer_ids)
    logging.info("getting default layers from %s" % template_user)
    if theRequest.user.is_authenticated():
        logging.info("the user is authenticated: %s" % theUser.username)
        for myObject in myObjects:
            logging.info(" adding %s" % myObject.wmslayer.name)
            myUserWmsLayer = UserWmsLayer(user=theUser,
                                      wmslayer=myObject.wmslayer,
                                      is_visible=myObject.is_visible,
                                      is_deleted=False,
                                      order=myObject.order,
                                      is_default=True)
            myUserWmsLayer.save()
    else:
        logging.info("the user is not authenticated: %s" % theUser.username)

    myNewObjects = UserWmsLayer.objects.filter(fexp)
    return myNewObjects

def getSAFireCount(sensor, hours, bbox):
    logging.info("getSAFireCount called")

    myFileName = "fire" + dateQuery + str(hours) + str(bbox)
    myLocalPath = os.path.join(settings.FIRE_ROOT, myFileName)

    # now, in seconds from the Epoch.
    now = time.time()
    if os.path.exists(myLocalPath):
        then = os.stat(myLocalPath).st_mtime
    else:
        then = now
    if not os.path.exists(myLocalPath) or (now - then > settings.FIRE_STATS_REFRESH_TIME):
        logging.info("Fetching stats from WFS request.")
        timeperiod = str(hours)
        if timeperiod.isdigit():  # e.g. 48, 24
            timeperiod  = timeperiod + \
                "h"  # names of digit based service end with h
        myUrl = settings.AFIS_WFS_URL + \
            "?request=GetFeature&version=1.1.0&typeName=openafis:af_%s_datetime_%s&outputFormat=GML2&resultType=hits" % (
                sensor.lower(), timeperiod)
        logging.info(myUrl)
        if (bbox):
            myUrl = myUrl + "&bbox=-25.83688,28.18836,-25.65722,28.36802"
        # Save out the response
        myResponse = urllib.urlopen(myUrl, proxies=settings.PROXIES)
        myRawResponse = myResponse.read()
        myFile = file(myLocalPath, "wt")
        myFile.write(myRawResponse)
        myFile.close()

    else:
        logging.info("Reading from " + myLocalPath)
        pass

    # Read the XML
    try:
        xmlObject = minidom.parse(myLocalPath)
        splittedXml = xmlObject.firstChild.toxml().split(" ")
        logging.info(splittedXml)
        for token in splittedXml:
            logging.info(token)
            tokenList = token.split("=")
            if tokenList[0] == "numberOfFeatures":
                numMatches = int(tokenList[1].replace("\"", ""))
                logging.info("Matches found %d" % numMatches)
                return numMatches
    except:
        os.remove(myLocalPath)
        return "Fire stats could not be retrieved"

def load_datetime_string(cachepathname):
    # Returns UTC datetime value of overpass from cache, or None
    # Expects file to contain "YYYY-mm-dd %H:%M:%S\n"
    if os.path.exists(cachepathname) is False or \
       os.path.getsize(cachepathname) == 0:
        return None
    with open(cachepathname) as fh:
        dtstring = fh.readline().rstrip('\n')
    try:
        dtval = datetime.datetime.strptime(dtstring, '%Y-%m-%d %H:%M:%S')
    except Exception, err:
        msg = "Bad overpass datetime in %s: '%s': %s" % (cachepathname, dtstring, err)
        logging.warning("get_overpass_datetime: "+msg)
        dtval = None
    return dtval

def get_overpass_datetime(cachename, querycmd, tzo_min=0, latency_min=0, cachettl=None):
    """Returns a fresh overpass datetime in user's timezone,
       and previous value from cache if it was different
       cachettl, if given, implies previous overpass query and vice-versa."""
    logging.info("get_overpass_datetime")
    myLocalPath = os.path.join(settings.FIRE_ROOT, cachename)
    # Adjust to user's localtime;
    # and add processing time to predicted overpass
    delta = datetime.timedelta(minutes=tzo_min+latency_min)
    now = datetime.datetime.utcnow()
    utcdatetime = load_datetime_string(myLocalPath)
    run_query = utcdatetime is None
    if run_query is False:
        if cachettl:
            # Previous overpass
            last_updated = datetime.datetime.utcfromtimestamp(os.path.getmtime(myLocalPath))
            run_query = last_updated + abs(datetime.timedelta(**cachettl)) < now
        else:
            # Next overpass, cache value is valid as long as it's future
            run_query = utcdatetime <= now
    if run_query:
        rc = os.system(querycmd + ' > %s' % myLocalPath)
        if rc == 0:
            newval = load_datetime_string(myLocalPath)
        if rc != 0 or newval is None:
            logging.error("get_overpass_datetime failed: %s" % querycmd)
            raise ValueError("Overpass database query failed")
    else:
       return utcdatetime+delta, None
    if utcdatetime:
        return newval+delta, utcdatetime+delta
    else:
        return newval+delta, None


import simplejson
from django.template import Template, Context
import datetime
from googlemaps import GoogleMaps
import urlparse
from urlparse import parse_qs


'''
   Converts julian day to gregorian date
   Source:http://code.activestate.com/recipes/117215-a-date-module/
'''


def DateFromJDNumber(n):
    """Returns a date corresponding to the given Julian day number."""
    if not isinstance(n, int):
        raise TypeError("%s is not an integer." % str(n))

    a = n + 32044
    b = (4*a + 3)//146097
    c = a - (146097*b)//4
    d = (4*c + 3)//1461
    e = c - (1461*d)//4
    m = (5*e + 2)//153
    day = e + 1 - (153*m + 2)//5
    month = m + 3 - 12*(m//10)
    year = 100*b + d - 4800 + m/10
    ret = datetime.datetime.strptime(str(
        year)+"-"+str(month)+"-"+str(day), '%Y-%m-%d')
    return ret.strftime('%Y-%m-%d')


def curingCalc(eviList):
    modis_fillvalue = -0.3
    curing_percentile = 0.95
    eviNofill = []
    curing = []
    for item in eviList:
        if item != modis_fillvalue:
            eviNofill.append(item)
    eviNofill.sort()
    minPercentile = eviNofill[int((
        1.0 - curing_percentile)*len(eviNofill)+0.5)]
    maxPercentile = eviNofill[int((curing_percentile*len(eviNofill)+0.5))]
    delta = maxPercentile - minPercentile
    for item in eviList:
        if item != modis_fillvalue:
            c = 1.0 - (item - minPercentile)/delta
            if (c < 0):
                c = 0
            elif (c > 1.0):
                c = 1.0
        else:
            c = modis_fillvalue
        curing.append(c)
    index = 0
    for curings in curing:
        if curings != modis_fillvalue:
            curing[index] = int(curings*100)
        index = index + 1
    return curing


def hex_to_rgb(value):
    # value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))


def triplet(rgb):
    return format((rgb[0] << 16) | (rgb[1] << 8) | rgb[2], '06x')


def calc_Luminance(rgb):
    blue = rgb[0] / 255.
    green = rgb[1] / 255.
    red = rgb[2] / 255.
    luminance = red * 0.2126 + green * 0.7152 + blue * 0.0722
    return luminance


def getFireReport(theRequest):
    try:
        wsgi_get_request = theRequest.GET
        theLat = wsgi_get_request['theLat']
        theLon = wsgi_get_request['theLon']
       
        clientIP = theRequest.META.get('HTTP_X_FORWARDED_FOR', theRequest.META['REMOTE_ADDR'])
        opener = urllib2.build_opener()
        # Pass along the original user agent and IP so cubeserver can produce better logs
        opener.addheaders = [
            ('User-Agent', theRequest.META['HTTP_USER_AGENT']),
            ('X-Forwarded-For', clientIP)
        ]
        response = opener.open("http://qi.afis.meraka.org.za/mobileFireReport/?lat="+theLat+"&lon="+theLon)
        if response.code == 200:
            decoded_json = json.loads(response.read())
        else:
            decoded_json = {}

        Location = {}
        try:
            landCoverContainer = decoded_json['NLC'] 
            landCoverType =  landCoverContainer['class']
            Location['landCoverClass'] = landCoverType
        except:
            pass
        try:
            landCoverContainer = decoded_json['USNLC']
            landCoverType = landCoverContainer['class']
            Location['landCoverClass'] = landCoverType
        except:
            pass

        timeScale = decoded_json['time']
        yTemp = decoded_json['EVI']
        yData = yTemp['y']
        FDI_Data = decoded_json['FDI']
        Summary_Data = decoded_json['burndate']

        curing = curingCalc(yData)

        curingNoFill = []
        for item in curing:
            if (item != -0.3):
                curingNoFill.append(item)
        greg_dates = []
        for item in timeScale:
            greg_date = DateFromJDNumber(item)
            greg_dates.append(greg_date)
        date_curing_pair = []
        x_y = {}
        index = 0

        for a_date in greg_dates:
            x_y['curing'] = curing[index]
            x_y['date'] = a_date
            date_curing_pair.append(x_y)
            index = index + 1
            x_y = {}

        Sorted_FDI_Data = {}
        Day_of_Week = []
        Sorted_Dates = []
        Sorted_LFDI = []
        Sorted_Temp = []
        Sorted_Humidity = []
        Sorted_Wind = []
        Sorted_FPI = []
        Location["lon"] = round(float(theLon), 3)
        Location["lat"] = round(float(theLat), 3)

        address_url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + \
            theLat+","+theLon+"&sensor=false"
        address_dict = urllib.urlopen(address_url).read()
        address_data = json.loads(address_dict)
        if address_data['status'] == "OK":
            data_holder = address_data['results']
            try:
                Location['placeName'] = data_holder[1]['formatted_address']
            except:
                Location['placeName'] = data_holder[0]['formatted_address']

        if Summary_Data['dates']:
            last_burn_date = Summary_Data['lastBurnDate']
            val = DateFromJDNumber(last_burn_date)
            now_last_burn_date_interval = ((
                datetime.datetime.now() - datetime.datetime.strptime(val, '%Y-%m-%d')).days)/365.0
            Summary_Data['lastBurnDate'] = round(
                now_last_burn_date_interval, 1)

        for k, v in sorted(FDI_Data.items()):
            try:
                Sorted_Dates.append(k)
            except:
                pass
            try:
                Sorted_LFDI.append(v['LFDI'])
            except:
                pass
            try:
                Sorted_Temp.append(int(v['temp_c']))
            except:
                pass
            try:
                Sorted_Humidity.append(int(v['rh_pct']))
            except:
                pass
            try:
                Sorted_Wind.append(int(v['ws_kmh']))
            except:
                pass
        max = len(Sorted_LFDI)
        if(max == 7):
            max = 5
        if (len(Sorted_Dates) > max):
            del Sorted_Dates[max:]
            del Sorted_LFDI[max:]
            del Sorted_Temp[max:]
            del Sorted_Humidity[max:]
            del Sorted_Wind[max:]
        rgbs = []
        luminanceList = []

        for item in Sorted_LFDI:
            rgb = hex_to_rgb(item[1])
            rgbs.append(rgb)
        for i in rgbs:
            luminance = calc_Luminance(i)
            luminanceList.append(luminance)
        counter = 0
        color = ""
        for i in Sorted_LFDI:
            if luminanceList[counter] > 0.6:
                color = "000000"
            else:
                color = "ffffff"
            i.append(color)
            counter = counter + 1
        if (len(Sorted_FPI) > 0):
            for i in Sorted_FPI:
                if luminanceList[counter] > 0.6:
                    color = "000000"
                else:
                    color = "ffffff"
                i.append(color)
            counter = counter + 1

        try:
            FPI_Container = decoded_json['FPI']
            for k, v in sorted(FPI_Container.items()):
                Sorted_FPI.append(v)
            del Sorted_FPI[len(Sorted_Dates):]
        except:
            pass

        index = 0
        for i in timeScale:
            gregorian_date = DateFromJDNumber(i)
            timeScale[index] = gregorian_date
            index = index + 1

        days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        for item in Sorted_Dates:
            Day_of_Week_Num = datetime.datetime.strptime(
                item, '%Y-%m-%d').weekday()
            Day_of_Week.append(days[Day_of_Week_Num])
        try:
            tzo = theRequest.COOKIES.get('timezoneoffset', '0')
            read_weather_data = urllib.urlopen("http://qi.afis.meraka.org.za/firedanger_aws/?lat="+str(
                theLat)+"&lon="+str(theLon)+"&tz="+str(tzo)).read()
            weather_data = json.loads(read_weather_data)
            stations_data = []
            stationInfo = {}
            data_per_station = []

            for stationItem in weather_data:
                stationInfo['station_name'] = stationItem['station_name']
                stationInfo['distance_m'] = stationItem['distance_m']/1000
                totalReadings = len(stationItem['data'])
                stations_data.append(stationInfo)
                if(totalReadings > 6):
                    startPoint = totalReadings-6
                    endPoint = len(stationItem['data'])
                    data_per_station_reduced = stationItem['data'][startPoint:]
                    data_per_station.append(data_per_station_reduced)
                else:
                    data_per_station.append(stationItem['data'])
                
                stationInfo = {}

            for readings in data_per_station:
                for data in readings:
                    hexa = data['LFDI'][1]
                    rgb = hex_to_rgb(hexa)
                    luminance = calc_Luminance(rgb)
                    if luminance > 0.6:
                        data['LFDI'].append("000000")
                    else:
                        data['LFDI'].append("ffffff")

            fireReportHtml = render_to_response('firereport2.html', Context({'days': Day_of_Week, 'dates': Sorted_Dates, 'FDI': Sorted_LFDI, 'Temp': Sorted_Temp, 'Humidity': Sorted_Humidity, 'Wind': Sorted_Wind, 'Summary':
                                                Summary_Data, 'location': Location, 'curing': curing, "curingNoFill": curingNoFill, "date_curing": date_curing_pair, "weather_stationInfo": stations_data, "detailed_weatherInfo": data_per_station, "FPI": Sorted_FPI}))
        except:
            fireReportHtml = render_to_response('firereport2.html', Context({'days': Day_of_Week, 'dates': Sorted_Dates, 'FDI': Sorted_LFDI, 'Temp': Sorted_Temp, 'Humidity':
                                                Sorted_Humidity, 'Wind': Sorted_Wind, 'Summary': Summary_Data, 'location': Location, "curingNoFill": curingNoFill, "date_curing": date_curing_pair, "FPI": Sorted_FPI}))
        return HttpResponse(fireReportHtml)
    except Exception as e:
        return HttpResponse("Data unavailable for chosen location.")


import cgi
import cgitb


def getFeatureInfo(theRequest,
                   theLon,
                   theLat,
                   theBoundingBox,
                   thePixelX,
                   thePixelY,
                   theMapWidth,
                   theMapHeight,
                   theMapScale):
    """ This view substituse proxy.cgi, the generic script that would allow JavaScript to
        do cross-site XHttpRequests. It is safer than it because the logic is private to
        this view. This approach also allows us to have a unified look and feel for the results."""

    logging.info("getFeatureInfo called \nLon: %s Lat: %s BBox: %s X: %s Y: %s Height: %s Width: %s Scale %s" % (
                     theLon,
                     theLat,
                     theBoundingBox,
                     thePixelX,
                     thePixelY,
                     theMapWidth,
                     theMapHeight,
                     theMapScale))
    myResponseHtml = """<div class="feature-info">"""
    myRawResponse = None

    # 20130115
    tzo = urllib.quote(urllib.unquote(theRequest.COOKIES.get(
        'timezoneoffset', '0')))  # should have been set in afis.js
    tz = urllib.quote(urllib.unquote(theRequest.COOKIES.get(
        'timezone', '0')))  # should have been set in afis.js
    boundingbox = theRequest.GET.get('boundingbox', False)
    gsLayerNames = []  # Geoserver layers
    msLayerNames = []  # Mapserver layers
    logging.info("getFeatureInfo tzo='%s' boundingbox=%s gLayers[]=%s" % (
        tzo, boundingbox, theRequest.GET.getlist('gLayers[]')))
    # E.g. gLayers = layers=[u'lyr2101', u'lyr2100', u'lyr29', u'lyr199',
    # u'lyr37']
    has_questionmark = re.compile('\?')
    is_notqueryable = re.compile('LayerNotQueryable')

    for myLayerName in theRequest.GET.getlist('gLayers[]'):

	myNoResponseHtml = ""
        myLayer = None
        myDateFilter = ""
        myUser = None

        if theRequest.user.is_authenticated and theRequest.user.username is not "":
            myUser = theRequest.user
        else:
            myUser = get_object_or_404(
                User, username=getAnonymousUser(theRequest))

        logging.info('User is ' + myUser.username)

        if myLayerName == "Query Position":
            continue

        logging.info("Getting feature info for %s" % myLayerName)
        myLayerId = int(myLayerName.replace("lyr", ""))
        try:
            myLayer = WmsLayer.objects.get(id=myLayerId)
        except Exception as e:
            logging.debug("No WmsLayer for %s (%s): %s" % (
                myLayerName, myLayerId, e))
            continue

        # 20130115
        u = re.sub(r'_TZOFFSET_', tzo, myLayer.url)
        u = re.sub(r'_TIMEZONE_', tz, u)
        logging.info("getFeatureInfo layer url: '%s' becomes '%s'" %
                     (myLayer.url, u))
        myLayer.url = u
        if has_questionmark.search(myLayer.url):
            qs_separator = '&'
        else:
            qs_separator = '?'
        if boundingbox:
            # Geoserver myLayerName is "{store}:{layername}" e.g.
            # "openafis:national_towers"
            if re.search(':', myLayer.layers):
                gsLayerNames.append(myLayer.layers)
            else:
                msLayerNames.append(myLayer.layers)
            continue

        try:
            if not myLayer.raster_legend is None:
                raster = True
            else:
                raster = False
        except:
            raster = False

        if raster:
            try:
                myUrl = myLayer.url + qs_separator + "service=WMS&version=1.1.0&request=GetFeatureInfo&layers=" + \
                    myLayer.layers + "&query_layers=" + myLayer.layers + "&bbox=" + \
                    theBoundingBox + "&srs=EPSG%3A900913&feature_count=1&x=" + thePixelX + \
                    "&y=" + thePixelY + "&height=" + theMapHeight + "&width=" + theMapWidth + \
                    "&info_format=text%2Fhtml&styles=" + myDateFilter
                logging.info(myUrl)
                try:
                    myResponse = urllib.urlopen(
                        myUrl, proxies=settings.PROXIES)
                    myRawResponse = myResponse.read()
                except Exception, E:
                    logging.info("Status: 500 Unexpected Error")
                    logging.info("Content-Type: text/plain")
                    logging.info(
                        "Some unexpected error occurred. Error text was: %s" % E)
                    myResponseHtml += myNoResponseHtml
                    continue
                logging.info(myRawResponse)
                legend_item_value = int(myRawResponse)
                if legend_item_value == 0:  # nodata
                    continue
                legend_item = RasterLegendItem.objects.get(
                    value=legend_item_value, legend=myLayer.raster_legend)
                # fill up the HTML table code flipping the table, filling up the header
                # first..
                myChunkHtml = ""
                # open HTML tags
                myChunkHtml += (
                    "<table><caption style=\"text-align: left;\">%s</caption>" % myLayer.name)
                myChunkHtml += ("<thead><tr>")
                myChunkHtml += ("<th>Description</th>")
                myChunkHtml += ("<th>Legend</th>")
                myChunkHtml += ("</tr></thead><tbody>")
                # ..then filling up the values rows
                myChunkHtml += ("<tr>")
                myChunkHtml += ("<td> %s </td>" % legend_item.description)
                myChunkHtml += ("<td style='color:#%s'>&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;</td>" % (
                    legend_item.rgb))
                myChunkHtml += ("</tr>")
                myChunkHtml += ("</tbody></table>")
                myResponseHtml += myChunkHtml
                myResponse.close()
                continue
            except:
                continue

        try:
            logging.info("Checking if this is a datequery layer")
            myDateQueryLayers = DateQueryLayer.objects.filter(owner=myUser).filter(id=myLayerId)
            logging.info("%s matched" % len(myDateQueryLayers))
            if len(myDateQueryLayers) > 0:
                    # Just use the first if there are duplicate names....
                myLayer = myDateQueryLayers[0]
                # myDateFilter =
                # "&FILTER=%3CFilter%3E%3CPropertyIsBetween%3E%3CPropertyName%3Eacqdatetime%3C%2FPropertyName%3E%3CLowerBoundary%3E%3CLiteral%3E"
                # + myLayer.start_date.isoformat()  +
                # "T00%3A00%3A00%3C%2FLiteral%3E%3C%2FLowerBoundary%3E%3CUpperBoundary%3E%3CLiteral%3E"
                # + myLayer.end_date.isoformat() +
                # "T00%3A00%3A00%3C%2FLiteral%3E%3C%2FUpperBoundary%3E%3C%2FPropertyIsBetween%3E%3C%2FFilter%3E"
                myDateFilter = "&cql_filter=date_timee DURING " + \
                    myLayer.start_date.isoformat(
                    ) + "Z/" + myLayer.end_date.isoformat() + "Z"
                # note the Z suffix is required for ISO8601 date format
                # compliance for geoserver.
        except Exception as e:
            logging.info("Error casting to date query layer: " + str(e))
            pass  # error is non critical as it may just be a normal wms layer

        if myLayer:
            myNoResponseHtml = "<table><caption style=\"text-align: left;\">%s</caption><thead><tr><th>No features found</th></tr></thead></table>" % myLayer.name

        # check if the layer scale range is a match for the V
        # current map scale - if not dont bother returning results
        theMapScale = float(theMapScale)
        logging.info("Min scale for layer %s is : %s" %
                     (myLayerName, myLayer.min_scale))
        logging.info("Max scale for layer %s is : %s" %
                     (myLayerName, myLayer.max_scale))
        logging.info("Map scale is : %s" % theMapScale)
        if (theMapScale < myLayer.min_scale) and (theMapScale > myLayer.max_scale):
            logging.info("Layer is within range for GFI query")
        else:
            logging.info("Layer is NOT within range for GFI query")
            continue

        logging.info("Getting feature info for %s" % myLayerName)
        # create the url
        myUrl = myLayer.url + qs_separator + "service=WMS&version=1.1.0&request=GetFeatureInfo&layers=" + \
            myLayer.layers + "&query_layers=" + myLayer.layers + "&bbox=" + \
            theBoundingBox + "&srs=EPSG%3A900913&feature_count=100&x=" + thePixelX + \
            "&y=" + thePixelY + "&height=" + theMapHeight + "&width=" + theMapWidth + \
            "&info_format=text%2Fplain&styles=" + myDateFilter
        logging.info(myUrl)
        try:
            myResponse = urllib.urlopen(myUrl, proxies=settings.PROXIES)
            myRawResponse = myResponse.read()
        except Exception, E:
            logging.info("Status: 500 Unexpected Error")
            logging.info("Content-Type: text/plain")
            logging.info("Some unexpected error occurred. Error text was: %s " % str(E))
            myResponseHtml += myNoResponseHtml
            continue
        logging.info(myRawResponse)
        if not myRawResponse.startswith("no features were found"):
            # split it on the feature to have a chunk containing a selfstanding
            # table
            myChunks = myRawResponse.split(
                "--------------------------------------------")
            # split it on the fields of each feature
            myChunkList = []
            for myChunk in myChunks:
                if " = " in myChunk:
                # chunk the response
                    myTrimmedResponse = {}
                    mySplittedResponse = myChunk.split("\n")
                    for token in mySplittedResponse:
                        if " = " in token:
                            # split the key-value pair and fill the dictionary
                            [k, v] = token.split(" = ")
                            myTrimmedResponse[k] = v
                    logging.info(myTrimmedResponse)
                    myChunkList.append(myTrimmedResponse)
            logging.info(myChunkList)

            # fill up the HTML table code flipping the table, filling up the header
            # first..
            myChunkHtml = ""
            for myChunkListItem in myChunkList:
                if myChunkListItem == myChunkList[0]:
                    # open HTML tags
                    myChunkHtml += (
                        "<table><caption style=\"text-align: left;\">%s</caption>" % myLayer.name)
                    myChunkHtml += ("<thead><tr>")
                    keys = myChunkListItem.keys()
                    keys.sort()
                    if 'the_geom' in keys: keys.remove('the_geom')
                    if 'geom' in keys: keys.remove('geom')
                    for key in keys:
                        if key[0] == '_':  # hidden columns
                            continue
                        regex = '^(#\d+#)?(?P<heading>.*)$'
                        heading = re.search(regex, key).groupdict()['heading']
                        myChunkHtml += ("<th>%s</th>" % heading)
                    myChunkHtml += ("</tr></thead><tbody>")
                # ..then filling up the values rows
                myChunkHtml += ("<tr>")
                for key in keys:
                    if key[0] == '_':  # hidden columns
                        continue
                    myChunkHtml += ("<td> %s </td>" % myChunkListItem[key])
                myChunkHtml += ("</tr>")
            if myChunkHtml != "":
                myChunkHtml += ("</tbody></table>")
                myResponseHtml += myChunkHtml
            else:
                myResponseHtml += myNoResponseHtml
        else:
            myResponseHtml += myNoResponseHtml
        try:
            myResponse.close()
        except Exception, E:
            logging.info("Error closing response from urllib")
            continue
        logging.info(myResponseHtml)

    myResponseHtml += """</div>"""  # closes feature-info div
    logging.info("Response 2: %s" % myResponseHtml)
    return HttpResponse(myResponseHtml)


def fireProtectionAgencySLD(theRequest):
    return render_to_response("sld.xml")


def setLayerVisibility(theRequest, theId, theFlag):
    """ When logged user changes visibility of a layer, the change is written
    down into the UserWmsLayer lookup table.
    Anonymous users don't have access to the table and won't save the layers' status. """
    myLayer = get_object_or_404(WmsLayer, id=theId)

    if theRequest.user.is_authenticated and theRequest.user.username is not "":
        myUserWmsLayer = UserWmsLayer.objects.get(
            wmslayer=myLayer, user=theRequest.user)
        if theFlag == "f":
            # save into lookup table
            myUserWmsLayer.is_visible = False
            myMessage = "%s will be hidden by default now" % myLayer
        else:
            myUserWmsLayer.is_visible = True
            myMessage = "%s will be shown by default now" % myLayer
        myUserWmsLayer.save()

    else:
        # the user is not logged in
        myMessage = "You are not logged in, the changes won't be saved."
    return HttpResponse(myMessage)


def saveLegend(theRequest, theId, theOrder, theDeletedState):
    """ Saves the relative position and deleted state of the layer in the legend. """
    myLayer = get_object_or_404(WmsLayer, id=theId)
    logging.info(myLayer.name)
    logging.info(theRequest.user)
    myUserWmsLayer = None
    # if the user layer already exists and is assigned to the user just update
    # its state
    try:
        myUserWmsLayer = UserWmsLayer.objects.get(
            wmslayer=myLayer, user=theRequest.user)
    except:
        myUserWmsLayer = UserWmsLayer()
        myUserWmsLayer.wmslayer = myLayer
        myUserWmsLayer.user = theRequest.user
        myUserWmsLayer.is_visible = True
        myUserWmsLayer.has_access = True
    # continue on to set the properties as passed to the view
    myUserWmsLayer.order = theOrder
    myResponse = ""
    if theDeletedState == "f":
        myUserWmsLayer.is_deleted = False
        myResponse = myUserWmsLayer.wmslayer.as_open_layer
        myVisibility = "false"
        if myUserWmsLayer.is_visible:
            myVisibility = "true"
        myResponse += "\ngMap.addLayer( %s );" % myUserWmsLayer.wmslayer.layerName(
        )
        myResponse += "\n%s.setVisibility( %s );" % (
            myUserWmsLayer.wmslayer.layerName(), myVisibility)
        logging.info(myResponse)
    else:
        myUserWmsLayer.is_deleted = True
    myUserWmsLayer.save()

    return HttpResponse(myResponse, mimetype='text/javascript')


def setLayerDeletedState(theRequest, theId, theDeletedFlag, theVisibleFlag):
    """ When logged user deletes a layer from the legend, the change is written down into the UserWmsLayer lookup table.
    Anonymous users don't have access to the table and won't save the layers' status. """

    myLayer = get_object_or_404(WmsLayer, id=theId)
    myUserWmsLayer = UserWmsLayer.objects.get(wmslayer=myLayer, user=theRequest.user)

    if theRequest.user.is_authenticated and theRequest.user.username is not "":
        if theDeletedFlag == "f":
            # save into lookup table
            myUserWmsLayer.is_deleted = False
            myUserWmsLayer.deleted_timestamp = None
            myMessage = "Layer (%s) is no longer deleted from the legend." % myLayer
        else:
            myUserWmsLayer.is_deleted = True
            myUserWmsLayer.deleted_timestamp = datetime.datetime.utcnow()
            myMessage = "Layer (%s) is now deleted from the legend." % myLayer
        myUserWmsLayer.save()

    else:
        # the user is not logged in
        myMessage = "You are not logged in, the changes won't be saved."
    return HttpResponse(myMessage)


def getPlaceNames(theRequest):
    """ Retrieves the place names and casts them in JSON format, to be passed to the
    autocompletion-javascript-combobox of Places dialog.
    Format required is (with completely bogus example lat lons):
    [{"id":"856","value":"Cape Town","lon":"34.32","lat":"24.3"},
     {"id":"1113","value":"Johannesburg","lon":"34.32","lat":"24.3"}
    ]
    """
    myFilter = theRequest.GET["term"]
    logging.info("Filtering on %s" % myFilter)
    myPlaceNames = PlaceName.objects.filter(
        name__istartswith=myFilter).order_by('name')[:10]
    places = []
    for myPlace in myPlaceNames:
        places.append('{"id":%d,"value":"%s","lon":"%s","lat":"%s" }' % (
            myPlace.id, myPlace.name, myPlace.position.x, myPlace.position.y))
    return HttpResponse('[' + ','.join(places) + ']', mimetype='application/json')


def dateQuery(request):
    """Handle a date query request. When the request comes in, we will
       use it to create a new user owned layer definition, and then
       refresh the legend on the map an add the new layer to the map.
       Doing it this way means that queries can be persisted and named
       by the user."""
    myPost = None
    myAnonymousFlag = False
    if (request.GET):
        myPost = request.GET
    if (request.POST):
        logging.info("Posted")
        myPost = request.POST
    if myPost:
        if request.user.is_authenticated and request.user.username is not "":
            myUser = request.user
        else:
            # Anonymous user - it populates [User]WmsLayer models but no other
            # way
            myUser = get_object_or_404(
                User, username=getAnonymousUser(request))
            myAnonymousFlag = True

        myName = myPost["name"]
        mySensor = get_object_or_404(Sensor, id=myPost["sensor"])
        myFormat = get_object_or_404(ImageFormat, name="png")
        myLegendGroup = get_object_or_404(LegendGroup, title="Date Queries")

        # Ensure the start date set to the beginning of the day
        myStartDate = datetime.datetime(*(list(time.strptime(
            myPost["start-date"], "%m/%d/%Y")[0:5]))).replace(hour=0, minute=0)
        # Ensure that end date is set to end of the day
        myEndDate = datetime.datetime(*(list(time.strptime(
            myPost["end-date"], "%m/%d/%Y")[0:5]))).replace(hour=12, minute=0)

        # to send back to the ui
        myDescription = "You have searched for %s data collected between %s and %s. The search results will be added to the map as a layer called %s" % (
            mySensor, myStartDate, myEndDate, myName)
        # to store in the layer model
        myLayerDescription = "%s data collected between %s and %s" % (
            mySensor, myStartDate, myEndDate)

        # Create a new datequery layer now
        myUrl = settings.AFIS_WMS_URL
        myLayer = DateQueryLayer()
        myLayer.start_date = myStartDate
        myLayer.end_date = myEndDate
        myLayer.url = myUrl
        myLayer.name = myName
        myLayer.sensor = mySensor
        myLayer.layers = mySensor.layer
        myLayer.owner = myUser
        myLayer.is_visible = False
        myLayer.is_backdrop_layer = False
        myLayer.is_transparent = True
        myLayer.image_format = myFormat
        myLayer.description = myLayerDescription
        myLayer.legend_style = mySensor.style
        myLayer.legend_group = myLegendGroup

        try:
            myLayer.save()

        except Exception, e:
            logging.info("Exception %s" % e)
            return HttpResponse("alert(\"Exception %s\");" % escapejs(str(e)))

        # save a UserWmsLayer as well, as it is the SPOT for legend population.
        #@FIXME anonymous users populate the model anyway and propagate changes to other nonlogged users.

        myNewUserWmsLayer = UserWmsLayer(user=myUser,
                                         wmslayer=myLayer,
                                         is_visible=True,
                                         is_deleted=False,
                                         has_access=True,
                                         order=0)
        # shift all layer pairs' order accordingly
        myUserWmsLayers = UserWmsLayer.objects.filter(user=myUser)
        for myUserWmsLayer in myUserWmsLayers:
            myUserWmsLayer.order = myUserWmsLayer.order + 1
            myUserWmsLayer.save()
        myNewUserWmsLayer.save()
        logging.info("Saving Layer")
        if myAnonymousFlag:
            mySessionLayers = request.session.get('queryLayers', False)
            if not mySessionLayers:
                # create a new session
                mySessionLayers = [myNewUserWmsLayer.id]
            else:
                mySessionLayers.append(myNewUserWmsLayer.id)
            request.session['queryLayers'] = mySessionLayers

        myResponse = """
                    $('#output').html("%s");
                    %s;
                    %s.setVisibility( true );
                    gMap.addLayer( %s );
                    $('#layers').load('/showLegend/');
                    """ % (
            myLayer.description,
            myLayer.as_open_layer,
            myLayer.layerName(),
            myLayer.layerName()
        )
        return HttpResponse(myResponse, mimetype='text/javascript')
    else:
        mySensors = Sensor.objects.all()
        return render_to_response("dateQuery.html", {'mySensors': mySensors})


def places(theRequest):
    """ Shows a dialog with list of South African relevant places to zoom into. """
    return render_to_response("places.html")


def baseLayerDialog(theRequest):
    """ Show a dialog to pick up one of the base layers. """
    return render_to_response("baseLayerDialog.html")


def uploadFeature(request):
    """ Let the user upload a polygon from a shapefile. Asks for a zipped shapefile and loads the first geometry. """
    # cosmetics
    formHtmlBegin = """<form enctype="multipart/form-data" action="" method="post" class="horizontal">"""
    formHtmlEnd = """<button type="submit">Load shapefile</button></form>"""

    if request.FILES:
        #@TODO the file size is (going to be) limited by Apache, using LimitRequestBody directive.
        ## the file type can be validated after upload.

        myForm = InputFileForm(request.POST, request.FILES)
        if not myForm.is_valid():
            # Redisplay it with validation messages
            return HttpResponse(formHtmlBegin + myForm.as_p() + formHtmlEnd)
        else:
            try:
                #@TODO move dimension check before download
                if myForm.cleaned_data['file'].content_type != "application/x-zip-compressed":
                    #@TODO: i18n of messages?
                    raise forms.ValidationError(
                        'Wrong format. Please select a ZIP archive.')
                if myForm.cleaned_data['file'].size > 1048576:  # 1MB
                    raise forms.ValidationError(
                        'File size exceeds limit of 1MB.')
                extractedGeometries = getFeaturesFromZipFile(
                    myForm.cleaned_data['file'], "Polygon", 1)

                mySearch = Search(owner=request.user,
                                  polygon=extractedGeometries[0],
                                  is_deleted=False)
                mySearch.save()
                return HttpResponse("The first polygon has been successfully uploaded into Search model.")

            except (forms.ValidationError, RuntimeError), e:
                #@FIXME ugly but logic.
                return HttpResponse(formHtmlBegin + myForm.as_p() + formHtmlEnd + str(e))

    else:
        # No files so make a new empty form
        myForm = InputFileForm()
        # Show the form in the users browser
        return HttpResponse(formHtmlBegin + myForm.as_p() + formHtmlEnd)
    # return a confirmation page. Better to come back to the list of layers,
    # TBD
    return HttpResponse("The extracted geometries are " + str(extractedGeometries))


def updateOpenLayerStrings(request):
    myObjects = WmsLayer.objects.all()
    for myObject in myObjects:
        myObject.save()
    myObjects = UserWmsLayer.objects.all()
    for myObject in myObjects:
        myObject.save()
    myObjects = DateQueryLayer.objects.all()
    for myObject in myObjects:
        myObject.save()
    return HttpResponse("OpenLayer defs updated")

from registration.signals import user_registered
from django.dispatch import receiver
from django.template.loader import render_to_string


@receiver(user_registered)
def email_new_user(sender, **kwargs):
    from django.core.mail import send_mail
    request = kwargs['request']
    user = kwargs['user']
    host = request.get_host()
    subject = render_to_string(
        'registration/registration_notification_email_subject.txt', {})
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string(
        'registration/registration_notification_email.txt',
        {'host': host, 'username': user.username})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


# create a user profile for the new user. this keeps users created on the
# viewer compatible with the alerts system. once a single registration
# portal is available this would not be needed.
@receiver(user_registered)
def create_new_user_profile(sender, **kwargs):
    user = kwargs['user']
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.timezone = 'Africa/Johannesburg'
    profile.save()


def get_wildcard_sub_domain_info(request):
    try:
        afis_host = request.get_host()
        regex = r"""(((?P<sub1>[^\.]+)\.)?(?P<sub0>[^\.]+)\.)?afis\..+"""
        match_obj = re.search(regex, afis_host)
        subdomain0 = match_obj.group('sub0')
        subdomain1 = match_obj.group('sub1')

        if subdomain0 in CUSTOM_WILDCARD_SUBDOMAIN_INFO:
            if subdomain1 in CUSTOM_WILDCARD_SUBDOMAIN_INFO[subdomain0]:
                json_str = ('{"success": true, "message": "Custom info as specified.", "info": %s}' %
                            CUSTOM_WILDCARD_SUBDOMAIN_INFO[subdomain0][subdomain1]).replace('\'', '"')
                return HttpResponse(json_str)
            elif '*' in CUSTOM_WILDCARD_SUBDOMAIN_INFO[subdomain0]:
                # Redirect subdomain0 to another subdomain lookup as specified
                subdomain0 = CUSTOM_WILDCARD_SUBDOMAIN_INFO[subdomain0]['*']

        cursor = connections['knownfeatures'].cursor()

        if len(subdomain0) == 2:
            # This is probably a HASC (Hierarchical Administrative Subdivision
            # Codes - http://www.statoids.com/ihasc.html)
            if subdomain1 is not None:
                # Country with primary subdivision HASC, ex: ZA.WC
                sql = "SELECT iso, name_0, name_1, ST_EXTENT(the_geom)::TEXT AS bbox, ST_AREA(ST_ENVELOPE(ST_COLLECT(the_geom))) AS area FROM gadm2 WHERE (NOT hasc_1 IS NULL OR NOT hasc_2 IS NULL) AND (hasc_1 ILIKE %(part0)s||'.'||%(part1)s OR hasc_2 ILIKE %(part0)s||'.'||%(part1)s) GROUP BY iso, name_0, name_1, hasc_1 ORDER BY area DESC;"
                params = {'part0': subdomain0, 'part1': subdomain1}
            else:
                # Country only HASC, ex: ZA
                sql = "SELECT iso, name_0, NULL::TEXT AS name_1, ST_EXTENT(the_geom)::TEXT AS bbox, ST_AREA(ST_ENVELOPE(ST_COLLECT(the_geom))) AS area FROM gadm2 WHERE (NOT hasc_1 IS NULL OR NOT hasc_2 IS NULL) AND (hasc_1 ILIKE %(part0)s||'.'||%(wildcard)s OR hasc_2 ILIKE %(part0)s||'.'||%(wildcard)s) GROUP BY iso, name_0 ORDER BY area DESC;"
                params = {'part0': subdomain0, 'wildcard': '%'}
        else:
            return HttpResponse('{"success": false, "message": "Only HASC supported. First subdomain length must be 2."}')

        cursor.execute(sql, params)
        row = cursor.fetchone()

        if row is None:
            json_str = '{"success": false, "message": "HASC lookup failed (not found)."}'
            return HttpResponse(json_str)

        cursor.close()

        iso = row[0]
        name_0 = row[1]
        name_1 = row[2]
        bbox_str = row[3]

        bounds_str = bbox_str.replace('BOX(', '').replace(
            ',', ' ').replace(')', '').split(' ')
        json_str = '{"success": true, "message": "HASC lookup success.", "info": {"west": %s, "south": %s, "east": %s, "north": %s}}' % tuple(
            bounds_str)
        return HttpResponse(json_str)
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = 'Caught %s in %s at line %d' % (
            exc_type, fname, exc_tb.tb_lineno)
        return HttpResponse('{"success": false, "message": "%s"}' % error)
