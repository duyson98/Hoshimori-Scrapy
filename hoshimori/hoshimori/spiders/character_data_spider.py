import scrapy


class CharacterDataSpider(scrapy.Spider):
    name = "character_data"
    allowed_domains = ["http://shinjugamine.tumblr.com"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'results/character_data.csv',
        'FEED_EXPORT_FIELDS': ['name',
                               'description',
                               'i_school_year',
                               'birthday',
                               'i_blood_type',
                               'extra_activity',
                               'catchphrase_1',
                               'catchphrase_2',
                               'height',
                               'weight',
                               'three_sizes',
                               'hobby_1',
                               'hobby_2',
                               'hobby_3',
                               'food_likes',
                               'food_dislikes',
                               'family',
                               'dream',
                               'ideal_1',
                               'ideal_2',
                               'ideal_3',
                               'pastime',
                               'destress',
                               'fav_memory',
                               'fav_phrase',
                               'secret',
                               ],
        'CONCURRENT_REQUESTS': 2,
    }

    start_urls = (
        'http://shinjugamine.tumblr.com/post/126079105160/amano-nozomi-cv-touyama-nao-a-trendsetter-who',
        'http://shinjugamine.tumblr.com/post/125582109325/narumi-haruka-cv-amamiya-sora-as-an-aspiring',
        'http://shinjugamine.tumblr.com/post/125821041925/wakaba-subaru-cv-sakura-ayane-a-versatile-and',
        'http://shinjugamine.tumblr.com/post/125660539695/',
        'http://shinjugamine.tumblr.com/post/125580657955/',
        'http://shinjugamine.tumblr.com/post/125582747130/',
        'http://shinjugamine.tumblr.com/post/135154522780/',
        'http://shinjugamine.tumblr.com/post/126702558600/',
        'http://shinjugamine.tumblr.com/post/125822517515/',
        'http://shinjugamine.tumblr.com/post/126407592025/',
        'http://shinjugamine.tumblr.com/post/126076378660/',
        'http://shinjugamine.tumblr.com/post/126248859870/',
        'http://shinjugamine.tumblr.com/post/125583671405/',
        'http://shinjugamine.tumblr.com/post/125819803955/',
        'http://shinjugamine.tumblr.com/post/134544190750/',
        'http://shinjugamine.tumblr.com/post/158995052005/kusunoki-asuha-middle-school-year-1-cv-tamura',
        'http://shinjugamine.tumblr.com/post/158994864565/mitsurugi-furan-cv-fukuhara-ayaka-the-widely',
        'http://shinjugamine.tumblr.com/post/158994536225/sakaide-mari-cv-senbongi-sayaka-with-a-pure',
        'http://shinjugamine.tumblr.com/post/158994160725/yakumo-itsuki-cv-hidaka-noriko-earnest-and',
    )

    @classmethod
    def parse(self, response):
        results = response.xpath('//*[@id="captions"]//text()').extract()

        yield {
            'name': results[0],
            'description': results[1],
            'i_school_year': results[3],
            'birthday': results[5],
            'i_blood_type': results[9],
            'extra_activity': results[11],
            'catchphrase_1': results[13],
            'catchphrase_2': results[15],
            'height': results[17],
            'weight': results[19],
            'three_sizes': results[21],
            'hobby_1': results[23],
            'hobby_2': results[25],
            'hobby_3': results[27],
            'food_likes': results[29],
            'food_dislikes': results[31],
            'family': results[33],
            'dream': results[35],
            'ideal_1': results[37],
            'ideal_2': results[39],
            'ideal_3': results[41],
            'pastime': results[43],
            'destress': results[45],
            'fav_memory': results[47],
            'fav_phrase': results[49],
            'secret': results[51],
        }
