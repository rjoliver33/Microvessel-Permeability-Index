#!/usr/bin/env python3

"""
Author : Rob J Oliver Jr <roliver2389@gmail.com>
Date   : 2021-07-27
Purpose: Detect overlapping pixel intensities within separate channels, specifically for dextran (red) and stained blood vessels (green).
Formats: Images must be multichannel .tif. Thresholds based on 0-256 pixel intensity images.
"""

import argparse
import os
from datetime import date
import cv2
import pandas as pd

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Detect overlapping pixel intensities within separate channels, specifically for dextran (red) and stained blood vessels (green).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-p",
        "--path",
        metavar="filepath",
        help="Filepath where images to analyze are located, defaults to cwd",
        type=str,
        default=os.getcwd(),
    )

    parser.add_argument(
        "-d",
        "--dthresh",
        help="Threshold value for inclusion as a positive dextran (red channel) pixel",
        metavar="dthresh",
        type=int,
        default=25,
    )

    parser.add_argument(
        "-v",
        "--vthresh",
        help="Threshold value for inclusion as a positive vessel (green channel) pixel",
        metavar="vthresh",
        type=int,
        default=15,
    )

    return parser.parse_args()


# --------------------------------------------------
def dir_path(path):
    """Get and validate filepath"""
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


# --------------------------------------------------
def main():
    """Calculate number of dextran pixels found within a blood vessel positive pixel"""

    args = get_args()
    filepath = args.path
    dextran_thresh = args.dthresh
    vessel_thresh = args.vthresh

    sample_id = []
    out_in_vessel_ratio_list = []
    group_id = []
    total_dex_pix = []
    total_vessel_pix = []

    for filename in os.listdir(filepath):
        if filename.endswith(".tif"):
            sample_id.append(filename)
            if os.path.isfile(os.path.join(filepath, filename)) and "PAE" in filename:
                group_id.append("PAE")
            else:
                group_id.append("SAC")
            tif_path = os.path.abspath(os.path.join(filepath, filename))
            read_tif = cv2.imread(tif_path)
            blue_channel, vessel_img, dextran_img = cv2.split(read_tif)

            pixels_in_vessel = 0
            pixels_out_vessel = 0
            for i in range(dextran_img.shape[0]):
                for j in range(dextran_img.shape[1]):
                    if dextran_img[i, j] >= dextran_thresh:
                        if vessel_img[i, j] >= vessel_thresh:
                            pixels_in_vessel += 1
                        if vessel_img[i, j] < vessel_thresh:
                            pixels_out_vessel += 1
                    else:
                        pass

            total_vessel_pix_count = 0
            for i in range(vessel_img.shape[0]):
                for j in range(vessel_img.shape[1]):
                    if vessel_img[i, j] >= vessel_thresh:
                        total_vessel_pix_count += 1
                    else:
                        pass

            out_in_vessel_ratio = (
                (pixels_out_vessel) / (pixels_in_vessel + pixels_out_vessel) * 100
            )
            out_in_vessel_ratio_list.append(out_in_vessel_ratio)
            total_dex_pix_count = pixels_out_vessel + pixels_in_vessel
            total_dex_pix.append(total_dex_pix_count)
            total_vessel_pix.append(total_vessel_pix_count)

    data_tuples = list(
        zip(
            sample_id,
            group_id,
            out_in_vessel_ratio_list,
            total_dex_pix,
            total_vessel_pix,
        )
    )
    out_in_vessel_ratio_df = pd.DataFrame(
        data_tuples,
        columns=["sample_id", "Group", "out_in_vessel_ratio", "dex_pix", "vessel_pix"],
    )

    today = date.today()
    run_id = today.strftime("%d%b%Y")
    with pd.ExcelWriter(str(run_id) + "DextranRatio.xlsx") as writer:
        out_in_vessel_ratio_df.to_excel(writer, sheet_name=str(run_id))

    print("Analysis complete")
    print(str(run_id) + "DextranRatio.xlsx saved to: " + str(filepath))


# --------------------------------------------------
if __name__ == "__main__":
    main()
