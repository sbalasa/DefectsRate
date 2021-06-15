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
    """
    This class is the main data structure used to calculate defect rate in production line FC.
    """

    def __init__(self, picks_file_name, qc_file_name):
        """
        This is constructor to the class
        Args:
            picks_file_name (str): File name to the input picks file
            qc_file_name (str): File name to the input quality control file
        """
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
        """
        This method is used to group the picks by order_id and get total orders
        """
        _total_orders = {}
        for i in self.picks_file_content.groupby("order_id"):
            _total_orders[list(i[1].order_id.to_dict().values())[0]] = len(i[1].order_id.to_dict().values())
        self.total_orders = _total_orders

    def get_defects_per_order(self):
        """
        This method is used to group the picks by order_id and get defects per order
        """
        _defects_per_order = {}
        for i in self.qc_file_content.groupby("order_id"):
            _defects_per_order[set(i[1].order_id.to_dict().values()).pop()] = list(
                i[1].defect.to_dict().values()
            ).count(1)
        self.defects_per_order = _defects_per_order

    def calculate_defect_rate(self):
        """
        This method is used to calculate the defect rate
        Defect Rate per order = (Defective Ingredients found per order / Total Picked Ingredients per order) in %
        """
        _defect_rate = {}
        for k, v in self.defects_per_order.items():
            _defect_rate[k] = str(v / self.total_orders.get(k) * 100)[:5] + "%"
        self.defect_rate = _defect_rate

    def generate_output(self):
        """
        This method is used to generate output csv having defect rate, section and timeframe.
        """
        for i in self.picks_file_content.groupby("order_id"):
            _order_id = list(i[1].order_id.to_dict().values())[0]
            _ingredient_id = ",".join(map(str, set(i[1].ingredient_id.to_dict().values())))
            _defect_rate = self.defect_rate.get(_order_id, "0.0%")
            _zone_id = ",".join(map(str, set(i[1].zone_id.to_dict().values())))
            _time = list(i[1].created_at.to_dict().values())
            _timeframe = f"{min(_time)} - {max(_time)}"
            self.output_content[_order_id] = [_order_id, _ingredient_id, _defect_rate, _zone_id, _timeframe]
        output = pd.DataFrame.from_dict(
            self.output_content,
            orient="index",
            columns=["Order ID", "Ingredients", "Defect Rate", "Section", "Time Frame"],
        )
        output.to_csv(self.output_file_path)


def generate_defect_rates():
    """
    Function to generate defect rate walking through the input csv files.
    """
    picks = DATA_PATH + PICKS_PATH
    qc = DATA_PATH + QC_PATH
    for picks_files, qc_files in zip(os.walk(picks), os.walk(qc)):
        for picks_file, qc_file in zip(picks_files[-1], qc_files[-1]):
            dr_obj = DEFECT_RATE(picks_file, qc_file)
            dr_obj.get_total_picks_per_order()
            dr_obj.get_defects_per_order()
            dr_obj.calculate_defect_rate()
            dr_obj.generate_output()


@click.command()
@click.option(
    "--data_path",
    required=True,
    help="Pass the data folder path to determine the defect rates",
)
def main(data_path):
    """
    This file is used to calculate defect rate in production line FC.
    Args:
        data_path (str): Path to the input data files
    """
    global DATA_PATH
    DATA_PATH = data_path
    generate_defect_rates()


if __name__ == "__main__":
    main()
