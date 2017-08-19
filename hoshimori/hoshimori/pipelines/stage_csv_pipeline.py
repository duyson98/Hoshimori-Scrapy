# -*- coding: utf-8 -*-


class StageCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):
        # Retrieve name
        item['stage_name'] = item['stage_name'].split('/')[1]

        # Retrieve episode
        splitted = item['stage_name'].split('-')
        item['episode'] = splitted[0]
        item['stage_number'] = splitted[1][0]

        # # Retrieve story part for stage
        # temp = item['story_part']
        # if temp == '\xe7\x89\xb9\xe5\x88\xa5\xe7\xb7\xa8':
        #     item['story_part'] = "Special part"
        # else:
        #     item['story_part'] = temp[((temp.find('\xe7\xac\xac'))+3):(temp.find('\xe9\x83\xa8'))]
        #
        # # Retrieve story chapter for stage
        # temp = item['story_chapter']
        # if temp == "エピローグ":
        #     item['story_chapter'] = "Epilogue"
        # elif temp.find("特別編") != -1:
        #     item['story_chapter'] = temp.replace("特別編", "Special chapter ")
        # else:
        #     item['story_chapter'] = temp[((temp.find('\xe7\xac\xac')) + 3):(temp.find('\xe7\xab\xa0'))]

        # # Return fields in multiple lines style
        # for key in ['small_irous', 'large_irous']:
        #     temp = item[key]
        #     item[key] = ""
        #     for substr in temp:
        #         item[key] = "%s%s\n" % (item[key], substr)
        #     item[key] = item[key].rstrip("\n")

        # # Return fields in multiple lines style
        # for key in ['easy_drops', 'normal_drops', 'hard_drops', 'ex_drops']:
        #     temp = item[key]
        #     item[key] = ""
        #     for substr in temp:
        #         item[key] = "%s%s\n" % (item[key], substr)
        #     item[key] = item[key].rstrip("\n")

        return item
