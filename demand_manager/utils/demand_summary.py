import os
import os.path
from datetime import date
import re
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from django_pandas.io import read_frame
from demand_manager.models import Demand, VerificationContent, Technology, Release


class DemandFeature:
    def __init__(self):
        # Demand
        self.qs_demand = Demand.objects.all()
        self.df_demand = read_frame(self.qs_demand)
        # VerificationContent
        self.qs_content = VerificationContent.objects.all()
        self.df_content = read_frame(self.qs_content, index_col='content')
        self.list_base_feature = [i for i in list(self.df_content.columns) if re.search(r"lic_feature", i)]
        # Technology
        self.qs_tech = Technology.objects.all()
        self.df_tech = read_frame(self.qs_tech, index_col='tech_node')
        self.list_tech_feature = [i for i in list(self.df_tech.columns) if re.search(r"lic_feature", i)]

        # Date
        self.today = date.today()
        self.start_date = self.df_demand['start_date'].min()
        self.end_date = self.df_demand['end_date'].max()

        # Demand DataFrame
        # Create List of License Feature
        self.list_feature = self.list_base_feature + self.list_tech_feature
        # Create Date list
        self.list_date = pd.date_range(start=self.start_date, end=self.end_date, freq='D')
        # Create Initial DataFrame of Feature
        self.df_demand_feature = pd.DataFrame(index=self.list_date, columns=self.list_feature)
        self.df_num_demand_feature = pd.DataFrame()

        # Max Demand Series
        self.ser_pct_max_demand = pd.Series()
        self.ser_num_max_demand = pd.Series()
        # Required Lic
        self.df_required_lic = pd.DataFrame()
        self.ser_required_lic = pd.Series()

        # Release DataFrame
        self.release_feature = ReleaseFeature(self.list_feature)
        self.release_feature.create_df_release_feature()
        self.df_release_feature = self.release_feature.df_release_feature

        # Setup PNG dir
        self.png_static_dir = "demand_manager/PNG/"
        self.png_dir = "demand_manager/static/" + self.png_static_dir

        # PNG Dictionary
        self.list_png_demand = []
        self.list_png_required_lic = []
        self.df_png_path = pd.DataFrame()

    def demand_summary(self):

        # Create DataFrame of Feature
        self.create_df_demand_feature()

        # Create Series of Required License Feature
        self.get_required_lic()

        # Create Figure Demand-Date
        self.create_demand_figure()

    def create_df_demand_feature(self):

        for index, ser_demand in self.df_demand.iterrows():
            # product = ser_demand['product']
            tech_node = ser_demand['tech_node']
            content = ser_demand['content']
            start_date = ser_demand['start_date']
            end_date = ser_demand['end_date']
            frequency = ser_demand['frequency']

            list_date = pd.date_range(start=start_date, end=end_date, freq='D')
            dict_data = {}
            for base_feature in self.list_base_feature:
                if self.df_content.at[content, base_feature]:
                    dict_data[base_feature] = np.array([frequency] * len(list_date), dtype='int32')
                else:
                    dict_data[base_feature] = np.array([0] * len(list_date), dtype='int32')
            for tech_feature in self.list_tech_feature:
                if self.df_tech.at[tech_node, tech_feature]:
                    dict_data[tech_feature] = np.array([frequency] * len(list_date), dtype='int32')
                else:
                    dict_data[tech_feature] = np.array([0] * len(list_date), dtype='int32')
            df_product = pd.DataFrame(dict_data, index=list_date)

            # Add DataFrame(Product) to DataFrame()
            self.df_demand_feature = self.df_demand_feature.add(df_product, fill_value=0)

    def get_required_lic(self):
        self.df_release_feature = self.df_release_feature[self.start_date:self.end_date].fillna(0)
        self.df_num_demand_feature = self.df_demand_feature.applymap(lambda x: math.ceil(x / 100))
        self.df_required_lic = self.df_num_demand_feature - self.df_release_feature
        self.df_required_lic = self.df_required_lic.mask(self.df_required_lic < 0, 0)

        self.ser_pct_max_demand = self.df_demand_feature.max().astype('int64')
        self.ser_num_max_demand = self.df_num_demand_feature.max().astype('int64')
        self.ser_required_lic = self.df_required_lic.max().astype('int64')

    def create_demand_figure(self):
        if not os.path.isdir(self.png_dir):
            os.makedirs(self.png_dir)
        for lic_feature in self.df_demand_feature.columns:
            self.create_demand_date_png(lic_feature)
            self.create_required_lic_date_png(lic_feature)

        # DataFrame of PNG path
        self.df_png_path = pd.DataFrame({"Demand": self.list_png_demand,
                                         "Required License Feature": self.list_png_required_lic,
                                         },
                                        index=self.df_demand_feature.columns)

    def create_demand_date_png(self, lic_feature):
        # Setup PNG name
        png_name = lic_feature + "_demand.png"

        # Set Data
        x = self.df_demand_feature.index
        y = self.df_demand_feature[lic_feature]

        # figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # plot
        ax.plot(x, y, marker='o')

        # label
        ax.set_xlabel('Date')
        ax.set_ylabel('Demand [%]')

        ax.tick_params(direction='in')
        ylim_max = max(y.max() * 1.1, math.ceil(y.max() / 100) * 100, y.max() + 50)
        plt.ylim([0, ylim_max])
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
        plt.setp(ax.get_xticklabels(), rotation=45, fontsize=10)

        # Title
        ax.set_title(lic_feature)

        # Save as PNG
        fig.tight_layout()
        plt.savefig(self.png_dir + png_name)

        # Add PNG list
        self.list_png_demand.append(self.png_static_dir + png_name)

    def create_required_lic_date_png(self, lic_feature):
        # Setup PNG name
        png_name = lic_feature + "_required_lic.png"

        # Set Data
        date_d = self.df_demand_feature.index
        demand = self.df_num_demand_feature[lic_feature]
        date_r = self.df_release_feature.index
        release = self.df_release_feature[lic_feature]

        # figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # plot
        ax.bar(date_d, demand, width=1, color='#007FFF', edgecolor='#00BFFF', label='Demand')
        ax.plot(date_r, release, color='#FF3232', label='Release')

        # label
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of License Feature')

        ax.tick_params(direction='in')
        ylim_max = max(max(demand), max(release)) + 1
        plt.ylim([0, ylim_max])
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
        plt.setp(ax.get_xticklabels(), rotation=45, fontsize=10)

        plt.legend()

        # Title
        ax.set_title(lic_feature)

        # Save as PNG
        fig.tight_layout()
        plt.savefig(self.png_dir + png_name)

        # Add PNG list
        self.list_png_required_lic.append(self.png_static_dir + png_name)


class ReleaseFeature:
    def __init__(self, list_feature):
        # Release
        self.qs_release = Release.objects.all()
        self.df_release = read_frame(self.qs_release)

        # Date
        self.start_date = self.df_release['start_date'].min()
        self.end_date = self.df_release['end_date'].max()

        # Demand DataFrame
        # Create List of License Feature
        # self.list_feature = list(set(self.df_release['lic_feature'].values.tolist()))
        self.list_feature = list_feature
        # Create Date list
        self.list_date = pd.date_range(start=self.start_date, end=self.end_date, freq='D')
        # Create Initial DataFrame of Feature
        self.df_release_feature = pd.DataFrame(index=self.list_date, columns=self.list_feature)

    def create_df_release_feature(self):

        for index, ser_release in self.df_release.iterrows():
            lic_type = ser_release['lic_type']
            lic_feature = ser_release['lic_feature']
            start_date = ser_release['start_date']
            end_date = ser_release['end_date']
            num_lic_feature = ser_release['num_lic_feature']

            list_date = pd.date_range(start=start_date, end=end_date, freq='D')
            dict_data = {}
            for feature in self.list_feature:
                if feature == lic_feature:
                    dict_data[feature] = np.array([num_lic_feature] * len(list_date), dtype='int32')
                else:
                    dict_data[feature] = np.array([0] * len(list_date), dtype='int32')
            df_feature = pd.DataFrame(dict_data, index=list_date)

            # Add DataFrame(Product) to DataFrame()
            self.df_release_feature = self.df_release_feature.add(df_feature, fill_value=0)

