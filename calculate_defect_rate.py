#!/usr/bin/python3
"""
Main runner to calculate the defect rate in production line FC.
Author: Santhosh Balasa
Email: santhosh.kbr@gmail.com
Date: 15/June/2021
"""

import os
import click
import pandas as pd


# Global
PICKS_PATH = "/input/picks/"
QC_PATH = "/input/quality_control/"
OUTPUT_PATH = "/output/"
DATA_PATH = None


class DEFECT_RATE:
    def __init__(self, picks_file_name, qc_file_name):
        self.picks_file_name = picks_file_name
        self.qc_file_name = qc_file_name
        self.picks_file_path = DATA_PATH + PICKS_PATH + self.picks_file_name
        self.qc_file_path = DATA_PATH + QC_PATH + self.qc_file_name
        self.output_file_path = DATA_PATH + OUTPUT_PATH + "output_" + self.picks_file_name.split("_")[1]
        self.total_orders = {}
        self.defects_per_order = {}
        self.defect_rate = {}
        self.output_content = {}
        self.picks_file_content = pd.read_csv(self.picks_file_path)
        self.qc_file_content = pd.read_csv(self.qc_file_path)

    def get_total_picks_per_order(self):
        _total_orders = {}
        for i in self.picks_file_content.groupby("order_id"):
            _total_orders[list(i[1].order_id.to_dict().values())[0]] = len(i[1].order_id.to_dict().values())
        self.total_orders = _total_orders

    def get_defects_per_order(self):
        _defects_per_order = {}
        for i in self.qc_file_content.groupby("order_id"):
            _defects_per_order[set(i[1].order_id.to_dict().values()).pop()] = list(
                i[1].defect.to_dict().values()
            ).count(1)
        self.defects_per_order = _defects_per_order

    def calculate_defects_rate(self):
        _defects_rate = {}
        for k, v in self.defects_per_order.items():
            _defects_rate[k] = str(v / self.total_orders.get(k) * 100)[:5] + "%"
        self.defect_rate = _defects_rate


def generate_defect_rates():
    picks = DATA_PATH + PICKS_PATH
    qc = DATA_PATH + QC_PATH
    for picks_files, qc_files in zip(os.walk(picks), os.walk(qc)):
        for picks_file, qc_file in zip(picks_files[-1], qc_files[-1]):
            dr_obj = DEFECT_RATE(picks_file, qc_file)
            dr_obj.get_total_picks_per_order()
            dr_obj.get_defects_per_order()
            dr_obj.calculate_defects_rate()


@click.command()
@click.option(
    "--data_path",
    required=True,
    help="Pass the data folder path to determine the defect rates",
)
def main(data_path):
    global DATA_PATH
    DATA_PATH = data_path
    generate_defect_rates()


if __name__ == "__main__":
    main()
