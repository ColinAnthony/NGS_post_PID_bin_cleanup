#!/usr/bin/python3
from __future__ import print_function
from __future__ import division
import os
import argparse
import collections
from Bio import SeqIO


__author__ = 'Colin Anthony'


def main(infile, outpath, field):

    alignment = SeqIO.parse(infile, "fasta")
    d = collections.defaultdict(list)

    # account for python zero indexing
    field -= 1

    # get unique field(s) for splitting by time point
    for sequence_obj in alignment:
        unique_field = sequence_obj.description.split("_")[0:field]
        new_name = "_".join(unique_field) + "_sep.fasta"
        out_file_name = os.path.join(outpath, new_name)
        d[out_file_name].append(sequence_obj)

    # write the grouped sequences to their outfiles
    for out_file, seq_objs in d.items():
        for seq_obj in seq_objs:
            with open(out_file, 'a') as handle:
                handle.write(">{0}\n{1}\n".format(seq_obj.name, str(seq_obj.seq)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plots loop stats from csv file (produced by loop_stats.py)',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--infile', type=str, required=True,
                        help='The input fasta file')
    parser.add_argument('-o', '--outpath', default=argparse.SUPPRESS, type=str,
                        help='The path to where the output file will be created', required=True)
    parser.add_argument('-f', '--field', type=int, default=4, required=False,
                        help="The field that differentiates your samples/time points (use the last field if multiple."
                             "(ie: 4 for 'CAP177_2000_004wpi_V3C4_GGGACTCTAGTG_28, or 2 for SVB008_SP_GGTAGTCTAGTG_231")

    args = parser.parse_args()
    infile = args.infile
    outpath = args.outpath
    field = args.field

    main(infile, outpath, field)
