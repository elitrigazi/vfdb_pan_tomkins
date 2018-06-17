import csv
import sys
import wfdb

VFDB_LOCATION = './vfdb/'
QRS_LOCATION = './vfdb-qrs/'

def load_qrs_i(record):
    """Returns a list with the positions of Rs that pan_tompkins returned for
       a specific record.
    """
    qrs_i_filepath = QRS_LOCATION + record + '_1s_i.txt'
    with open(qrs_i_filepath, 'rb') as qrs_i_file:
        line = qrs_i_file.readline()
        qrs_i = line.split(',')
        return qrs_i

def load_qrs_amp(record):
    """Returns a list with the amp values that pan_tompkins returned for
       a specific record.
    """
    filepath = QRS_LOCATION + record + '_1s_amp.txt'
    with open(filepath, 'rb') as fh:
        line = fh.readline()
        val = line.split(',')
        return val

def get_annotation(record):
    """Returns the annotatation object for a given record
    """
    record_path = VFDB_LOCATION + record
    ann = wfdb.rdann(record_path, 'atr')
    return ann

def get_record(record):
    """Returns the annotatation object for a given record
    """
    record_path = VFDB_LOCATION + record
    record = wfdb.rdrecord(record_path)
    return record

def get_annotation_positions(ann):
    """ Takes an annotation object and returns a list of tuples:
        [
        ('<idx if annotaion position>', 'annotations aux_label'),
        ('<idx if annotaion position>', 'annotations aux_label'),
        ...
        ('<idx if annotaion position>', 'annotations aux_label')
        ]
    """
    return zip(ann.sample.tolist(), ann.aux_note)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Please provide a vfdb record number'
        exit()
    record_id = str(sys.argv[1])
    #qrs_i = load_qrs_i(record)
    #qrs_amp = load_qrs_amp(record)
    ann = get_annotation(record_id)
    record = get_record(record_id)
    #print len(qrs_i), ' r peaks (qrs_i) in record', record
    #print len(qrs_amp), ' r peaks (qrs_amp) in record', record
    #print ann.__dict__
    #print len(ann.sample.tolist()), '\t', len(ann.aux_note), '\t', set(ann.aux_note)
    print record_id, '\t', get_annotation_positions(ann)[0], '\t', record.p_signal[:,0].size
