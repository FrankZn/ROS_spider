import scrapy
from ROS_spider.items import PkgItem
from ROS_spider.items import DistroItem

class PkgSpider(scrapy.Spider):
	name = "packages"

	DISTROS = [
		'crystal', 'bouncy', 'melodic', 'lunar', 'kinetic', 'indigo'
	]

	start_urls = ['https://index.ros.org/packages/']

	def parse(self, response):
		table = response.xpath("//table[@class]")[0]
		rows = table.xpath('./tbody/tr')

		self.logger.info(response.url)

		urls = rows.xpath('./td[5]/a/@href').extract()
		# for url in urls:
		for url in urls[:10]:
			yield response.follow(url, callback=self.pkg_parse)

		next_url = response.xpath('//ul[@class="pagination pagination-sm"]/li/a/@href').extract()[-1]
		next_url = None			# DEBUG
		if next_url is not None:
			yield response.follow(next_url, callback=self.parse)

	def pkg_parse(self, response):
		self.logger.info(response.url)
		pkg = PkgItem()
		pkg['name'] = response.xpath('//ol[@class="breadcrumb"]/li[3]/text()').extract_first()
		pkg['url'] = response.url
		pkg['distros'] = response.xpath('//div[@id="distro-switch"]/label[contains(@class, "btn-primary")]/@data').extract()

		for distro in self.DISTROS:
			if distro in pkg['distros']:
				d = DistroItem()
				d['distro'] = distro

				overview = response.xpath('//div[@id=$id]', id=distro+'-overview')
				pkg_summary = overview.xpath('.//table')[0]
				repo_summary = overview.xpath('.//table')[1]

				# Package Summary
				d['version'] = pkg_summary.xpath('./tr[2]/td[2]/text()').extract_first().strip()
				d['license'] = pkg_summary.xpath('./tr[3]/td[2]/text()').extract_first().strip()
				d['build_type'] = pkg_summary.xpath('./tr[4]/td[2]/span/text()').extract_first().strip()
				d['use'] = pkg_summary.xpath('./tr[5]/td[2]/span/text()').extract_first().strip()

				# Repository Summary
				d['checkout_URI'] = repo_summary.xpath('./tr[1]/td[2]/a/text()').extract_first().strip()
				d['VCS_type'] = repo_summary.xpath('./tr[2]/td[2]/span/text()').extract_first().strip()
				d['VCS_version'] = repo_summary.xpath('./tr[3]/td[2]/span/text()').extract_first().strip()
				d['last_updated'] = repo_summary.xpath('./tr[4]/td[2]/span/text()').extract_first().strip()
				# d['dev_status'] = repo_summary.xpath('./tr[5]/td[2]/span/text()').extract_first().strip()
				d['released'] = repo_summary.xpath('./tr[6]/td[2]/span/text()').extract_first().strip()

				if d['released'] == 'UNRELEASED':
					self.logger.info(d)
					self.logger.info(pkg)

				pkg[distro] = d
			else:
				pkg[distro] = None

		yield pkg