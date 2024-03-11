import scrapy
from urllib.parse import urljoin

class YelucrawlerSpider(scrapy.Spider):
    name = "yelucrawler"
    allowed_domains = ["www.yelu.in"]
    start_urls = ["https://www.yelu.in/category/pharmaceutical-manufacturers/city:ahmedabad"]

    def parse(self, response):
        # Scraping the current page
        company_page_urls = response.css('h4 a::attr(href)').getall()
        for link in company_page_urls:
            company_page_url = urljoin(response.url, link)
            yield response.follow(company_page_url, callback=self.parse_company_page)

        # Checking for pagination and following the next page
        next_page = response.css('a.pages_arrow[rel="next"]::attr(href)').get()
        if next_page:
            self.logger.info(f"\n\nGoing to {next_page}\n\n")
            yield response.follow(next_page, callback=self.parse)

    def parse_company_page(self, response):
        company_name = response.css('div.info div.label:contains("Company name") + b::text').get()
        
        print("\n\n\n")

        if company_name:
            self.logger.info(f"Company Name: {company_name.strip()}")

        mobile_number = response.css('div.info div.label:contains("Mobile phone") + div.text::text').get()
        phone_number = response.css('div.info div.label:contains("Phone number") + div.text::text').get()

        if mobile_number:
            self.logger.info(f"Mobile Number: {mobile_number}")

        if phone_number:
            self.logger.info(f"Phone Number: {phone_number}")
            
        print("\n\n")

        if company_name and (mobile_number or phone_number):
            yield {
                'company_name': company_name.strip(),
                'mobile_number': mobile_number.strip() if mobile_number else None,
                'phone_number': phone_number.strip() if phone_number else None,
                'company_url': response.url,
            }
