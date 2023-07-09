import sys
import os
import csv
import io

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_stop_seq():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No filename provided!" + COLOR_RESET)
        exit()    
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(COLOR_RED + "Input is not a file! Please input stop_times.txt." + COLOR_RESET)
        exit()
    make_new_file(filepath)

def make_new_file(filepath):
    with open(filepath, "rb") as file_raw:
        stop_times_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(stop_times_txt)
        csv_list = list(csv_file)
        if "stop_sequence" not in csv_file.fieldnames:
            print(COLOR_RED + "No stop_sequence column detected. The operation cannot be performed." + COLOR_RESET)
            return
        for row in csv_list:
            if not row["stop_sequence"]:
                print(COLOR_RED + "Input file missing stop_sequence value(s). The operation cannot be performed." + COLOR_RESET)
                return
        file_name = "stop_times_syncro.txt"
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["stop_sequence"] = int(row["stop_sequence"]) - 1
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with stop_sequence reduced by 1." + COLOR_RESET)

if __name__ == "__main__":
    convert_stop_seq()