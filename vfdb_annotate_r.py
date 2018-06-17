import csv
import numpy
import sys
import wfdb

ann_str_to_num  = {
    '(AFIB\x00': 0,
    '(ASYS\x00': 1,
    '(B\x00': 2,
    '(BI\x00': 3,
    '(HGEA\x00': 4,
    '(N\x00': 5,
    '(NSR\x00': 5,
    '(NOD\x00': 6,
    '(NOISE\x00': 7,
    '(PM\x00': 8,
    '(SBR\x00': 9,
    '(SVTA\x00': 10,
    '(VER\x00': 11,
    '(VF\x00': 12,
    '(VFIB\x00': 12,
    '(VFL\x00': 13,
    '(VT\x00': 14
}


VFDB_LOCATION = './vfdb/'
QRS_LOCATION = './vfdb-qrs/'

def load_qrs_i(record):
    """Returns a list with the positions of Rs that pan_tompkins returned for
       a specific record.
    """
    filepath = QRS_LOCATION + record + '_1s_i.txt'
    qrs_i = numpy.genfromtxt(filepath, delimiter=',')
    return qrs_i

def load_qrs_amp(record):
    """Returns a list with the amp values that pan_tompkins returned for
       a specific record.
    """
    filepath = QRS_LOCATION + record + '_1s_amp.txt'
    qrs_amp = numpy.genfromtxt(filepath, delimiter=',')
    return qrs_amp

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

def create_qrs_annotation_mapping(qrs_i, qrs_amp, ann_pos):
    """Assign annotations to every R peak.

    :param qrs_i: list with the r positions
    :param qrs_amp: amp values in the qrs_i positions
    :param ann_pos: list of tuples with the position of every annotation

    returns a list of tuples [(qrs_i, qrs_amp, annotation_string), ...]
    """
    ann_pos = [(0, '(N\x00')] + ann_pos
    len_ann_pos = len(ann_pos)
    len_qrs_i = len(qrs_i)
    res = numpy.zeros((len_qrs_i, 3))
    i = 0
    while i < len_ann_pos - 1:
        pos, ann = ann_pos[i]
        ann = ann_str_to_num[ann]
        next_pos, next_ann = ann_pos[i + 1]
        x = 0
        while x < len_qrs_i:
            if pos <= qrs_i[x] and qrs_i[x] < next_pos:
                res[x][0] = qrs_i[x]
                res[x][1] = qrs_amp[x]
                res[x][2] = ann
            x = x +1
        i = i + 1

    pos, ann = ann_pos[len_ann_pos - 1]
    ann = ann_str_to_num[ann]
    x = 0
    while x < len_qrs_i:
        if pos <= qrs_i[x]:
            res[x][0] = qrs_i[x]
            res[x][1] = qrs_amp[x]
            res[x][2] = ann
        x = x +1
    return res


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Please provide a vfdb record number'
        exit()
    record_id = str(sys.argv[1])
    qrs_i = load_qrs_i(record_id)
    #print type(qrs_i)
    qrs_amp = load_qrs_amp(record_id)
    ann = get_annotation(record_id)
    #record = get_record(record_id)
    #print len(qrs_i), ' r peaks (qrs_i) in record', record
    #print len(qrs_amp), ' r peaks (qrs_amp) in record', record
    #print ann.__dict__
    #print len(ann.sample.tolist()), '\t', len(ann.aux_note), '\t', set(ann.aux_note)
    #print record_id, '\t', get_annotation_positions(ann)[0], '\t', record.p_signal[:,0].size
    #print get_annotation_positions(ann)
    print create_qrs_annotation_mapping(qrs_i, qrs_amp, get_annotation_positions(ann))
