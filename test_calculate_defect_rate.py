import pytest

import calculate_defect_rate

calculate_defect_rate.DATA_PATH = "./data"
dr_obj = calculate_defect_rate.DEFECT_RATE("pick_1.csv", "qc_1.csv")


def test_get_total_picks_per_order():
    dr_obj.get_total_picks_per_order()
    assert dr_obj.total_orders == {
        1: 2,
        2: 5,
        3: 4,
        4: 4,
        5: 6,
        6: 4,
        7: 6,
        8: 4,
        9: 2,
        10: 6,
        11: 9,
        12: 5,
        13: 3,
        14: 3,
        15: 3,
        16: 5,
        17: 4,
        18: 4,
        19: 8,
        20: 5,
    }


def test_get_defects_per_order():
    dr_obj.get_defects_per_order()
    assert dr_obj.defects_per_order == {
        2: 2,
        3: 0,
        4: 0,
        5: 1,
        7: 0,
        8: 0,
        10: 2,
        11: 1,
        12: 2,
        14: 1,
        15: 1,
        16: 0,
        17: 1,
        18: 0,
        19: 2,
        20: 0,
    }


def test_calculate_defect_rate():
    dr_obj.calculate_defect_rate()
    assert dr_obj.defect_rate == {
        2: "40.0%",
        3: "0.0%",
        4: "0.0%",
        5: "16.66%",
        7: "0.0%",
        8: "0.0%",
        10: "33.33%",
        11: "11.11%",
        12: "40.0%",
        14: "33.33%",
        15: "33.33%",
        16: "0.0%",
        17: "25.0%",
        18: "0.0%",
        19: "25.0%",
        20: "0.0%",
    }

