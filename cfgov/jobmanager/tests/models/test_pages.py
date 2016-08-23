from django.core.exceptions import ValidationError
from mock import patch
from model_mommy import mommy
from unittest import TestCase

from jobmanager.models.django import JobCategory, Grade, Location
from jobmanager.models.pages import JobListingPage


class JobListingPageTestCase(TestCase):
    def setUp(self):
        self.division = mommy.make(JobCategory)
        self.grade = mommy.make(Grade)
        self.region = mommy.make(Location)

        page_clean = patch('jobmanager.models.pages.CFGOVPage.clean')
        page_clean.start()
        self.addCleanup(page_clean.stop)

    def prepare_job_listing_page(self, **kwargs):
        kwargs.setdefault('description', 'default')
        kwargs.setdefault('division', self.division)
        return mommy.prepare(JobListingPage, **kwargs)

    def test_clean_with_all_fields_passes_validation(self):
        page = self.prepare_job_listing_page()
        try:
            page.full_clean()
        except ValidationError:
            self.fail('clean with all fields should validate')

    def test_clean_without_description_fails_validation(self):
        page = self.prepare_job_listing_page(description=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_open_date_fails_validation(self):
        page = self.prepare_job_listing_page(open_date=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_close_date_fails_validation(self):
        page = self.prepare_job_listing_page(close_date=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_salary_min_fails_validation(self):
        page = self.prepare_job_listing_page(salary_min=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_salary_max_fails_validation(self):
        page = self.prepare_job_listing_page(salary_max=None)
        with self.assertRaises(ValidationError):
            page.full_clean()

    def test_clean_without_division_fails_validation(self):
        page = self.prepare_job_listing_page(division=None)
        with self.assertRaises(ValidationError):
            page.full_clean()
