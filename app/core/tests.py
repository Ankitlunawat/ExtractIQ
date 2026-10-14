from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import ExtractionJob,ExtractedRecord
from .scraper import parse_page,allowed

class ExtractionTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user("user")
        self.job=ExtractionJob.objects.create(owner=self.user,name="Capture",state="completed")
        ExtractedRecord.objects.create(job=self.job,title="Catalogue record",url="https://books.toscrape.com/catalogue/record",price=Decimal("12.50"),rating=4,available=True,fingerprint="x"*64)
    def test_owner_only_export_and_views(self):
        other=User.objects.create_user("other")
        self.client.force_login(other)
        self.assertEqual(self.client.get(f"/extractiq/{self.job.pk}/").status_code,404)
        self.client.force_login(self.user)
        self.assertContains(self.client.get(f"/extractiq/{self.job.pk}/"),"Catalogue record")
        output=self.client.get(f"/extractiq/{self.job.pk}/export/json/").json()
        self.assertEqual(output[0]["price"],"12.50")
        self.assertEqual(self.client.get(f"/extractiq/{self.job.pk}/export/xml/").status_code,404)
    def test_parser_and_source_allowlist(self):
        card='<article class="product_pod"><h3><a title="A record" href="catalogue/a">A</a></h3><p class="price_color">£12.50</p><p class="star-rating Four"></p><p class="availability">In stock</p></article>'
        rows,next_url,rejected=parse_page(card,"https://books.toscrape.com/")
        self.assertEqual(rows[0]["rating"],4);self.assertEqual(rejected,0)
        self.assertEqual(rows[0]["price"],"12.50")
        with self.assertRaises(ValueError):parse_page("<html></html>","https://books.toscrape.com/")
        with self.assertRaises(ValueError):allowed("https://example.com/")
        rows,_,rejected=parse_page(card.replace("£12.50","invalid"),"https://books.toscrape.com/")
        self.assertEqual(rejected,1);self.assertEqual(rows,[])
