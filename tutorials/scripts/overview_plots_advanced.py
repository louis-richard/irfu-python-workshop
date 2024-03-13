#!/usr/bin/env python

r"""SHARP summer school

Example script to load magnetic field and electric field from CDF files for MMS
"""

# Built-in imports
import argparse
import glob
import os
import re

# Third party imports
from cdflib import cdfread
from pyrfu import pyrf

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2023"


def main(args):
    r"""main script

    Parameters
    ----------
    args : argparse object
        Code arguments (typically shock id)

    """

    # Construct path to cdf files for the shock and list the files.
    shock_path = os.path.join(os.getcwd(), f"shock{args.shock_id:d}")
    files = glob.glob(os.path.join(shock_path, "*.cdf"))
    files.sort()

    # Load magnetic field
    b_dsl = None

    for file in files:
        if re.match(r"mms1_fgm_brst_l2_*", os.path.basename(file)):
            with cdfread.CDF(file) as f:
                # Get variable attributes
                attrs = f.varattsget("mms1_fgm_b_dmpa_brst_l2")

                # Get time stamps
                epoch = f.varget(attrs["DEPEND_0"])

                # Get data
                data = f.varget("mms1_fgm_b_dmpa_brst_l2")[:, :-1]  # ignore magnitude

            # Convert epoch_tt2000 to numpy.datetime64
            epoch = pyrf.cdfepoch2datetime64(epoch)

            # Construct the time series
            b_dsl_tmp = pyrf.ts_vec_xyz(epoch, data, attrs)

            # Merge time series from different files
            b_dsl = pyrf.ts_append(b_dsl, b_dsl_tmp)
        else:
            continue

    # Load electric field
    e_dsl = None
    for file in files:
        if re.match(r"mms1_edp_brst_l2_*", os.path.basename(file)):
            with cdfread.CDF(file) as f:
                # Get variable metadata
                attrs = f.varattsget("mms1_edp_dce_dsl_brst_l2")

                # Get time stamps
                epoch = f.varget(attrs["DEPEND_0"])

                # Get data
                data = f.varget("mms1_edp_dce_dsl_brst_l2")

            # Convert epoch_tt2000 to numpy.datetime64
            epoch = pyrf.cdfepoch2datetime64(epoch)

            # Construct the time series
            e_dsl_tmp = pyrf.ts_vec_xyz(epoch, data, attrs)

            # Merge time series from different files
            e_dsl = pyrf.ts_append(e_dsl, e_dsl_tmp)
        else:
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--shock-id",
        "-",
        help="shock number",
        required=True,
        type=int,
        choices=[1, 2, 3, 4],
    )
    main(parser.parse_args())
