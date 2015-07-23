#!/usr/bin/env python
# -*- coding: utf-8 -*-


from shapely.geometry import Point, Polygon, box
import shapely.wkt as wkt
from collections import OrderedDict
import itertools
import re

__all__ = ['GeoRK', 'getGeoRKSet']

class GeoRK(object):
    
    seperator = '.'
    wildcard_single = '*'
    wildcard_multi = '#'
    w_dot_w = wildcard_single + seperator + wildcard_single
    valid = [seperator, wildcard_single, wildcard_multi, '0', '1', '2', '3']

    def _clean_rk(self, rk):
        if rk == '':
            rk = self.w_dot_w
        rk = re.sub(r'^\*\.\*\.', '', rk)
        rk = re.sub(r'\.\*\.\*', '', rk)
        assert(self._is_valid_rk(rk))
        return rk
    
    def _is_valid_rk(self, rk):
        if rk == '':
            return True
        for s in rk.split('.'):
            if not s in self.valid:
                print 'Invalid: %s' % rk
                return False
        return True
    
    def __init__(self, rk):
        self._rk = self._clean_rk(rk)
    
    def _bits(self):
        rk = self._clean_rk(self._rk)
        rklist = rk.split(self.seperator)
        bits = [ str(item) for item in rklist]
        return bits[0::2], bits[1::2]
        
    def to_string(self, depth=None):
        depth = depth or self.depth
        hb = self._bits()[0][:depth]
        vb = self._bits()[1][:depth]
        hb = hb + list(itertools.repeat(None, depth - len(hb)))
        vb = vb + list(itertools.repeat(None, depth - len(vb)))
        values = [ (v or '*') for v in list(itertools.chain(*zip(hb, vb))) ]
        rk = '.'.join(values)
        return rk
    
    def __str__(self):
        return self.to_string()
        
    @property
    def point(self):
        h, v = self._bits()
        x = y = 0.
        dx = 45.
        dy = 45.
        # first digit in [0, 1, 2, 3] to cover full range -180 to 180
        first = True
        for hv in zip(h, v):
            if hv[0] == '0':
                x = -135. if first else x - dx 
            elif hv[0] == '1':
                print x
                x = -45. if first else x + dx
                print x
            elif first and hv[0] == '2':
                x = 45.
            elif first and hv[0] == '3':
                x = 135.
            elif hv[0] == '*':
                x = x
            else:
                raise ValueError('Expected * or 0 or 1, found %s' % hv[0])
            first = False
            if hv[1] == '0':
                y = y - dy
            elif hv[1] == '1':
                y = y + dy
            elif hv[1] == '*':
                y = y
            else:
                raise ValueError('Expected * or 0 or 1, found %s' % hv[1])
            dx = dx / 2
            dy = dy / 2
            print x, y, dx, dy, hv
        return Point(x, y)

    @property
    def depth(self):
        #print 'rk: "%s"' % self._clean_rk(self._rk)
        if self._clean_rk(self._rk) == self.w_dot_w:
            depth = 0
        else:
            depth = max(len(self._bits()[0]), len(self._bits()[1])) 
        return depth
    
    @property
    def bbox(self):
        dx = 180./2
        dy = 90.
        depth = self.depth
        x = self.point.x
        y = self.point.y
        #print depth, x, y
        #print x,y, dx / 2**(depth), dy / 2**(depth)
        minx = x - dx / 2**(depth)
        maxx = x + dx / 2**(depth)
        miny = y - dy / 2**(depth)
        maxy = y + dy / 2**(depth)
        #print minx, miny, maxx, maxy
        return minx, miny, maxx, maxy

    @property
    def polygon(self):
        return box(*self.bbox)
        
    def appending(self, h,v):
        rk = self._clean_rk(self.to_string()())
        rk = '%s.%s.%s' % (rk, h, v)
        rk = self._clean_rk(rk)
        return rk

id_ = 0

def getGeoRKSet(polygon, rk = GeoRK(''), depth=20):
    global id_
   
    # if this RK is at the maximum depth, simply return it
    if rk.depth >= depth:
        #print "max depth reached"
        yield rk
    else:
        # if the GeoRK is wholly contained in the target
        # polygon, we need look no further:  all of its 
        # children will also be wholly contained, because
        # they nest
        if polygon.contains(rk.polygon):
            #print "fully contained"
            yield rk
        else:
            #print "check children"
            # recurse into all children that intersect the
            # query polygon, but start with the child whose
            # centroid is closer to that of the target
            # TODO: doing on dimention at a time may lead to further optimization
            child1 = GeoRK(rk.appending('0','0'))
            child2 = GeoRK(rk.appending('0','1'))
            child3 = GeoRK(rk.appending('1','0'))
            child4 = GeoRK(rk.appending('1','1'))
            for child in [child1, child2, child3, child4]:
                #print "checking child: %s" % child.rk 
                if polygon.intersects(child.polygon):
                    #print 'polygon intersects child'
                    for rk in getGeoRKSet(polygon, child, depth):
                        #print "yielding from child"
                        yield rk


def getPointRK(lon,lat, depth=20):
    dx = 90./2
    dy = 90./2
    x = 0.
    y = 0.
    rk = ''
    assert(type(lon) == float)
    assert(type(lat) == float)
    print 'lon,lat: %d, %d' % (lon,lat)
    # first longitude digit in [0,1,2,3] to account for unsymetric dimensions  
    west = None
    if lon < 0.:
        x = -90.
        west = True
    else:
        x = 90.
        west = False
    if lon < x:
        x = x - dx 
        rk = '0' if west else '2'
    else:
        x = x + dx 
        rk = '1' if west else '3'
    print 'rk:', rk, '       x,y: %0.2f, %0.2f' % (x, y)    
    # now for the rest
    for i in range(depth):
        if i != 0:
            if lon < x:
                x = x - dx/2**i
                rk = rk + '.0'
            else:
                x = x + dx/2**i
                rk = rk + '.1'
        if lat < y:
            y = y - dy/2**i
            rk = rk + '.0'
        else:
            y = y + dy/2**i
            rk = rk + '.1'
        print 'rk:', rk, '       x,y: %0.2f, %0.2f' % (x, y)    
    
    return rk
    
    



schema = {'geometry': 'Polygon', 'properties': OrderedDict([(u'id', 'int:10')])}
crs = {'init': u'epsg:4326'}


record_template = {'geometry': {'coordinates': [],
  'type': 'Polygon'},
 'id': None,
 'properties': {u'id': None},
 'type': 'Feature'}


def process_feature(feature):
    #return True
    #return feature.get('properties').get('NAME') == 'South Africa'
    return feature.get('properties').get('NAME') == 'Namibia'


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        depth=int(sys.argv[2])
        import fiona
        with fiona.open(sys.argv[1], 'r') as source:
            source_ = source
            for f in source:
                print 'Feature:', f['id'], f['properties']['NAME']
                if process_feature(f):
                    georks = []
                    g = f['geometry']
                    if g['type'] in ['Polygon', 'MultiPolygon']:
                        target = fiona.open('rk/%s.shp' % f['properties']['NAME'], 'w', driver='ESRI Shapefile', schema=schema, crs=crs)
                        txt = open('rk/%s.txt' % f['properties']['NAME'], 'w')
                        polygons = []
                        if g['type'] == 'MultiPolygon':
                            for p in g['coordinates']:
                                polygons.append(Polygon(p[0]))
                        elif g['type'] == 'Polygon':
                            polygons.append(Polygon(g['coordinates'][0]))
                        else:
                            print g['type'] 
                        for polygon in polygons:
                            for rk in getGeoRKSet(polygon, depth=depth):
                                if rk.to_string(depth) in georks:
                                    continue
                                georks.append(rk.to_string(depth))
                                coords = list(rk.polygon.exterior.coords)
                                record = record_template
                                record['geometry']['coordinates'] = [coords]
                                record['id'] = id_
                                record['properties']['id'] = id_
                                record['properties']['name'] = f['properties']['NAME']
                                target.write(record)
                                txt.write('%s\n' % rk.to_string(depth))
                                print id_, rk.to_string(depth), rk.bbox
                                id_ += 1                             
                        target.flush()
                        target.close()
                        txt.flush()
                        txt.close()
                    else:
                        print g['type'] 
    elif len(sys.argv) > 1:
        lon, lat, depth = sys.argv[1].split(':')
        lon = float(lon)
        lat = float(lat)
        depth = int(depth)
        
        point_rk = getPointRK(lon, lat, depth) 
        print '-----------------------------'
        print point_rk
        geo_rk = GeoRK(point_rk)
        print geo_rk
        print 'POINT: %0.7f, %0.7f' % (geo_rk.point.x, geo_rk.point.y)
    else:
        rk = GeoRK('0.0.0.0.0.1.0.0.0.1.0.1.0.0.0.1.0.0.0.0')
        print rk.polygon.bounds[2] - rk.polygon.bounds[0], rk.polygon.bounds[3] - rk.polygon.bounds[1]
