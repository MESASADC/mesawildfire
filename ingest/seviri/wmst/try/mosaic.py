"""
Purpose:    Create a new GeoServer ImageMosaic Store from a pre-created mosaic
            zip file (with all meta-data), and/or add a new layer to it
Reference:  http://geoserver.geo-solutions.it/edu/en/rest/python_gsconfig.html
Requires:
    pip install gsconfig
Author:     dhohls@csir.co.za
Created:    2015-10-08 11:05:54
Updated:    2015-10-21 11:25:23
"""
# lib
import argparse
import logging
import os
import socket
import zipfile
# third party
from geoserver.catalog import Catalog, FailedRequestError, ConflictingDataError
from geoserver.support import DimensionInfo


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = os.getcwd() #os.path.dirname(os.path.realpath(__file__))
GEOSERVER = 'http://localhost:8080'
WORKSPACE = 'mesa'
STORE = "mesa"
MOSAIC_NAME = "mesaframes"


def _zip_granule(layer_file):
    zf_name = '/tmp/' + os.path.basename(layer_file) + '.zip'
    zf = zipfile.ZipFile(zf_name, mode='w')
    try:
        zf.write(layer_file)
    finally:
        zf.close()
    return zf.filename


def main(args):

    # print args
    data_path = args.path or DATA_PATH
    geo_server = args.geoserver or GEOSERVER
    mosaic_name = args.mosaic or MOSAIC_NAME
    new_layer = args.layer  # eg. '20091201.tif' or '20091201.zip'
    store_name = args.store or STORE
    workspace_name = args.workspace or WORKSPACE

    # access geoserver
    # TODO - in production usage, find another way to access username & password
    try:
        gs_catalog = Catalog("%s/geoserver/rest" % geo_server,
                             username="admin", password="geoserver") 
        ws = gs_catalog.get_workspace(workspace_name)
        if not ws:
            logger.error('Unable to access workspace: "%s"' % workspace_name)
            return
    except FailedRequestError, e:
        logger.error('Unable to access GeoServer.', exc_info=True)
        return
    except socket.error, e:
        logger.error('Unable to connect to GeoServer.', exc_info=True)
        return

    if mosaic_name:  # create mosaic
        try:
            upload_zip = os.path.join(data_path, "%s.zip" % mosaic_name)
            if not os.path.exists(upload_zip):
                logger.error('Unable to find file: "%s"' % upload_zip)
                return
            gs_catalog.create_imagemosaic(mosaic_name, upload_zip, workspace=ws)
            lyr = gs_catalog.get_layer(mosaic_name)
            logger.info('Mosaic "%s" has been created' % lyr.name)
            # a basic time dimension manager (simply lists all time entries)
            _time = DimensionInfo("time", "true", "LIST", None, "ISO8601", None)
            # time needs to be set up against the resource
            res = lyr.resource
            res.metadata = ({'dirName': '%s_%s' % (res.name, lyr.name),
                             'time': _time})
            gs_catalog.save(res)
            gs_catalog.save(lyr)
            logger.info('Mosaic "%s" has been updated with time entry' % 
                        lyr.name)
        except ConflictingDataError:
            logger.warn('Mosaic "%s" already exists!' % mosaic_name)

    if new_layer:  # update mosaic
        try:
            store = gs_catalog.get_store(store_name, workspace=ws)
            new_file = os.path.join(data_path, new_layer)
            if not os.path.exists(new_file):
                logger.error('Unable to find file: "%s"' % new_file)
                return
            new_filename, new_file_extension = os.path.splitext(new_file)
            # if not zipped, zip it
            if new_file_extension != ".zip":
                new_file = _zip_granule(new_file)
            gs_catalog.harvest_uploadgranule(new_file, store)
            logger.info('Added layer "%s" to %s' % (new_layer, store_name))
        except FailedRequestError, e:
            logger.error('Unable to access store: "%s"' % store_name,
                         exc_info=True)
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-g', '--geoserver',
        help="Full URL, with port, for GeoServer")
    parser.add_argument(
        '-p', '--path',
        help="Path for location of files to be used (default is current)")
    parser.add_argument(
        '-w', '--workspace',
        help="Name of workspace to be used")
    parser.add_argument(
        '-s', '--store',
        help="Name of store to be used")
    parser.add_argument(
        '-m', '--mosaic',
        help="Name of ImageMosaic corresponding to existing ZIP file")
    parser.add_argument(
        '-l', '--layer',
        help="Name of new layer to be added to existing mosaic")
    args = parser.parse_args()
    main(args)

