import sys
import os
import csv
import io

COLOR_RED   = "\033[1;31m"
COLOR_BLUE  = "\033[1;34m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_stop_seq():
    filepath = sys.argv[1]
    if len(sys.argv) < 2:
        print(COLOR_RED + "No filename provided!" + COLOR_RESET)
        exit()
    if not os.path.isfile(filepath):
        print(COLOR_RED + "File does not exist!" + COLOR_RESET)
    if not os.path.basename(filepath) == 'stop_times.txt':
        print(COLOR_RED + "Incorrect file input! Please input stop_times.txt" + COLOR_RESET)
        exit()
    stopseq_map = make_stopseq_map(filepath)
    make_new_file(filepath, stopseq_map)

def make_stopseq_map(filepath):
    stop_seq_map = {}
    with open(filepath, "rb") as stop_times_file_raw:
        stop_times_txt = io.TextIOWrapper(stop_times_file_raw)
        stop_times_csv = csv.DictReader(stop_times_txt)
        for row in stop_times_csv:
            if "stop_sequence" not in row or not row["stop_sequence"]:
                print(COLOR_BLUE + "No stop_sequence values are present and therefore the operation cannot be performed" + COLOR_RESET)
            subtract_one = int(row["stop_sequence"]) - 1
            stop_seq_map[row["stop_sequence"]] = subtract_one            
    return(stop_seq_map)

def make_new_file(filepath, stopseq_map, field_names=["stop_sequence"]):
    with open(filepath, "rb") as file_raw:
        stop_times_txt = io.TextIOWrapper(file_raw)
        csvfile = csv.DictReader(stop_times_txt)
        file_name = 'stop_times2.txt'
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again. Skipping..." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csvfile.fieldnames)
        new_csv_writer.writeheader()
        for row in csvfile:
            row_copy = row.copy()
            for field_name in field_names:
                if row[field_name] not in stopseq_map:
                    print(COLOR_BLUE + "Invalid field name " + field_name + " for file " + file_name + ", skipping this file" + COLOR_RESET)
                    return
                found_stop_seq = row_copy[field_name]
                row_copy[field_name] = stopseq_map[found_stop_seq] if found_stop_seq in stopseq_map else found_stop_seq
            new_csv_writer.writerow(row_copy)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with stop_sequence reduced by 1" + COLOR_RESET)

if __name__ == "__main__":
    convert_stop_seq()