#!/usr/bin/env python
import pygeoip
import logging
import os
import validators
import sys


'''
 Available methods:
     get_country() - returns name,abbr(short name)
     get_asn() - returns name, number
     get_city() - returns name 
  
'''

# setup logging
logging.basicConfig(stream=sys.stdout,level=logging.INFO)
logger = logging.getLogger('site-response')

class Geoip_mapping():

    def __init__(self,country_db=None,city_db=None, asn_db=None):

        #self.city_db = os.path.join(os.path.sep,os.getcwd(),'GeoLiteCity.dat')
        self.country_db = country_db
        self.city_db = city_db
        self.asn_db = asn_db
        self.geocountry_instance = None
        self.geocity_instance = None
        self.geoasn_instance = None

        # setup geoip instances for country,city and asn
        self._setup_geodb() 

    def _setup_geodb(self):
        try: 

            if not os.path.isfile(self.country_db):
                logger.info("""GeoIP Country database - {} could not be found in the current directory. 
                Please download it from the location -
                http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz""".format(self.country_db))
            else:
                self.geocountry_instance = pygeoip.GeoIP(self.country_db) 

            if not os.path.isfile(self.city_db):
                logger.info("""GeoIP City database - {} could not be found. 
                    Please download it from the location -
                    http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz""".format(self.city_db))
            else:
                self.geocity_instance = pygeoip.GeoIP(self.city_db)   
    
            if not os.path.isfile(self.asn_db):
                logger.info("""GeoIP ASN database - {} could not be found.  
                    Please download it from the location - 
                    http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz""".format(self.asn_db))
            else: 
                self.geoasn_instance = pygeoip.GeoIP(self.asn_db)   

            #return self.geocountry_instance, self.geocity_instance, self.geoasn_instance

        except Exception, exc:
            logger.error("Error while setting up geoip databases - %s" % exc.message,exc_info=True)


    def find_country(self,ip):

        country_name = country_code = None
 
        if validators.ip_address.ipv4(ip) and self.geocountry_instance:
            country_name = self.geocountry_instance.country_name_by_addr(ip)
            country_code = self.geocountry_instance.country_code_by_addr(ip)
            return country_name, country_code
        else:
            return None, None

    def find_city(self,ip):

        city_name = None
        city_latitude = None
        city_longitude = None

        if validators.ip_address.ipv4(ip) and self.geocity_instance:
            city_info = self.geocity_instance.record_by_addr(ip)
            city_name = city_info.get('city','')
            city_longitude = city_info.get('longitude','')
            city_latitude = city_info.get('latitude','')

            return city_name,city_longitude,city_latitude
        else:
            return None, None, None

    def find_asn(self,ip):

        asn_name = None

        if validators.ip_address.ipv4(ip) and self.geoasn_instance:
            asn_name = self.geoasn_instance.asn_by_addr(ip)
        return asn_name 

     
