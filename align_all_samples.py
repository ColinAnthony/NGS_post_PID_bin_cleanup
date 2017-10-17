#!/usr/bin/python
from __future__ import print_function
from __future__ import division
import os
import tempfile
import subprocess
from subprocess import DEVNULL
import argparse
import collections
from Bio import SeqIO


__author__ = 'Colin Anthony'


def fasta_to_dct_rev(fn):
    '''Converts a fasta file to a dictionary
    :param fn: a fasta file
    :return: a dictionary key = sequence, value = list of sequence names with that sequence
    '''

    dct = collections.defaultdict(list)
    for seq_record in SeqIO.parse(open(fn), "fasta"):
        dct[str(seq_record.seq).upper()].append(seq_record.description.replace(" ", "_"))

    return dct


def align_dna(dna_dict, tmp_file):
    '''
    does a mafft multiple sequence alignment on a fasta file
    :param dna_dict (dict) dictionary containing the conserved regions f the sequence
    :param tmp_file: (srt) path to temp folder
    :return: (dict) dictionary of aligned sequences for all conserved regions
    '''
    # write temp outfile
    tmp_file_in = os.path.join(tmp_file + '.fasta')
    tmp_file_out = os.path.join(tmp_file + '.aln')
    for seq, name_list in dna_dict.items():
        with open(tmp_file_in, 'a') as handle1:
            handle1.write('>' + str(name_list[0]) + '\n' + str(seq) + '\n')

    cmd = 'mafft {0} > {1}'.format(tmp_file_in, tmp_file_out)
    subprocess.call(cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL)
    # todo error message add mafft to path
    # print("Aligning the sequences, please wait")

    # import the aligned file
    aln_seqs = fasta_to_dct_rev(tmp_file_out)

    # remove the temp files
    os.remove(tmp_file_in)
    os.remove(tmp_file_out)

    new_aln_seqs = collections.defaultdict()
    for seq in aln_seqs.keys():
        lookup_sequence = seq.replace("-", "")
        names_list = dna_dict[lookup_sequence]
        new_aln_seqs[seq] = names_list

    return new_aln_seqs


def main(infile, outpath, name):

    outfile = os.path.join(outpath, name)
    tmp_path = tempfile.gettempdir()
    tmp_file = os.path.join(tmp_path, name)

    # import sequences into dictionary
    d = fasta_to_dct_rev(infile)

    # run mafft alignment on sequences
    align_d = align_dna(d, tmp_file)

    # overwrite existing file if present
    with open(outfile, 'w') as handle:
        handle.write('')

    # write aligned sequences to file
    with open(outfile, 'w') as handle:
        for seq, name_list in align_d.items():
            for seq_name in name_list:
                out_name = '>' + seq_name + '\n'
                handle.write(out_name + seq + '\n')

    print("Aligning completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--infile', default=argparse.SUPPRESS, type=str,
                        help='The input fasta file, with all the time points in one file', required=True)
    parser.add_argument('-o', '--outpath', default=argparse.SUPPRESS, type=str,
                        help='The path to where the output file will be created', required=True)
    parser.add_argument('-n', '--name', default=argparse.SUPPRESS, type=str,
                        help='the prefix name of your outfile', required=True)

    args = parser.parse_args()
    infile = args.infile
    outpath = args.outpath
    name = args.name

    main(infile, outpath, name)
