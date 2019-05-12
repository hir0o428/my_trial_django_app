from datetime import date
import re
import pandas as pd
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt

from django_pandas.io import read_frame
from demand_manager.models import Demand, VerificationContent, Technology


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

    def demand_summary(self):

        # Create DataFrame of Feature
        self.create_df_demand_feature()

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
                    dict_data[base_feature] = np.array([frequency] * len(list_date), dtype='int8')
                else:
                    dict_data[base_feature] = np.array([0] * len(list_date), dtype='int8')
            for tech_feature in self.list_tech_feature:
                if self.df_tech.at[tech_node, tech_feature]:
                    dict_data[tech_feature] = np.array([frequency] * len(list_date), dtype='int8')
                else:
                    dict_data[tech_feature] = np.array([0] * len(list_date), dtype='int8')
            df_product = pd.DataFrame(dict_data, index=list_date)

            # Add DataFrame(Product) to DataFrame()
            self.df_demand_feature = self.df_demand_feature.add(df_product, fill_value=0)

    def create_demand_figure(self):
        # Setup PNG dir
        png_dir = "./demand_manager/static/demand_manager/PNG/"
        if not os.path.isdir(png_dir):
            os.makedirs(png_dir)
        for lic_feature in self.df_demand_feature.columns:
            self.create_demand_date_png(lic_feature, png_dir)

    def create_demand_date_png(self, lic_feature, png_dir):
        # Setup PNG name
        png_name = lic_feature + ".png"

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
        # plt.ylim([0,])

        # Title
        ax.set_title(lic_feature)

        # Save as PNG
        fig.tight_layout()
        plt.savefig(png_dir + png_name)

