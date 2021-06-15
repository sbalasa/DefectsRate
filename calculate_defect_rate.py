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


from pprint import pprint


# Global
PICKS_PATH = "/input/picks/"
QC_PATH = "/input/quality_control/"
OUTPUT_PATH = "/output/"
DATA_PATH = None


def get_output_file_path(suffix):
    return DATA_PATH + OUTPUT_PATH + "output_" + suffix


def get_input_picks_file_path(name):
    return DATA_PATH + PICKS_PATH + name


def get_input_qc_file_path(name):
    return DATA_PATH + QC_PATH + name


def get_total_picks_per_order(picks_file):
    picks_file_content = pd.read_csv(get_input_picks_file_path(picks_file))
    total_orders = {}
    for i in picks_file_content.groupby("order_id"):
        total_orders[list(i[1].order_id.to_dict().values())[0]] = len(i[1].order_id.to_dict().values())
    return total_orders


def get_defects_per_order(qc_file):
    qc_file_content = pd.read_csv(get_input_qc_file_path(qc_file))
    defects_per_order = {}
    for i in qc_file_content.groupby("order_id"):
        defects_per_order[set(i[1].order_id.to_dict().values()).pop()] = list(i[1].defect.to_dict().values()).count(1)
    return defects_per_order


def calculate_defects_rate(total_orders, defects_per_order):
    defects_rate = {}
    for k, v in defects_per_order.items():
        defects_rate[k] = str(v / total_orders.get(k) * 100)[:5] + "%"
    return defects_rate


def generate_output(picks_file, qc_file):
    output_file_path = get_output_file_path(picks_file.split("_")[1])
    total_orders = get_total_picks_per_order(picks_file)
    defects_per_order = get_defects_per_order(qc_file)
    defects_rate = calculate_defects_rate(total_orders, defects_per_order)
    pprint(defects_rate)


def generate_defect_rates():
    picks = DATA_PATH + PICKS_PATH
    qc = DATA_PATH + QC_PATH
    for picks_files, qc_files in zip(os.walk(picks), os.walk(qc)):
        for picks_file, qc_file in zip(picks_files[-1], qc_files[-1]):
            generate_output(picks_file, qc_file)

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
