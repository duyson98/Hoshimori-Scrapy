# -*- coding: utf-8 -*-

import re


class ZhCardCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):

        # Images
        # for key in ['image', 'special_icon', 'art', 'special_front', 'front_top', 'front_bottom', 'front_name', 'front_rarity', 'front_weapon']:
        #     temp = item[key]
        #     item[key] = temp[(temp.find("Card")):(temp.find("png")+3)]

        # if item['image_7'].find("Card_icn_wp") == -1:
        #     for num in range(6, 0, -1):
        #         temp = item['image_{}'.format(num)]
        #         if temp.find("Card_icn_wp") != -1:
        #             item['image_7'] = temp
        #             item['image_{}'.format(num)] = ""
        #             break
        #
        # if item['image_6'].find("Card_icn_rarity") == -1:
        #     for num in range(6, 0, -1):
        #         temp = item['image_{}'.format(num)]
        #         if temp.find("Card_icn_rarity") != -1:
        #             item['image_6'] = temp
        #             item['image_{}'.format(num)] = ""
        #             break
        #
        # if item['image_5'].find("Card_name") == -1:
        #     for num in range(5, 0, -1):
        #         temp = item['image_{}'.format(num)]
        #         if temp.find("Card_name") != -1:
        #             item['image_5'] = temp
        #             item['image_{}'.format(num)] = ""
        #             break
        #
        # if item['image_4'].find("Card_fr_bottom") == -1:
        #     for num in range(4, 0, -1):
        #         temp = item['image_{}'.format(num)]
        #         if temp.find("Card_fr_bottom") != -1:
        #             item['image_4'] = temp
        #             item['image_{}'.format(num)] = ""
        #             break
        #
        # if item['image_3'].find("Card_fr_top") == -1:
        #     for num in range(3, 0, -1):
        #         temp = item['image_{}'.format(num)]
        #         if temp.find("Card_fr_top") != -1:
        #             item['image_3'] = temp
        #             item['image_{}'.format(num)] = ""
        #             break
        #
        # if item['image_2'].find("Card_fr") != -1:
        #     for num in range(2, 0, -1):
        #         temp = item['image_{}'.format(num)]
        #         if temp.find("Card_fr") != -1:
        #             item['image_2'] = temp
        #             break
        #
        # if item['image_0'].find("Card_icn_wp_0") == -1:
        #     item['image_1'] = item['image_0']
        #
        # item['image_0'] = ""
        #
        # # Weapon type
        # if item['weapon_type'] == (u' \u528d'):
        #     item['weapon_type'] = "Sword"
        # elif item['weapon_type'] == (u' \u77db'):
        #     item['weapon_type'] = "Spear"
        # elif item['weapon_type'] == (u' \u69cc'):
        #     item['weapon_type'] = "Hammer"
        # elif item['weapon_type'] == (u' \u69cd'):
        #     item['weapon_type'] = "Gun"
        # elif item['weapon_type'] == (u' \u6756'):
        #     item['weapon_type'] = "Rod"
        # elif item['weapon_type'] == (u' \u528d\u69cd'):
        #     item['weapon_type'] = "Gun-blade"
        # elif item['weapon_type'] == (u' \u96d9\u69cd'):
        #     item['weapon_type'] = "Double-pistol"
        #
        # # Star
        # if item['rarity'] == (u'\u2605'):
        #     item['rarity'] = 1
        # elif item['rarity'] == (u'\u2605\u2605'):
        #     item['rarity'] = 2
        # elif item['rarity'] == (u'\u2605\u2605\u2605'):
        #     item['rarity'] = 3
        # elif item['rarity'] == (u'\u2605\u2605\u2605\u2605'):
        #     item['rarity'] = 4
        #
        # # Event
        # temp = item['card_name']
        # item['event'] = temp[(temp.index(u'\u3010')+1):temp.index(u'\u3011')]
        # if item['event'] == (u'\u30b5\u30d6\u30ab\u5c02\u7528'):
        #     item['event'] = ""
        #
        # # Character
        # temp = item['card_name']
        # if item['event'] != (u'\u30b5\u30d6\u30ab\u5c02\u7528'):
        #     if temp.find(u'(') != -1 and temp.find(u'\u4e2d1') == -1:
        #         item['character'] = temp[(temp.index(u'\u3011')+1):(temp.index(u'('))]
        #     else:
        #         item['character'] = temp[(temp.index(u'\u3011') + 1):]
        #
        # if item['character'] == u'\u307f\u304d':
        #     item['character'] = "Hoshitsuki Miki"
        # elif item['character'] == u'\u6634':
        #     item['character'] = "Wakaba Subaru"
        # elif item['character'] == u'\u9065\u9999':
        #     item['character'] = "Narumi Haruka"
        # elif item['character'] == u'\u671b':
        #     item['character'] = "Amano Nozomi"
        # elif item['character'] == u'\u3086\u308a':
        #     item['character'] = "Himukai Yuri"
        # elif item['character'] == u'\u304f\u308b\u307f':
        #     item['character'] = "Tokiwa Kurumi"
        # elif item['character'] == u'\u3042\u3093\u3053':
        #     item['character'] = "Tsubuzaki Anko"
        # elif item['character'] == u'\u84ee\u83ef':
        #     item['character'] = "Serizawa Renge"
        # elif item['character'] == u'\u660e\u65e5\u8449':
        #     item['character'] = "Kusunoki Asuha"
        # elif item['character'] == u'\u685c':
        #     item['character'] = "Fujimiya Sakura"
        # elif item['character'] == u'\u3072\u306a\u305f':
        #     item['character'] = "Minami Hinata"
        # elif item['character'] == u'\u6953':
        #     item['character'] = "Sendouin Kaede"
        # elif item['character'] == u'\u30df\u30b7\u30a7\u30eb':
        #     item['character'] = "Watagi Michelle"
        # elif item['character'] == u'\u5fc3\u7f8e':
        #     item['character'] = "Asahina Kokomi"
        # elif item['character'] == u'\u3046\u3089\u3089':
        #     item['character'] = "Hasumi Urara"
        # elif item['character'] == u'\u30b5\u30c9\u30cd':
        #     item['character'] = "Sadone"
        # elif item['character'] == u'\u82b1\u97f3':
        #     item['character'] = "Kougami Kanon"
        # elif item['character'] == u'\u8a69\u7a42':
        #     item['character'] = "Kunieda Shiho"
        # elif item['character'] == u'\u8309\u68a8':
        #     item['character'] = "Sakaide Mari"
        # elif item['character'] == u'\u6a39':
        #     item['character'] = "Yakumo Itsuki"
        # elif item['character'] == u'\u98a8\u862d':
        #     item['character'] = "Mitsurugi Fuuran"
        # elif item['character'] == u'\u660e\u65e5\u8449(\u4E2D1)':
        #     item['character'] = "Kusunoki Asuha (Middle School Year 1)"
        #
        # # Card type
        # if item['character']==(u'\u98a8\u862d') or item['character']==(u'\u8309\u68a8') or item['character']==(u'\u6a39') or item['character']==(u'\u660e\u65e5\u8449(\u4e2d1)'):
        #     item['card_type'] = "1"
        # elif item['event'] == (u'\u30b5\u30d6\u30ab\u5c02\u7528'):
        #     item['card_type'] = "2"
        # else:
        #     item['card_type'] = "0"
        #
        # # Skill damage
        # for key in ['skill_damage_normal', 'skill_damage_secret_lesson']:
        #     item[key] = item[key].replace(u'\u500d', " times ")
        #     if item[key].find(u'\u7d04') == 0:
        #         item[key] = item[key].replace(u'\u7d04', "Approx. ", 1)
        #         item[key] = item[key].replace(u'\u7d04', " approx. ")
        #     else:
        #         item[key] = item[key].replace(u'\u7d04', " approx. ")
        #     if item[key].find(u'\u53f0') != -1:
        #         item[key] = item[key].split(u'(\u65e5)')[0]
        #
        # # Skill range
        # item['skill_range'] = item['skill_range'].replace(u'\u4ee5\u81ea\u8eab\u4f5c\u8d77\u9ede\u5c0f',"Start with self ")
        # item['skill_range'] = item['skill_range'].replace(u'\u56db\u5468\u81ea\u8eab', "Around self ")
        # item['skill_range'] = item['skill_range'].replace(u'\u81ea\u8eab', "Self")
        # item['skill_range'] = item['skill_range'].replace(u'\u6211\u65b9\u5168\u54e1', "All allies")
        # item['skill_range'] = item['skill_range'].replace(u'\u5168\u65b9\u4f4d', "Omni-directional ")
        # item['skill_range'] = item['skill_range'].replace(u'\u524d\u65b9', " Forward ")
        # item['skill_range'] = item['skill_range'].replace(u'\u7bc4\u570d', " area")
        # item['skill_range'] = item['skill_range'].replace(u'\u6575\u4eba', "Enemy")
        # item['skill_range'] = item['skill_range'].replace(u'\u7684', "'s ")
        # item['skill_range'] = item['skill_range'].replace(u'\u4e2d\u5fc3', " center ")
        # item['skill_range'] = item['skill_range'].replace(u'\u70b8\u5f48', "Bomb")
        # item['skill_range'] = item['skill_range'].replace(u'\u8ffd\u8e64', "tracking ")
        # item['skill_range'] = item['skill_range'].replace(u'\u79fb\u52d5', " mobile ")
        # item['skill_range'] = item['skill_range'].replace(u'\u6975\u5c0f', " very small ")
        # item['skill_range'] = item['skill_range'].replace(u'\u7279', " very ")
        # item['skill_range'] = item['skill_range'].replace(u'\u5927', " large ")
        # item['skill_range'] = item['skill_range'].replace(u'\u4e2d', " medium ")
        # item['skill_range'] = item['skill_range'].replace(u'\u5c0f', " small ")
        # item['skill_range'] = item['skill_range'].replace(u'\u76f4', " straight ")
        # item['skill_range'] = item['skill_range'].replace(u'\u7dda', " line")
        # item['skill_range'] = item['skill_range'].replace(u'\u578b', " type")
        # item['skill_range'] = item['skill_range'].replace(u'\u79fb\u52d5\u6642\u7784\u6e96', "aim at moving ")
        # # item['skill_range'] = item['skill_range'].replace(u'', "")
        #
        # # Split items
        # if (not item['nakayoshi_effects_noevol']) or (item['nakayoshi_effects_noevol'] != (u'\uff0d')):
        #     splitted = item['nakayoshi_effects_noevol'].split(u'\uff0f')
        #     item['nakayoshi_target_noevol'] = splitted[0]
        #     item['nakayoshi_effects_noevol'] = splitted[1]
        #
        # if (not item['nakayoshi_effects_evol']) or (item['nakayoshi_effects_evol'] != (u'\uff0d')):
        #     splitted = item['nakayoshi_effects_evol'].split(u'\uff0f')
        #     item['nakayoshi_target_evol'] = splitted[0]
        #     item['nakayoshi_effects_evol'] = splitted[1]
        #
        # # Nakayoshi target no evol and evol
        # for key in ['nakayoshi_target_noevol', 'nakayoshi_target_evol']:
        #     item[key] = item[key].replace(u'\u6240\u6709\u4eba', "Everyone")
        #     item[key] = item[key].replace(u'\u5e74\u751f', " year")
        #     item[key] = item[key].replace(u'\u8207', " and ")
        #     item[key] = item[key].replace(u'\u528d', "sword")
        #     item[key] = item[key].replace(u'\u77db', "spear")
        #     item[key] = item[key].replace(u'\u96d9\u69cd', "dual-pistols")
        #     item[key] = item[key].replace(u'\u69cd', "gun")
        #     item[key] = item[key].replace(u'\u6756', "rod")
        #     item[key] = item[key].replace(u'\u69cc', "hammer")
        #     # item[key] = item[key].replace(u'', "")
        #     # item[key] = item[key].replace(u'', "")
        #     # item[key] = item[key].replace(u'', "")
        #     # item[key] = item[key].replace(u'', "")
        #
        # # Return fields in multiple lines style
        # for key in ['skill_description']:
        #     temp = item[key]
        #     item[key] = ""
        #     for substr in temp:
        #         item[key] = "%s%s\n" % (item[key], substr)
        #     item[key] = item[key].rstrip("\n")

        return item