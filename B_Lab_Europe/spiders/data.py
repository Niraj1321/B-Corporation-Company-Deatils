from scrapy.cmdline import execute
import scrapy
import json
import re
import pandas as pd


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["bcorporation.eu"]
    start_urls = ["https://bcorporation.eu/"]

    # Regex to remove illegal Excel characters
    ILLEGAL_EXCEL_CHARS = re.compile(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]")

    # Request headers
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0'
    }

    # API params
    params = {
        "x-typesense-api-key": "eoWf8NTNsTFdaxcxNSuyaKAjLeV4T3F0",
    }

    # Request payload
    data = {
        "searches": [{
            "query_by": "name,description,websiteKeywords,countries,industry,sector,hqCountry,hqProvince,hqCity,hqPostalCode,provinces,cities,size,demographicsList",
            "exhaustive_search": True,
            "collection": "companies-production-en-us",
            "q": "*",
            "page": 1,
            "per_page": 250,
        }]
    }

    url = "https://94eo8lmsqa0nd3j5p.a1.typesense.net/multi_search"

    # Store all scraped data
    all_data = []

    def start_requests(self):
        """Initial request"""
        try:
            self.data['searches'][0]['page'] = 1

            url_with_params = f"{self.url}?x-typesense-api-key={self.params['x-typesense-api-key']}"

            yield scrapy.Request(
                url=url_with_params,
                method="POST",
                headers=self.headers,
                body=json.dumps(self.data),
                callback=self.parse,
                meta={"page_no": 1, "product_count": 0},
                dont_filter=True
            )
        except Exception as e:
            self.logger.error(f"Error in start_requests: {e}")

    def clean_excel_text(self, value):
        """Remove illegal Excel characters"""
        try:
            if isinstance(value, str):
                return self.ILLEGAL_EXCEL_CHARS.sub("", value)
            return value
        except Exception as e:
            self.logger.error(f"Error cleaning text: {e}")
            return value

    def parse(self, response, **kwargs):
        """Parse API response"""
        try:
            if response.status != 200:
                self.logger.error(f"Bad response: {response.status}")
                return

            page_no = response.meta.get('page_no', 1)
            product_cnt = response.meta.get('product_count', 0)

            self.logger.info(f"Fetched Page: {page_no}")

            json_dic = response.json()

            hits = json_dic.get('results', [{}])[0].get('hits', [])

            for dic in hits:
                try:
                    doc = dic.get("document", {})

                    # Convert timestamp to date
                    ts = doc.get("initialCertificationDateTimestamp")
                    cert_dt = pd.to_datetime(ts, unit="ms", errors="coerce") if ts else pd.NaT

                    self.all_data.append({
                        "name": doc.get("name", ""),
                        "isCertified": doc.get("isCertified", ""),
                        "latestVerifiedScore": doc.get("latestVerifiedScore", ""),
                        "industry": doc.get("industry", ""),
                        "sector": doc.get("sector", ""),
                        "size": doc.get("size", ""),
                        "hqCity": doc.get("hqCity", ""),
                        "hqProvince": doc.get("hqProvince", ""),
                        "hqCountry": doc.get("hqCountry", ""),
                        "hqPostalCode": doc.get("hqPostalCode", ""),
                        "cities": ", ".join(doc.get("cities", [])),
                        "provinces": ", ".join(doc.get("provinces", [])),
                        "countries": ", ".join(doc.get("countries", [])),
                        "demographicsList": ", ".join(doc.get("demographicsList", [])),
                        "websiteKeywords": doc.get("websiteKeywords", ""),
                        "description": doc.get("description", ""),
                        "initialCertificationDate": cert_dt.strftime("%Y-%m-%d") if pd.notna(cert_dt) else "",
                        "certifiedSince": cert_dt.strftime("%B %Y") if pd.notna(cert_dt) else "",
                    })

                    product_cnt += 1

                except Exception as inner_e:
                    self.logger.error(f"Error parsing record: {inner_e}")

            total_records = json_dic.get('results', [{}])[0].get('found', 0)

            self.logger.info(f"Total collected: {len(self.all_data)}")

            # Pagination logic
            if product_cnt < total_records:
                self.data['searches'][0]['page'] = page_no + 1

                url_with_params = f"{self.url}?x-typesense-api-key={self.params['x-typesense-api-key']}"

                yield scrapy.Request(
                    url=url_with_params,
                    method="POST",
                    headers=self.headers,
                    body=json.dumps(self.data),
                    callback=self.parse,
                    meta={"page_no": page_no + 1, "product_count": product_cnt},
                    dont_filter=True
                )

        except Exception as e:
            self.logger.error(f"Error in parse method: {e}")

    def closed(self, reason):
        """Executed when spider closes"""
        try:
            # Save JSON
            with open("Find_A-B_Corp_Data.json", "w", encoding='utf-8') as fp:
                json.dump(self.all_data, fp, indent=4)

            self.logger.info("JSON file saved successfully")

            # Convert to DataFrame
            df = pd.DataFrame(self.all_data)

            # Clean data
            df = df.applymap(self.clean_excel_text)
            df = df.drop_duplicates()
            df = df.fillna('')

            # Uppercase columns
            df.columns = df.columns.astype(str).str.upper()

            # Save Excel
            df.to_excel("Find_A-B_Corp_Data.xlsx", index=False, engine='openpyxl')

            self.logger.info("Excel file saved successfully")

        except Exception as e:
            self.logger.error(f"Error in closed method: {e}")


# Run spider
execute("scrapy crawl links".split())