import argparse
import sys
from pathlib import Path

import pandas as pd


def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--column1', '-1',
                        required=True,
                        help='First cluster column to compare')

    parser.add_argument('--column2', '-2',
                        required=True,
                        help='Second cluster column to compare')

    parser.add_argument('--clusters',
                        type=Path,
                        required=True,
                        help='Tab-delimited cluster table')

    return parser.parse_args()


def load_data(cluster_path):

    clusters = pd.read_csv(cluster_path, header=0, index_col=0, sep='\t')

    return clusters


def filter_contingency_table(clusters1, clusters2, clusters):

    contingency_table = pd.crosstab(clusters[clusters2], clusters[clusters1])

    rows = contingency_table.iterrows()

    splitting_rows = (row for row in rows if sum(row[1]) != max(row[1]))

    return splitting_rows


def analyze_split(row):

    merged_name, values = row

    *donors, recipient = [x for x in sorted(zip(values, values.index)) if x[0]]

    donor_sizes, donor_names = zip(*donors)

    recipient_size, recipient_name = recipient

    output = {
        'merged': merged_name,
        'donors': donor_names,
        'donor_sizes': donor_sizes,
        'donor_size_total': sum(donor_sizes),
        'recipient': recipient_name,
        'recipient_size': recipient_size,
        'total': sum(donor_sizes) + recipient_size
    }

    return output


def analyze(clusters1, clusters2, clusters):

    splitting_rows = filter_contingency_table(clusters1, clusters2, clusters)

    analysis = [analyze_split(row) for row in splitting_rows]

    return analysis


def report(analysis):

    report_df = pd.DataFrame(analysis, columns=('merged',
                                                'donors',
                                                'donor_sizes',
                                                'donor_size_total',
                                                'recipient',
                                                'recipient_size',
                                                'total'))

    report_df.to_csv(path_or_buf=sys.stdout, sep='\t', index=False)


def main():

    args = arguments()

    data = load_data(args.clusters)

    analysis = analyze(args.column1, args.column2, data)

    report(analysis)


if __name__ == '__main__':
    main()
