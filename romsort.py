#!/usr/bin/python3
import argparse
import re
import os
import shutil

parser = argparse.ArgumentParser(description="region sort roms files, sorts into destination dir in region based folders")
parser.add_argument('rom_base_dir', metavar="r", type=str, help="origin path for roms to sort")
parser.add_argument('rom_destination_base_dir', metavar='d', type=str, help="base path for resulting roms")
args = parser.parse_args()
if not args.rom_base_dir or not args.rom_destination_base_dir:
    print("missing args")
    exit()


def regex_for_region(region):
    return ".*((?:\(.*\s?"+region+"\s?[\),]))"


def evaluate_region(rom_file_path):
    if re.search(regex_for_region("USA"), rom_file_path, re.IGNORECASE):
        return "USA"
    elif re.search(regex_for_region("EUROPE"), rom_file_path, re.IGNORECASE):
        return "EUROPE"
    elif re.search(regex_for_region("JAPAN"), rom_file_path, re.IGNORECASE):
        return "JAPAN"
    elif re.search(regex_for_region("World"), rom_file_path, re.IGNORECASE):
        return "WORLD"
    else:
        return "UNKNOWN"

rom_path = os.path.abspath(args.rom_base_dir)


roms_in_folder = [f for f in os.listdir(rom_path)]

usa_path = os.path.join(rom_path, os.path.join(args.rom_destination_base_dir, "USA"))
euro_path = os.path.join(rom_path, os.path.join(args.rom_destination_base_dir, "EUROPE"))
japan_path = os.path.join(rom_path, os.path.join(args.rom_destination_base_dir, "JAPAN"))
world_path = os.path.join(rom_path, os.path.join(args.rom_destination_base_dir, "WORLD"))


def get_dest_file_name(region_path,rom_full_path):
    if not os.path.exists(region_path):
        os.mkdir(region_path)
    return os.path.join(region_path,os.path.basename(rom_full_path))


for r in roms_in_folder:
    if evaluate_region(r) in "USA":
        shutil.copy(os.path.join(rom_path, r), get_dest_file_name(usa_path, r))
    elif evaluate_region(r) in "EUROPE":
        shutil.copy(os.path.join(rom_path, r), get_dest_file_name(euro_path, r))
    elif evaluate_region(r) in "JAPAN":
        shutil.copy(os.path.join(rom_path, r), get_dest_file_name(japan_path, r))
    elif evaluate_region(r) in "WORLD":
        shutil.copy(os.path.join(rom_path, r), get_dest_file_name(world_path, r))
    else:
        print(r)
