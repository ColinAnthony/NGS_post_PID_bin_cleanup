#!/usr/bin/python
from __future__ import print_function
from __future__ import division
import os
import argparse


__author__ = 'Colin Anthony'


def main(your_path, gene_region, fnames):
    '''
    create folder structure for a sequencing project
    :param your_path: (str) path to where the folders should be make
    :param gene_region: (str) gene region being sequenced
    :param fnames: (list) list of top level directories to populate
    :return:
    '''

    third_level_dirs = ['1raw', '2consensus', '3cleaned', '4aligned', '5haplotype', '6analysis']
    fourth_level_dirs = ['aa_frq', 'divergence', 'entropy', 'glycans', 'loops', 'tree']

    for fname in fnames:
        print(your_path, fname)
        top_level_dir = os.path.join(your_path, str(fname))
        second_level_dir = os.path.join(top_level_dir, gene_region)

        # make top level directory (usually participant or study)
        if not os.path.exists(top_level_dir):
            os.makedirs(top_level_dir)

        # make second level directory (usually gene region)
        if not os.path.exists(second_level_dir):
            os.makedirs(second_level_dir)

        # make third level directories (analysis directories)
        for folder in third_level_dirs:
            if folder == '6analysis':
                for nested_folder in fourth_level_dirs:
                    set_path = os.path.join(second_level_dir, folder)
                    if not os.path.exists(set_path):
                        make_folder = os.path.join(set_path, nested_folder)
                        os.makedirs(make_folder)
            else:
                make_folder = os.path.join(second_level_dir, folder)
                if not os.path.exists(make_folder):
                    os.makedirs(make_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create folder structure for NGS data cleanup/analysis',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--path', default=argparse.SUPPRESS, type=str,
                        help='The path where the folders will be created', required=True)
    parser.add_argument('-g', '--gene_region', default=argparse.SUPPRESS, type=str,
                        help='the genomic region being sequenced', required=True)
    parser.add_argument('-n', '--name', default=argparse.SUPPRESS, type=list,
                        help='the name of the participant', required=True)

    args = parser.parse_args()
    path = args.path
    gene_region = args.gene_region
    name = args.name

    main(path, gene_region, name)
