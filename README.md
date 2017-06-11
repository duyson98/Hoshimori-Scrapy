# ScrapyTutorial
Put spiders in \hoshimori\hoshimori\spiders

Crawl by executing "scrapy crawl '%spider's name%'" in \hoshimori

Output to file by executing "scrapy crawl '%spider's name%' -o '%filename%'" in \hoshimori

Run get_cardlist.py to get 3 lists, respectively of normal cards, extra cards, and subcards.

Run get_database.py after running get_cardlist.py to get all carddata in 3 files, respectively of normal cards, extra cards, and subcards. Needs rechecking as not all cards have the same format, which may lead to missing or wrong data / datafield.

Main is used for running scrapy directly from inside IDE instead of using terminal / CMD.