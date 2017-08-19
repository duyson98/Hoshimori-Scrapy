# -*- coding: utf-8 -*-

import re


class ZhWeaponCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):

        if item['weapon_type'] == (u'\u528d'):
            item['weapon_type'] = 0
        elif item['weapon_type'] == (u'\u77db'):
            item['weapon_type'] = 1
        elif item['weapon_type'] == (u'\u69cc'):
            item['weapon_type'] = 2
        elif item['weapon_type'] == (u'\u69cd'):
            item['weapon_type'] = 3
        elif item['weapon_type'] == (u'\u6756'):
            item['weapon_type'] = 4
        elif item['weapon_type'] == (u'\u528d\u69cd'):
            item['weapon_type'] = 5
        elif item['weapon_type'] == (u'\u96d9\u69cd'):
            item['weapon_type'] = 6

        # for key in ['weapon_image']:
        #     temp = item[key]
        #     item[key] = temp[(temp.find("W")):(temp.find("png")+3)]
            
        item['obtain_method'] = " ".join(item['obtain_method'])

        # Split item
        splitted = item['rhythm'].split(':')
        item['beat1'] = splitted[0]
        item['beat2'] = splitted[1]
        item['beat3'] = splitted[2]

        item['weapon_name'] = item['weapon_name'][0]

        if item['weapon_prototype'] != "":
            item['weapon_prototype'] = item['weapon_prototype'][0]

        # Multiple lines
        for key in ['main_effects', 'sub_effects', 'material']:
            temp = item[key]
            item[key] = ""
            for substr in temp:
                item[key] = "%s%s\n" % (item[key], substr)
            item[key] = item[key].rstrip("\n")

        for key in ['weapon_name', 'weapon_image', 'weapon_type',
                               'rarity', 'rhythm', 'beat1', 'beat2', 'beat3',
                               'basic_atk', 'max_atk', 'material', 'coins_required', 'obtain_method',
                               'main_effects', 'sub_effects', 'weapon_prototype']:
            if item[key] == u'\uff0d':
                item[key] = ""

        return item