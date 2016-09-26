from __future__ import print_function

import importlib
import re

from django.apps import apps
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.test import RequestFactory
from django.test.runner import DiscoverRunner
from mock import Mock

from scripts import initial_data


class TestDataTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        dbs = super(TestDataTestRunner, self).setup_databases(**kwargs)

        # Ensure that certain key data migrations are always run, even if
        # tests are being run without migrations, e.g. through use of
        # settings.test_nomigrations.
        self.run_required_data_migrations()

        # Set up additional required test data that isn't contained in data
        # migrations, for example an admin user.
        initial_data.run()

        return dbs

    def run_required_data_migrations(self):
        migration_methods = (
            (
                'wagtail.wagtailcore.migrations.0002_initial_data',
                'initial_data'
            ),
            (
                'wagtail.wagtailcore.migrations.0025_collection_initial_data',
                'initial_data'
            ),
            (
                'v1.migrations.0009_site_root_data',
                'create_site_root'
            ),
        )

        loader = MigrationLoader(connection)
        for migration, method in migration_methods:
            if not self.is_migration_applied(loader, migration):
                print('applying migration {}'.format(migration))
                module = importlib.import_module(migration)
                getattr(module, method)(apps, None)

    @staticmethod
    def is_migration_applied(loader, migration):
        parts = migration.split('.')
        migration_tuple = (parts[-3], parts[-1])
        return migration_tuple in loader.applied_migrations


class HtmlMixin(object):
    def assertHtmlRegexpMatches(self, s, r):
        s_no_right_spaces = re.sub('>\s*', '>', s)
        s_no_left_spaces = re.sub('\s*([<"])', r'\1', s_no_right_spaces)
        s_no_extra_spaces = re.sub('\s+', ' ', s_no_left_spaces)

        self.assertIsNotNone(
            re.search(r, s_no_extra_spaces.strip(), flags=re.DOTALL),
            '{} did not match {}'.format(s_no_extra_spaces, r)
        )

    def assertPageIncludesHtml(self, page, s):
        request = RequestFactory().get('/')
        request.user = Mock()

        rendered_html = page.serve(request).render()
        try:
            self.assertHtmlRegexpMatches(str(rendered_html), s)
        except AssertionError:
            self.fail('rendered page HTML did not match {}'.format(s))
