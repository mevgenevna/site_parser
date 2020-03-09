from scraper import engine
from scraper.site import site_params


def execute(args):
    engine.start(site_params.START_URL, site_params.parse, args.outfile, args.format)