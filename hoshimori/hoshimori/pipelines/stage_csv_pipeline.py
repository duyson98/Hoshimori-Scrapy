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

        # Return 'drops' field in multiple lines style
        temp = item['drops']
        item['drops'] = ""
        for substr in temp:
            item['drops'] = "%s%s\n" % (item['drops'], substr)
        item['drops'] = item['drops'].rstrip("\n")

        return item
