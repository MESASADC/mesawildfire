#! /usr/bin/env python
#
# Read raster2pgsql output from stdin and modify the INSERT statements
# to include additional custom fields
#
import sys
import os
from optparse import OptionParser
import re
import logging

help_text = """Modify raster2pgsql INSERT statements from STDIN to include additional columns+values
String values must be quoted explicitly, i.e. "'example string value'"
%prog column1 value1 ... [options, -h for details]"""

def main(argv=None):
    if argv is None:
        argv = sys.argv

    debuglevelD = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    defvals = {
        'field': 'rast',
    }
    parser = OptionParser(usage=help_text)
    parser.add_option("-f", "--field", dest="field", type="string", metavar='COLUMN',
        help="specify name of destination raster column, default is '%s'"%defvals['field'])
    parser.add_option("-d", "--delete", dest="delete", action="store_true",
        help="Delete before insert")
    parser.add_option("-m", "--meta", dest="meta", type="string", metavar='RASTER_META',
        help="Used in WHERE-clause for delete")
    parser.add_option("-l", "--loglevel", dest="debug", type="string", help="Verbosity %s"%debuglevelD.keys(), metavar='LOGLEVEL')
    parser.set_defaults(**defvals)
    (options, args) = parser.parse_args()
    if options.debug:
        if options.debug not in debuglevelD: raise AssertionError("Verbosity level must be one of: %s"%debuglevelD.keys())
        dbglvl = debuglevelD[options.debug]
    else:
        dbglvl = logging.WARNING
    logger = logging.getLogger(__name__)
    logger.setLevel(dbglvl)
    ch = logging.StreamHandler()
    ch.setFormatter( logging.Formatter('%(asctime)s %(lineno)d %(name)s %(funcName)s %(message)s') )
    ch.setLevel(dbglvl)
    logger.addHandler(ch)

    if len(args) == 0:
        parser.error("Requires at least one column-value pair")
    if len(args)%2:
        parser.error("Column-Value pair mismatch")
    clist = []
    vlist = []
    for i, arg in enumerate(args):
        if i%2 == 0:
            clist.append(arg)
        else:
            vlist.append(arg)
    clist.append(options.field)
    #
    # INSERT INTO "test"."w_ecmwf" ( rast ) VALUES ( ('...') )
    #
    pattern = re.compile(r'\(\s*"%s"\s*\)\s+VALUES\s*\(' % options.field)
    replacement = '( %s ) VALUES ( %s,' % (', '.join('"%s"'%c for c in clist), ', '.join(vlist))
    logger.debug('pattern: %s' % pattern)
    logger.debug('replacement: %s' % replacement)
    first_time = True
    for line in sys.stdin:
        m = re.search(r'^INSERT INTO\s+(\S+)', line, re.I)
        if m is None:
            print line,
        else:
            if first_time and options.delete:
                first_time = False
                sql_del = 'DELETE FROM %s WHERE %s' % (
                m.group(1),
                " AND ".join(
                    ['"%s" = %s'%(clist[i], vlist[i]) for i, c in enumerate(vlist)]
                ))
                if options.meta:
                    sql_del += ' AND ST_Metadata(rast) = %s' % options.meta
                print sql_del + ';'
            newline = pattern.sub(replacement, line, re.I)
            print newline,
    return 0

if __name__ == "__main__":
    sys.exit(main())
