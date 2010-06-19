import sys
from optparse import OptionParser, make_option

from django.core.management.base import BaseCommand
from kong.models import Test
from kong.models import Site, Type, Server
from kong.utils import run_test, run_tests_for_type, run_tests_for_site, run_tests_for_box

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-a", "--all", dest="all", action="store_true"),
        make_option("--all-sites", dest="all-sites", action="store_true"),
        make_option("--all-types", dest="all-types", action="store_true"),
        make_option("-t", "--test", dest="test"),
        make_option("-s", "--site", dest="site"),
        make_option("-T", "--type", dest="type"),
        make_option("-b", "--box", dest="box"),
        make_option("-l", "--list", dest="list", action="store_true", default=False),
    )

    def handle(self, *args, **options):
        ALL = options.get('all')
        ALL_SITES = options.get('all-sites')
        ALL_TYPES = options.get('all-types')
        TEST = options.get('test')
        SITE = options.get('site')
        TYPE = options.get('type')
        BOX = options.get('box')
        LIST = options.get('list')

        passed =  True
        if ALL:
            #print "Running tests for all sites and types"
            all_passed = True
            for site in Site.objects.all():
                passed = run_tests_for_site(site)
                all_passed = passed and all_passed
            for type in Type.objects.all():
                passed = run_tests_for_type(type)
                all_passed = passed and all_passed
        elif ALL_SITES:
            for site in Site.objects.all():
                passed = run_tests_for_site(site)
        elif ALL_TYPES:
            for type in Type.objects.all():
                passed = run_tests_for_type(type)
        elif TEST:
            #print "Running test: %s" % TEST
            test = Test.objects.get(slug=TEST)
            passed = run_test(test)
        elif TYPE:
            #print "Running tests for type : %s" % TYPE
            type = Type.objects.get(slug=TYPE)
            passed = run_tests_for_type(type)
        elif SITE:
            #print "Running tests for site : %s" % SITE
            site = Site.objects.get(slug=SITE)
            passed = run_tests_for_site(site)
        elif BOX:
            #print "Running tests for box: %s" % BOX
            box = Server.objects.get(slug=BOX)
            passed = run_tests_for_box(box)
        elif LIST:
            print "All Sites:"
            for site in Site.objects.all():
                print site.slug
            print "All Tests:"
            for test in Test.objects.all():
                print test.slug
            print "All Boxes:"
            for server in Server.objects.all():
                print server.slug
        else:
            print "No action"
            return 0

        if passed:
            print "All Good"
            sys.exit(0)
        else:
            print "Tests Failed!"
            sys.exit(2)
