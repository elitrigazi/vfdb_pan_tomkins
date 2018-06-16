import csv
import sys
import wfdb

VFDB_LOCATION = './vfdb/'
QRS_LOCATION = './vfdb-qrs/'

def load_qrs_i(record):
    qrs_i_filepath = QRS_LOCATION + record + '_1s_i.txt'
    with open(qrs_i_filepath, 'rb') as qrs_i_file:
        line = qrs_i_file.readline()
        qrs_i = line.split(',')
        return qrs_i

def get_annotation(record):
    record_path = VFDB_LOCATION + record
    ann = wfdb.rdann(record_path, 'atr')
    return ann

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Please provide a vfdb record number'
        exit()
    record = str(sys.argv[1])
    qrs_i = load_qrs_i(record)
    ann = get_annotation(record)
    print len(qrs_i), ' r peaks in record', record
    print ann.__dict__
