# Hoshimori Project

This is a database processor for the main [project](https://github.com/kokonguyen191/Hoshimori-Project)

## How to use?

### Prerequisites

```
scrapy 1.4: https://doc.scrapy.org/en/latest/index.html
```

### Quick start

1. Delete all **.csv** files in *hoshimori/results/* first

2. There are three *get_XX.py* files in *hoshimori/*. Just run any of them to get the related database.
    - **get_database_dengeki.py**: Crawl card info in Japanese from [dengekionline](https://wiki.dengekionline.com/battlegirl/)
    - **get_database_zh.py**: Crawl card info in Chinese from [zh.battlegirl](https://zh.battlegirl.wikia.com/)
    - **get_stagedatabase.py**: Crawl stage info in Japanese from [dengekionline](https://wiki.dengekionline.com/battlegirl/)
  
3. Results are exported as **.csv** in *hoshimori/results/*

### Adding new spiders

Just add them to *hoshimori/hoshimori/spiders*

## Authors

* **[Koko191](https://github.com/kokonguyen191)** -  Main dev
* **[duyson98](https://github.com/duyson98)** - Minor collaborator

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
