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
    args = "scrapy crawl database_normal -o database_normal.xml"
    scrapy.cmdline.execute(argv=convert_arguments(args))

if  __name__ =='__main__':
    main()