# -*- coding: utf-8 -*-

import re


class CardCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):
        if item['card_type'] != 'sub':
            event_split = re.split(u'\u3010|\u3011', item['card_name'], flags=re.UNICODE)
            item['character'] = re.split(u'\uFF08', event_split[2], flags=re.UNICODE)[0]
            item['event'] = event_split[1]
        for key in ['skill_combo', 'skill_damage', 'skill_range', 'skill_effect', 'skill_comment']:
            # Copy skill* field
            temp = item[key]
            item[key] = ""
            for substr in temp:
                item[key] = "%s%s\n" % (item[key], substr)
            item[key] = item[key].rstrip("\n")
        return item
