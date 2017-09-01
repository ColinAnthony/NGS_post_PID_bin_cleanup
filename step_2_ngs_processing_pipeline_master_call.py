#!/usr/bin/python3
from __future__ import print_function
from __future__ import division
import os
from shutil import copyfile
import argparse
import subprocess
from glob import glob
from Bio import SeqIO


__author__ = 'Colin Anthony'


def fasta_to_dct(fn):
    '''
    :param fn: (str)infile name
    :param frame: (int) reading frame (1, 2 or 3)
    :return: (dict) dictionary of names and sequences
    '''
    dct = {}
    for seq_record in SeqIO.parse(open(fn), "fasta"):
        dct[seq_record.description.replace(" ", "_").upper()] = str(seq_record.seq).replace("-", "").upper()
    return dct


def main(path, name, script_folder, gene_region, fwd_primer, cDNA_primer, frame, stops, length, envelope):

    # initialize the log file
    logfile = os.path.join(path, (gene_region + "_logfile.txt"))
    with open(logfile, 'w') as handle:
        handle.write("Log File,{0}_{1}\n".format(name, gene_region))

    # remove contaminating sequences
    contam_removal_script = os.path.join(script_folder, "contam_removal.py")
    raw_fastqs = os.path.join(path, '0raw', "*R1.fastq")
    contam_removed_path = os.path.join(path, '1contam_removal')

    for read1 in glob(raw_fastqs):
        read2 = read1.replace("_R1.fastq", "_R2.fastq")
        cmd1 = 'python3 {0} -r1 {1} -r2 {2} -o {3}'.format(contam_removal_script,
                                                             read1,
                                                             read2,
                                                             contam_removed_path)

        #subprocess.call(cmd1, shell=True)

    # run the call_MotifBinner script which will floop over fastq files in the target folder
    cln_fastq_inpath = os.path.join(path, '1contam_removal')
    cons_outpath = os.path.join(path, '2consensus', 'binned')
    motifbinner = os.path.join(script_folder, 'call_motifbinner.py')
    cmd2 = 'python3 {0} -i {1} -o {2} -f {3} -r {4} -l {5}'.format(motifbinner,
                                                                   cln_fastq_inpath,
                                                                   cons_outpath,
                                                                   fwd_primer,
                                                                   cDNA_primer,
                                                                   logfile)

    #subprocess.call(cmd2, shell=True)

    # copy data from nested binned folders into 2consensus folder
    print("Copy fastq files from nested folders to '2consensus' folder")
    path_to_consensus = os.path.join(path, '2consensus/binned/*/n028_cons_seqLength/*kept_cons_seqLength.fastq')
    fastq_path = os.path.join(path, '2consensus')
    for cons_file in glob(path_to_consensus):
        if not os.path.isfile(cons_file):
            print("consensus files do not exist")
        old_path, old_name = os.path.split(cons_file)
        new_name = os.path.join(fastq_path, old_name)
        copyfile(cons_file, new_name)

    # convert copied fastq to fasta
    print("Converting fastq to fasta")
    search_path = os.path.join(fastq_path, '*.fastq')
    for fastq in glob(search_path):
        fasta = fastq.replace("fastq", "fasta")
        cmd3 = 'seqmagick convert {0} {1}'.format(fastq,
                                                  fasta)

        subprocess.call(cmd3, shell=True)

    # remove the copied fastq files
    print("Removing the copied fastq files")
    remove_fastq = search_path
    for old_fastq_copy in glob(remove_fastq):
        os.remove(old_fastq_copy)

    # call remove bad sequences
    print("Removing 'bad' sequences")
    remove_bad_seqs = os.path.join(script_folder, 'remove_bad_sequences.py')
    clean_path = os.path.join(path, '3cleaned')
    fasta_path = os.path.join(fastq_path, '*.fasta')

    for fasta_file in glob(fasta_path):
        if stops:
            cmd4 = 'python3 {0} -i {1} -o {2} -f {3} -s {4} -l {5} -lf {6}'.format(remove_bad_seqs,
                                                                                   fasta_file,
                                                                                   clean_path,
                                                                                   frame,
                                                                                   stops,
                                                                                   length,
                                                                                   logfile)
        else:
            cmd4 = 'python3 {0} -i {1} -o {2} -f {3} -l {4} -lf {5}'.format(remove_bad_seqs,
                                                                            fasta_file,
                                                                            clean_path,
                                                                            frame,
                                                                            length,
                                                                            logfile)
        if os.path.exists(logfile):
            with open(logfile, 'a') as handle:
                handle.write("\nremove_bad_sequences commands:\n{}\n".format(cmd4))

        subprocess.call(cmd4, shell=True)

    # get the HXB2 sequence for the gene region
    hxb2_file = os.path.join(script_folder, "HXB2_seqs.fasta")
    hxb2 = fasta_to_dct(hxb2_file)
    hxb2_gene = "HXB2_" + gene_region.split("_")[0]
    hxb2_seq = hxb2[hxb2_gene]

    # cat all cleaned files into one file + the relevant HXB2 sequence
    print("merging all cleaned fasta files into one file")
    all_clean_path = os.path.join(path, '3cleaned')
    clean_name = name + "_" + gene_region + "_all.fasta"
    all_cleaned_outname = os.path.join(all_clean_path, clean_name)
    cleaned_files = os.path.join(clean_path, '*clean.fa')
    with open(all_cleaned_outname, 'w') as outfile:
        outfile.write(">{0}\n{1}\n".format(hxb2_gene, hxb2_seq))
        for fasta_file in glob(cleaned_files):
            with open(fasta_file) as infile:
                for line in infile:
                    outfile.write(line + "\n")

    # move concatenated file to 4aligned
    print("moving concatenated file to 4aligned folder")
    aln_path = os.path.join(path, '4aligned')
    move_file = os.path.join(aln_path, clean_name)
    copyfile(all_cleaned_outname, move_file)

    # call alignment script
    print("Aligning the sequences")
    to_align = move_file
    inpath, fname = os.path.split(to_align)
    fname = fname.replace(".fasta", "_aligned.fasta")
    if envelope is not None:
        align_all = os.path.join(script_folder, 'align_all_env_samples.py')

        cmd5 = 'python3 {0}  -i {1} -o {2} -l {3}'.format(align_all, to_align, aln_path, fname, envelope)
    else:
        align_all = os.path.join(script_folder, 'align_all_samples.py')
        cmd5 = 'python3 {0}  -i {1} -o {2} -n {3}'.format(align_all, to_align, aln_path, fname)

    subprocess.call(cmd5, shell=True)


    # call funcion to calculate sequencing stats
    print("Calculating alignment stats")
    call_stats_calc = os.path.join(script_folder, 'ngs_stats_calculator.py')
    stats_outfname = (name + "_" + gene_region + '_sequencing_stats.csv')
    stats_outpath = os.path.join(path, stats_outfname)
    cmd6 = 'python3 {0} -i {1} -o {2}'.format(call_stats_calc, path, stats_outpath)
    subprocess.call(cmd6, shell=True)

    print("The sample processing has been completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Call make_folders script BEFORE running this script '
                                                 'Then copy your data into the /1raw/ folder'
                                                 'This script runs the NGS data processing pipeline. '
                                                 'It is a good idea to run this script using screen or nohup',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--path', default=argparse.SUPPRESS, type=str,
                        help='The path to the gene region subfolder (GAG_1/ or env_C1C2/ or POL_1/...)', required=True)
    parser.add_argument('-n', '--name', default=argparse.SUPPRESS, type=str,
                        help='the prefix name of your outfile', required=True)
    parser.add_argument('-g', '--gene_region', default=argparse.SUPPRESS, type=str,
                        help='the genomic region being sequenced, '
                             'valid options: GAG_1/GAG_2/ENV_C1C2/POL_1/NEF_1 etc..', required=True)
    parser.add_argument('-sf', '--script_folder', default=argparse.SUPPRESS, type=str,
                        help='the path to the folder containing the pipeline scripts', required=True)
    parser.add_argument('-f', '--fwd_primer', default=argparse.SUPPRESS, type=str,
                        help='The fwd primer for these samples (eg: NNNNGGAAATATGGAAAGGAAGGAC)', required=True)
    parser.add_argument('-r', '--cDNA_primer', default=argparse.SUPPRESS, type=str,
                        help='The cDNA primer for these samples (eg: NNNNNNNNNNNTCTTCTAATACTGTATCATCTG)', required=True)
    parser.add_argument('-fr', '--frame', type=int,
                        help='The reading frame (1, 2 or 3)', required=False)
    parser.add_argument('-s', '--stops', default=False, action='store_true',
                        help='Remove sequences with stop codons?)', required=False)
    parser.add_argument('-l', '--length', type=int,
                        help='The minimum read length)', required=False)
    parser.add_argument('-e', '--envelope', default=None, nargs="+",
                        help='If your sequences are of HIV envelope, which V-loops are in the sequence?'
                             '(eg: V1 V2) (options include: V1, V2 , V3, V4, V5)', required=False)

    args = parser.parse_args()
    path = args.path
    name = args.name
    script_folder = args.script_folder
    gene_region = args.gene_region
    fwd_primer = args.fwd_primer
    cDNA_primer = args.cDNA_primer
    frame = args.frame
    stops = args.stops
    length = args.length
    envelope = args.envelope

    main(path, name, script_folder, gene_region, fwd_primer, cDNA_primer, frame, stops, length, envelope)
