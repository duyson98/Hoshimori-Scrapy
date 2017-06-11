# -*- coding: utf-8 -*-

import re


class CardCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):
        if item['card_type'] != 'sub':
            item['character'] = re.split('】|（', item['card_name'])
            item['event'] = re.split('【|】', item['card_name'])
        return item