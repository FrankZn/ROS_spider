# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RosSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PkgItem(scrapy.Item):
	name = scrapy.Field()
	url = scrapy.Field()
	distros = scrapy.Field()
	# distros
	crystal = scrapy.Field()
	bouncy = scrapy.Field()
	ardent = scrapy.Field()
	melodic = scrapy.Field()
	lunar = scrapy.Field()
	kinetic = scrapy.Field()
	indigo = scrapy.Field()

class DistroItem(scrapy.Item):
	distro = scrapy.Field()
	# Package Summary
	version = scrapy.Field()
	license = scrapy.Field()
	build_type = scrapy.Field()
	use = scrapy.Field()
	# Repository Summary
	checkout_URI = scrapy.Field()
	VCS_type = scrapy.Field()
	VCS_version = scrapy.Field()
	last_updated = scrapy.Field()
	dev_status = scrapy.Field()
	released = scrapy.Field()
	#
	desc = scrapy.Field()
	addtional_links = scrapy.Field()
	maintainers = scrapy.Field()
	authors = scrapy.Field()