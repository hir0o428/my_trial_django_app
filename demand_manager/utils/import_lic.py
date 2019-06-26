import os
import os.path
from datetime import date, datetime
import re
import math
import pandas as pd
import numpy as np

from demand_manager.models import Release


class ReleaseLic:
    def __init__(self, lic_type, lic_file):
        self.lic_type = lic_type
        self.lic_file = lic_file

        self.dict_server = {}
        self.vendor = ""

        self.extract_flag = False
        self.feature = ""

    def add_feature2db(self):
        with open(self.lic_file, mode='r', encoding='utf-8' ) as f:
            for line in f:
                line = line.strip()
                if not self.extract_flag:
                    if re.search(r'^SERVER\s', line):
                        list_server = line.split()
                        if len(list_server) > 3:
                            host = list_server[1]
                            hostid = list_server[2]
                            port = list_server[3]
                        else:
                            host = list_server[1]
                            hostid = list_server[2]
                            port = ""
                        if host not in self.dict_server.keys():
                            self.dict_server[host] = {"HOST_ID": hostid, "PORT": port}
                        else:  # TODO:
                            pass
                    elif re.search(r'^VENDOR\s', line):
                        self.vendor = re.sub(r'^VENDOR\s+(\S+).*', '\\1', line)
                    elif re.search(r'^(FEATURE|INCREMENT)\s', line):
                        self.feature = Feature(self.lic_type, self.extract_flag)
                        self.feature.extract(line)
                        self.extract_flag = self.feature.extract_flag
                        # if not re.search(r'\\$', line):
                        #     self.add_db()
                        # else:
                        #    self.extract_flag = True
                else:
                    self.feature.extract(line)
                    self.extract_flag = self.feature.extract_flag
                    # if not re.search(r'\\$', line):
                    #    print("Add DB...")
                    #    self.add_db()
                    #    self.extract_flag = False


class Feature:
    def __init__(self, lic_type, extract_flag):
        self.lic_type = lic_type
        self.extract_flag = extract_flag

        self.feature = ""
        self.vendor = ""
        self.feat_version = ""
        self.exp_date = ""
        self.num_lic = 0
        self.sign = ""
        self.issued_date = ""
        self.start_date = ""
        self.list_param = []

    def extract(self, line):
        self.list_param.extend(line.split())
        if not re.search(r'[\\|¥]$', line):
            self.feature = self.list_param[1]
            self.vendor = self.list_param[2]
            self.feat_version = self.list_param[3]
            self.exp_date = self.list_param[4]
            self.exp_date = datetime.strptime(self.exp_date, '%d-%b-%Y').date()
            self.num_lic = self.list_param[5]
            print(self.list_param)
            print("FEATURE: {0}\n"
                  "VENDOR: {1}\n"
                  "FEATURE_VERSION: {2}\n"
                  "EXP_DATE: {3}\n"
                  "NUM_LIC: {4}\n"
                  .format(self.feature, self.vendor, self.feat_version, self.exp_date, self.num_lic))
            for item in self.list_param:
                if re.search(r'=', item):
                    if re.search(r'ISSUED=', item):
                        self.issued_date = re.sub(r'\S+=(\S+)', '\\1', item)
                    elif re.search(r'START=', item):
                        self.start_date = re.sub(r'\S+=(\S+)', '\\1', item)
                        self.start_date = datetime.strptime(self.start_date, '%d-%b-%Y').date()
            print("ISSUED_DATE: {0}\n"
                  "START_DATE: {1}\n".format(self.issued_date, self.start_date))

            print("Add DB...")
            self.add_db()

            self.extract_flag = False
        else:
            self.list_param.pop()
            self.extract_flag = True

    def add_db(self):
        release_lic, created = Release.objects.get_or_create(
            lic_type=self.lic_type,
            lic_feature=self.feature,
            end_date = self.exp_date,
            start_date = self.start_date,
            num_lic_feature = self.num_lic,
        )
        release_lic.save()


