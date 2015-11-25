# Django settings for the full AFIS Viewer web application

from afis_web_basic import *

import re

DEBUG = False

# Database queries for overpass info: pick up connection details from the environment
CMDLINE_FES = 'mysql --host=%(ORBITAL_FES_HOST)s --port=%(ORBITAL_FES_PORT)s --user=%(ORBITAL_FES_USER)s --password=%(ORBITAL_FES_PASS)s --database=%(ORBITAL_FES_DB)s --skip-column-names --batch -e '
CMDLINE_OPENAFIS = "env PGPASSWORD='%(OPENAFIS_PASS)s' psql -h localhost -d openafis -U %(OPENAFIS_USER)s -A -t -c "

# Used for fetching firestats
AFIS_WFS_URL = 'http://afis.meraka.org.za/geoserver/wfs'
AFIS_MAPSERVER_URL = 'http://afis.meraka.org.za/cgi-bin/mapserv'

# directory where to store cached fire stats
FIRE_ROOT = os.path.join(MEDIA_ROOT, 'fire_stats')
if not os.path.exists(FIRE_ROOT):
    os.makedirs(FIRE_ROOT) and os.chmod(FIRE_ROOT, 0777)

# Previous overpass datetime cache time-to-live, argument for timedelta()
FIRE_STATS_CACHE_TTL = dict(minutes=5)
# How to obtain overpass datetime for different URL hostnames
#   hostre: regular expression to match URL hostname
#   ext: cache file name extension
#   prev: query for update datetime from most recent overpass
#   next: query for expected datetime of next overpass
#   advert: contents for advertisement <div>
FIRE_STATS_MODIS = (
    {
        "hostre": re.compile("south.*africa", re.I),
        "ext": ".af",
        "prev": "SELECT MAX(ts) FROM (SELECT MAX(obs_time_stamp) AS ts FROM af_modis UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_npp_master) AS subquery",
        "next": "SELECT FROM_UNIXTIME(los_epoch) FROM PassPrediction WHERE max_el > 5.100000 AND Satellite_idSatellite IN (1, 2, 132) AND los_epoch > unix_timestamp(NOW()) ORDER BY los_date LIMIT 1;",
        # Hack to add an additional checkbox for Next Overpass Swath layer
        # wmslayer id hardcoded must also correspond to code in afis.js
        "advert": """
<form style='display:inline;' action=""><input id="layer-2879-checkbox-2" class="ui-state-default ui-corner-all layer-checkbox" type="checkbox" style='display:inline' name="Next satellite overpass coverage">Next satellite overpass coverage</input></form>
""",
    },
    {
        "hostre": re.compile("europe", re.I),
        "ext": ".eu",
        "prev": "SELECT MAX(obs_time_stamp) FROM af_modis_dundee",
        "advert": """<a href="http://www.sat.dundee.ac.uk/" target="_new">MODIS data provided by NEODAAS</a>""",
    },
    {
        "hostre": re.compile("northamerica", re.I),
        "ext": ".us",
        "prev": "SELECT MAX(obs_time_stamp) FROM af_modis_master WHERE source = 'W'"
    },
    {
        "hostre": re.compile("demo\."),
        "ext": ".demo",
        "next": "SELECT FROM_UNIXTIME(los_epoch) FROM PassPrediction WHERE max_el > 5.100000 AND Satellite_idSatellite IN (1, 2, 132) AND los_epoch > unix_timestamp(NOW()) ORDER BY los_date LIMIT 1;",
        "prev": "SELECT MAX(ts) FROM (SELECT MAX(obs_time_stamp) AS ts FROM af_modis UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_modis_dundee UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_modis_master UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_npp_master) AS subquery",

    },
    {
        "hostre": re.compile(".*"),
        "ext": ".any",
        "prev": "SELECT MAX(ts) FROM (SELECT MAX(obs_time_stamp) AS ts FROM af_modis UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_modis_dundee UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_modis_master UNION ALL SELECT MAX(obs_time_stamp) AS ts FROM af_npp_master) AS subquery",

    },
)
# Build complete command lines
for dic in FIRE_STATS_MODIS:
    if "next" in dic:
        dic["next"] = '%s "%s"' % (CMDLINE_FES, dic["next"])
    if "prev" in dic:
        dic["prev"] = '%s "%s"' % (CMDLINE_OPENAFIS, dic["prev"])


# Sub-domain wildcards
CUSTOM_WILDCARD_SUBDOMAIN_INFO = { 
  'us' : { None: { 'west': -130.0, 'south': 25.0, 'east': -70.0, 'north': 50.0 } }, 
  'uk' : { None: { 'west': -9.0, 'south': 49.0, 'east': 2.0, 'north': 59.0 }, 
           '*': 'gb',  # This maps *.uk.afis.co.za to *.gb.afis.co.za
         }, 
  'ru' : { None: {"west": 22.0, "south": 41.0, "east": 180, "north": 82.0} }, 
  'ca' : { None: {"west": -141.0, "south": 41.0, "east": -53.0, "north": 70.0} }, 

  }


GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-31934220-1'
TRACK_MULTIPLE_DOMAINS = True
GOOGLE_ANALYTICS_SITE_SPEED = True
