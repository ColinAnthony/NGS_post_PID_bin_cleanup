#!/usr/bin/python
from __future__ import print_function
from __future__ import division
import os
import sys
import argparse
import collections
from glob import glob
from Bio import SeqIO


__author__ = 'Colin Anthony'


def fasta_to_dct(fn):
    '''
    converts a fasta file to a dictionary where key = seq name, value = sequence
    :param fn: a fasta file
    :return: a dictionary
    '''
    dct = collections.OrderedDict()
    for seq_record in SeqIO.parse(open(fn), "fasta"):
        dct[seq_record.description.replace(" ", "_")] = str(seq_record.seq).replace("~", "-").upper()
    return dct


def fastq_to_dct(fn):
    '''
    converts a fastq file to a dictionary where key = seq name, value = sequence
    :param fn: a fastq file
    :return: a dictionary
    '''
    dct = collections.OrderedDict()
    for seq_record in SeqIO.parse(open(fn), "fastq"):
        dct[seq_record.description.replace(" ", "_")] = str(seq_record.seq).replace("~", "-").upper()
    return dct


def main(inpath, outfile):

    print("Calculating sequencing depth and yield statistics")
    # initialize master dict to return
    stats_d = collections.defaultdict(list)

    all_names = collections.defaultdict(str)

    # clear the stats_out file
    with open(outfile, 'w') as handle:
        handle.write("")

    # target dirs
    raw_files = os.path.join(inpath, "0raw", "*_R1.fastq")
    merged_files = os.path.join(inpath, "1consensus", "binned", "*", "*_mergePEAR", "*assembled.fastq")
    consensus_files = os.path.join(inpath, "1consensus", "*.fasta")
    cleaned_files = os.path.join(inpath, "2cleaned", "*_clean.fasta")
    contam_files = os.path.join(inpath, "3contam_removal", "*_good.fasta")
    # dirs_to_check = [raw_files, merged_files, consensus_files, contam_files]



    binned_folders = os.path.join(inpath, "1consensus", "binned", "*")
    for binned_folder in glob(binned_folders):
        raw = os.path.join(binned_folder, "n001_fwd_loadData")




    # calculate number of raw sequences
    stats_d["headers"].append("name")
    stats_d["headers"].append("raw_sequences")
    for raw_file in glob(raw_files):
        name = os.path.split(raw_file)[-1].replace("_R1.fastq", "")
        all_names[name] = name
        raw_d = fastq_to_dct(raw_file)
        total_raw = str(len(raw_d.keys()))
        stats_d[name].append(name)
        stats_d[name].append(total_raw)

    # calculate number of merged sequences
    stats_d["headers"].append("merged_sequences")
    for merged_file in glob(merged_files):
        # get rid of the generic file name "merged.fastq.assembled.fastq"
        path_split1 = os.path.split(merged_file)[0]
        # get rid of the generic folder name "*_mergePEAR"
        path_split2 = os.path.split(path_split1)[0]
        # get the sample name
        name = os.path.split(path_split2)[-1]

        # Check you have the correct sample name
        if name not in all_names.keys():
            print("Can't match name for merged file with parent file name")
            print("name", name)
            print("not in", all_names.keys())
            sys.exit()

        merged_d = fastq_to_dct(merged_file)
        total_merged = str(len(merged_d.keys()))
        stats_d[name].append(total_merged)

    # calculate number of consensus sequences
    stats_d["headers"].append("consensus_sequences")
    for consensus_file in glob(consensus_files):
        print(consensus_file)
        name = os.path.split(consensus_file)[-1].replace(".fasta", "")
        if name not in all_names.keys():
            print("Can't match name for consensus file with parent file name")
            print("name", name)
            print("not in", all_names.keys())
            sys.exit()
        consensus_d = fasta_to_dct(consensus_file)
        total_consensus = str(len(consensus_d.keys()))
        stats_d[name].append(total_consensus)

    # calculate number of cleaned sequences
    stats_d["headers"].append("cleaned_sequences")
    for cleaned_file in glob(cleaned_files):
        name = os.path.split(cleaned_file)[-1].replace("_clean.fasta", "")
        if name not in all_names.keys():
            print("Can't match name for cleaned file with parent file name")
            print("name", name)
            print("not in", all_names.keys())
            sys.exit()

        clean_d = fasta_to_dct(cleaned_file)
        total_clean = str(len(clean_d.keys()))
        stats_d[name].append(total_clean)

    # calculate number of sequences after contam removal
    stats_d["headers"].append("no_contaminants")
    stats_d["headers"].append("prop_detection_1_percent_variant")
    stats_d["headers"].append("variant_freq_with_95_percent_detection")
    for contam_file in glob(contam_files):
        name = os.path.split(contam_file)[-1].replace("_good.fasta", "")
        if name not in all_names.keys():
            print("Can't match name for no_contam file with parent file name")
            print("name", name)
            print("not in", all_names.keys())
            sys.exit()

        contam_rem_d = fasta_to_dct(contam_file)
        total_contam_rem = str(len(contam_rem_d.keys()))
        stats_d[name].append(total_contam_rem)

        freq = 1

        num_consensus_seqs = int(total_contam_rem)
        p = freq/100
        var_detection_limit = round((1 - ((1 - p) ** num_consensus_seqs))*100, 2)
        stats_d[name].append(str(var_detection_limit))
        var_freq_with_95perc_prob = round((1 - (0.05 ** (1 / num_consensus_seqs))) * 100, 3)
        stats_d[name].append(str(var_freq_with_95perc_prob))

    # write the stats to the log file
    with open(outfile, 'w') as handle:
        # write the headers
        headers_to_write = ",".join(stats_d["headers"])
        handle.write(headers_to_write + "\n")
        # write the stats
        for sequence_file in stats_d.keys():
            if sequence_file != "headers":
                stats_list = stats_d[sequence_file]
                # if sample failed at some point, add NaN's
                if len(stats_list) < len(stats_d["headers"]):
                    nan_to_add = 6 - len(stats_list)
                    for i in range(nan_to_add):
                        stats_list.append("NaN")
                lines_to_write = ",".join(str(x) for x in stats_list)
                handle.write(lines_to_write + "\n")

    print("Stats calculations on your NGS samples are complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='calculate stats on sample processing',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--inpath', default=argparse.SUPPRESS, type=str,
                        help='The path to where the output file will be created', required=True)
    parser.add_argument('-o', '--outfile', default=argparse.SUPPRESS, type=str,
                        help='The path and name for the stats output file', required=True)

    args = parser.parse_args()
    inpath = args.inpath
    outfile = args.outfile

    main(inpath, outfile)
