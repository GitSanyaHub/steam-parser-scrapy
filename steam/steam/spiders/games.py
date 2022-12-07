import scrapy


class GameSpider(scrapy.Spider):
    name = "game_spider"

    start_urls =  [
        "https://store.steampowered.com/search?term=indi&page=1&ndl=1",
        "https://store.steampowered.com/search?term=indi&page=2&ndl=1",

        "https://store.steampowered.com/search?term=military&page=1&ndl=1",
        "https://store.steampowered.com/search?term=military&page=2&ndl=1",

        "https://store.steampowered.com/search?term=drive&page=1&ndl=1",
        "https://store.steampowered.com/search?term=drive&page=2&ndl=1"
        ]

    def parse(self, response):
        for link in response.css('a.search_result_row::attr(href)').getall():
            yield response.follow(link, callback=self.parse_game)

    ## тут просиходит основной процесс сбора информации:

    def parse_game(self, response):

        tags = response.css("div.glance_tags.popular_tags a::text").getall()
        for i in range(len(tags)):
            tags[i] = tags[i].strip()

        check_mac = ""
        check_win = ""
        check_linux = ""
        if response.css("span.platform_img.mac").get():
            check_mac = "mac "
        if response.css("span.platform_img.win").get():
            check_win = "win "
        if response.css("span.platform_img.linux").get():
            check_linux = "linux"

        if int(response.css("div.date::text").get()[-4:]) >= 2000:
            yield {
                "name": response.css('div.apphub_AppName::text').get(),
                "category": response.css('div.blockbg a::text')[1:].getall(),
                "count_reviews": response.css("div.summary_section span::text")[1:].get().split()[0][1:],
                "score": response.css("div.summary_section span::text").get(),
                "release_date": response.css("div.date::text").get(),
                "developer": response.css('div.dev_row a::text').get(),
                "popular_tags": tags,
                "price_without_black_friday": response.css("div.game_purchase_price::text").get().strip(),
                "price_black_friday": response.css("div.discount_final_price::text").get(),
                "game_area_platform": check_mac + check_win + check_linux
            }
