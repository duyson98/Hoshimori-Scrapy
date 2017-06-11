# -*- coding: utf-8 -*-

import re


class CardCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):
        if item['card_type'] != 'sub':
            item['character'] = re.split(u'\u3011|\uFF08', item['card_name'], flags=re.UNICODE)[1]
            item['event'] = re.split(u'\u3010|\u3011', item['card_name'], flags=re.UNICODE)[1]
        return item