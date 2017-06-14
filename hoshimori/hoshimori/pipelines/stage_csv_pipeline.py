# -*- coding: utf-8 -*-

import re

class StageCSVPipeline(object):
    @classmethod
    def process_item(self, item, spider):
        for key in ['items']:
            # Copy skill* field
            temp = item[key]
            item[key] = ""
            for substr in temp:
                item[key] = "%s%s\n" % (item[key], substr)
            item[key] = item[key].rstrip("\n")
        return item