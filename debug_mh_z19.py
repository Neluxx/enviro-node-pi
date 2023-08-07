#!/usr/bin/env python3
"""
MH-Z19
"""

import mh_z19


def run():
    """Main Method"""

    mhz19 = mh_z19.read_all()

    print("MH-Z19")
    print("CO2:", mhz19["co2"])


if __name__ == "__main__":
    run()
