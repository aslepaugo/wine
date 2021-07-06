import collections
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas

from jinja2 import Environment, FileSystemLoader, select_autoescape


FOUNDATION_YEAR = 1920
WINE_CATALOGUE_FILE_PATH = 'catalogue/wine.xlsx'

def get_wine_catalogue(file_path):
    """
    Return a list of cards of wine from catalogue
    """
    wine_catalogue_df = pandas.read_excel(file_path, keep_default_na=False)
    wine_catalogue = wine_catalogue_df.to_dict('records')

    wine_catalogue_grouped = collections.defaultdict(list)
    for wine_card in wine_catalogue:
        wine_catalogue_grouped[wine_card['Категория']].append(wine_card)

    return dict(sorted(wine_catalogue_grouped.items()))


def get_age_years_ru() -> str:
    """
    Calculate difference between current year and foundation year
    then add year(s) in russian with declension
    """
    age = datetime.now().year - FOUNDATION_YEAR
    last_number = int(str(age)[-1])

    years_ru = 'лет'
    if last_number == 1:
        years_ru = 'год'
    elif last_number in range(2, 5):
        years_ru = 'года'

    return f"{age} {years_ru}"


def template_render() -> None:
    """
    Predefine variables and render landing age
    """
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    age_years_ru = get_age_years_ru()
    wine_cards = get_wine_catalogue(WINE_CATALOGUE_FILE_PATH)
    rendered_page = template.render(age_years_ru=age_years_ru, wine_cards=wine_cards)

    with open('index.html', 'w', encoding='utf8') as rendered_file:
        rendered_file.write(rendered_page)


if __name__ == '__main__':
    template_render()

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
