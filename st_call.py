import pandas as pd
import hashlib
import argparse
from pathlib import Path

__author__ = 'Dillon Barker'

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--calls',
                        type=Path,
                        required=True,
                        help='Input calls CSV')


    parser.add_argument('--output',
                        type=Path,
                        required=True,
                        help='Output directory')

    parser.add_argument('--delimiter',
                        help='Input table delimiter')

    return parser.parse_args()


def call_sts(table):

    def call_st(row):

        h = hashlib.md5()

        row_string = ' '.join(map(str, row)).encode('utf-8')

        h.update(row_string)

        return h.hexdigest()

    sts = table.apply(call_st, axis=1)

    return sts


def divide_files(table, outpath):

    sts = call_sts(table)

    strain_st = pd.DataFrame({'ST': sts})

    st_definitions = table.copy(deep=True)

    headers = list(st_definitions.columns)

    st_definitions['ST'] = sts

    st_definitions = st_definitions.reindex_axis(['ST'] + headers, axis=1)
    st_definitions = st_definitions.drop_duplicates()

    st_definitions.to_csv(outpath / 'st_definitions.tsv',
                          sep='\t', index=False)

    strain_st.to_csv(outpath / 'strain_st.tsv', sep='\t')

def main():

    args = arguments()

    table = pd.read_csv(args.calls, header=0, index_col=0, sep=args.delimiter)

    divide_files(table, args.output)

if __name__ == '__main__':
    main()

