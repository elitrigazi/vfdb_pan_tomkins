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
VFDB_RECORDS = [418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428,
                429, 430, 602, 605, 607, 609, 610, 611, 612, 614, 615]

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

    returns a ndarray (number of R, 3) Every row will contain the
            index of the R pick, the amp of the peak and the annotation
            as number. See the dict in the beggining of this file for the
            mapping.
            [
                [index_of_R_peak, value_of_amp, annotation_id],
                ...
                [index_of_R_peak, value_of_amp, annotation_id]
            ]
    """
    # From 0 to the first annotation set the annotation to normal.
    ann_pos = [(0, '(N\x00')] + ann_pos
    # number of annotation
    len_ann_pos = len(ann_pos)
    # Number of R peaks
    len_qrs_i = len(qrs_i)
    # Initialize a zeros array for the result
    res = numpy.zeros((len_qrs_i, 3))
    # For every annotation loop the R peaks
    i = 0
    while i < len_ann_pos:
        # Take the current annotation string and its position in the siganl
        pos, ann = ann_pos[i]
        # Take the posotion of the next annotation
        ann = ann_str_to_num[ann]
        # In the case of the last annotation loop until the end of the R peaks
        # array.
        if i == len_ann_pos - 1:
            next_pos = qrs_i[qrs_i.size - 1] + 1
        else:
            next_pos, next_ann = ann_pos[i + 1]
        # For evert peak:
        x = 0
        while x < len_qrs_i:
            # If the R index is after the index of the annotation and
            # before the next annotation (ot the end of the R array)
            # set the annotation string
            if pos <= qrs_i[x] and qrs_i[x] < next_pos:
                res[x][0] = qrs_i[x]
                res[x][1] = qrs_amp[x]
                # if the annotation is NOISE a.k.a 7, set the previous
                # annotation
                if ann == 7 and pos != 0:
                    ann = ann_str_to_num[ann_pos[i - 1][1]]
                res[x][2] = ann
            x = x +1
        i = i + 1

    return res

def create_rr_annotation(annotated_r_peaks):
    """Create RR segments and annotate them.

    :param qrs_i: np.array with the r positions
    :param ann_pos: list of tuples with the position of every annotation

    returns a length(qrs_i) by 4 array which looks like this:
    [
        [start_or_RR_segment, end_or_RR_segnemnt, RR_distane (aka end_or_RR_segnemnt - start_or_RR_segment), annotation_id]
        ...
        [start_or_RR_segment, end_or_RR_segnemnt, RR_distane (aka end_or_RR_segnemnt - start_or_RR_segment), annotation_id]
    ]
    """
    res = numpy.zeros((annotated_r_peaks[:,0].size - 1, 4))
    # Set the start of the RR segments
    # Take all R indices
    all_r_idx = annotated_r_peaks[:,0]
    # Take the annotations for all Rs
    all_annots = annotated_r_peaks[:,2]

    # For the start R take from the first to the second to last
    # position 0 to -1
    start_r = all_r_idx[0:-1]
    # For the end R take from the second to the end, position 1 to end
    end_r = all_r_idx[1:all_r_idx.size]
    if start_r.size != end_r.size:
        raise Exception("start_r and end_r have diffrent sizes.")
    # The 1st column is the start R peak
    res[:,0] = start_r
    # The 2nd column is the end R peak
    res[:,1] = end_r
    # The 3rd column is the difference of end - start Rs
    res[:,2] = end_r - start_r
    # The 4th column is the annotation of the RR segment, defined by the
    # annotation of the end R.
    res[:,3] = all_annots[1:all_annots.size]

    return res

def save_rr_segment_to_csv(record_id):
    """
    Takes a record id from vfdb and writes the RR segment with its annotation
    to a csv file.

    :param record_id: The record ID eg 418
    """

    qrs_i = load_qrs_i(record_id)
    #print type(qrs_i)
    qrs_amp = load_qrs_amp(record_id)
    ann = get_annotation(record_id)
    annot_positions = get_annotation_positions(ann)
    annotated_r_peaks = create_qrs_annotation_mapping(qrs_i, qrs_amp, annot_positions)
    annotated_rr_segments = create_rr_annotation(annotated_r_peaks)
    # numpy.set_printoptions(suppress=True)
    # print annotated_rr_segments
    numpy.savetxt(QRS_LOCATION + record_id + '_RR.txt', annotated_rr_segments, delimiter=",")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Please provide a vfdb record number'
        exit()
    arg1 = str(sys.argv[1])
    if arg1 == 'all':
        for record_id in VFDB_RECORDS:
            save_rr_segment_to_csv(str(record_id))
    else:
        record_id = arg1
