from django.test import TestCase
from dashboard.models import UrlTable, Report
from datetime import datetime

class TestModels(TestCase):

    def test_url_table_creation(self):
        urlTable = UrlTable.objects.create()
        self.assertIsNotNone(urlTable)
    
    def test_url_table_get_url(self):
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com/',
            nhs_url = 'nhsurl.com',
            lad = 'Birmingham'
        )
        self.assertEqual(urlTable.get_url(), 'report.com')
    
    def test_url_table_str(self):
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            lad = 'Birmingham',
            postcode = '123456'
        )
        self.assertEqual(str(urlTable), 'gp, 123456')
    
    def test_report_creation(self):
        report = Report.objects.create()
        self.assertIsNotNone(report)
    
    def test_report_str(self):
        date_string = "2024-03-01 10:10:10"
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
            start_time = datetime.fromisoformat(date_string)
        )
        self.assertEqual(str(report), 'report.com (2024-03-01 10:10:10)')
