'''
Created on May 26, 2017

@author: Koko
'''
import scrapy.cmdline


def convert_arguments(str):
    splitted = str.split()
    for i in range(len(splitted)):
        if splitted[i][0] == "'":
            splitted[i] = splitted[i][1:-1]
    return splitted


def main():
    args = "scrapy shell http://zh.battlegirl.wikia.com/wiki/%E3%80%90%E3%82%AD%E3%83%83%E3%83%81%E3%83%B3%E3%80%91%E6%9C%9B(%E5%BE%A9%E5%88%BB)"
    scrapy.cmdline.execute(argv=convert_arguments(args))


if __name__ == '__main__':
    main()
