import scrapy


class QuotesSpider(scrapy.Spider):
    name = "recipes"

    def start_requests(self):
        urls = [
            # "https://www.goodhousekeeping.com/food-recipes/easy/a22735786/shrimp-boil-with-sausage-and-spinach-recipe/",
            "https://www.goodhousekeeping.com/dinner-recipes/"
            # "https://www.goodhousekeeping.com/food-recipes/easy/a19855090/ginger-pork-and-cucumber-salad-recipe/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'food-dinner-recipes.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


# import scrapy
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
#
#
# class RecipesSpider(scrapy.Spider):
#     name = "recipes"
#     start_urls = [
#         'https://www.goodhousekeeping.com/food-recipes/easy/',
#         'https://www.goodhousekeeping.com/food-recipes/healthy/g448/salmon-recipes/',
#         'https://www.goodhousekeeping.com/food-recipes/healthy/',
#         'https://www.goodhousekeeping.com/easy-soup-recipes/',
#         'https://www.goodhousekeeping.com/dinner-recipes/',
#         'https://www.goodhousekeeping.com/food-recipes/dessert/',
#         'https://www.goodhousekeeping.com/easy-chicken-recipes/'
#     ]
#
#
#
#     def parse(self, response):
#         catagory = response.css('title::text').extract_first()
#         for menu in response.css('a.full-item-image'):
#             href = menu.css('a:nth-child(1)').xpath('@href').extract_first()
#             url_list = href.split("/")
#             url_list[-2] = url_list[-2].capitalize()
#             url_list[-2] = url_list[-2].replace("-", " ")
#             if url_list[-3][0] == 'a':
#                 item = {}
#                 item['category'] = catagory
#                 item['name'] = url_list[-2]
#                 item['picture'] = menu.css('img').xpath('@data-src').extract_first()
#                 item['ingredients'] =[]
#
#
#                 url = 'https://www.goodhousekeeping.com' + href
#
#                 if url is not None:
#
#                     request = scrapy.Request(url, callback=self.parse_recipe_details,
#                                       meta={'item': item})
#
#                     yield request
#
#
#     def parse_recipe_details(self, response):
#
#
#         item = response.meta["item"]
#         serving = response.css('span.yields-amount::text').extract_first()
#         if len(serving) > 0:
#             serving = [int(s) for s in serving.split() if s.isdigit()]
#             item['servings'] = serving[0]
#
#         time = response.css('span.total-time-amount::text').extract()
#         if len(time) > 0:
#             hour = int(time[0].strip())
#             minute = int(time[1].strip())
#             item['time'] = {'hour': hour, 'minute': minute}
#
#
#         calories = response.css('span.cal-per-serv-amount::text').extract_first()
#         if calories:
#             item['cal/serv'] = int(calories.strip())
#
#         directions =  response.css('div.direction-lists li::text').extract()
#         if len(directions) > 0:
#             item['directions'] = directions
#
#         for ingredient in response.css('div.ingredient-item'):
#             amount = ingredient.css('span.ingredient-amount::text').extract_first()
#             description = ingredient.css('span.ingredient-description p::text').extract_first()
#             if amount and description:
#                 item['ingredients'].append({'amount': amount, 'description': description})
#             elif description:
#                 item['ingredients'].append({'description': description})
#
#
#
#
#         return item
