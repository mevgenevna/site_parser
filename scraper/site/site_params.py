import requests
from parsel import Selector

START_URL = 'https://www.akc.org/dog-breeds/'

def parse(resp: requests.Response):
    sel = Selector(resp.text)

    breed_css = 'div[id="breed-type-card-"] a[class="d-block relative"]::attr(href)'
    tasks = [(url, parse_breed) for url in sel.css(breed_css).getall()]

    next_xpath = '//a[text()="Load More"]/@href'
    next_page = sel.xpath(next_xpath).get()
    if next_page:
        tasks.append((next_page, parse))

    return tasks


def parse_breed(resp: requests.Response):
    sel = Selector(resp.text)

    header = sel.css('.page-header')
    breed = {'name': header.css('h1::text').get().strip('\n ')}

    card = sel.css('.attribute-list')
    term = card.css('.attribute-list__term')
    desc = card.css('.attribute-list__description')

    breed_term = [x.get()[:-1] for x in term.css('span::text')]
    breed_desc = [x.get() for x in desc.css('span::text')]
    breed_params = {t: d for t, d in zip(breed_term, breed_desc)}
    breed.update(breed_params)

    return [breed]
