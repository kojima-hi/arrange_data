#!/bin/usr/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np


def get_stypes(path):
    stypes = []
    with open(path, 'r') as f:
        for line in f:
            stypes.append(line.strip())

    return stypes


def get_input_path(stypes, input_file, const_stypes_str):
    input_paths = []

    # extract types in match
    const_stypes = const_stypes_str.split()
    new_stypes = []
    for const_stype in const_stypes:
        for stype in stypes:
            if const_stype in stype:
                new_stypes.append(stype)

        stypes = new_stypes
        new_stypes = []

    # make input paths
    stypes.sort()
    for stype in stypes:
        input_paths.append(os.path.join(stype, input_file))

    return input_paths


def get_output_path(var_stype, const_stypes_str, output_dir):

    # make structure types list
    stypes = const_stypes_str.split()
    var_stype_rev = var_stype + 'x'
    stypes.append(var_stype_rev)
    stypes.sort()

    stype_str = '_'.join(stypes)

    output_file = stype_str + '.dat'
    output_path = os.path.join(output_dir, output_file)
    return output_path


def extract_variable(path, var_stype):

    stype_str = (path.split('/'))[0]
    stypes = stype_str.split('_')

    for stype in stypes:
        if var_stype in stype:
            var = int(stype[1:])

    return var


def extract_disp_data(input_paths, charge_file, var_stype):
    data_df = None

    extract_numbers = (pd.read_csv(charge_file, header=None, dtype=np.int32)).as_matrix() # ndarray
    extract_numbers = extract_numbers.flatten() - 1
    for input_path in input_paths:
        var = extract_variable(input_path, var_stype)

        charges = pd.read_csv(input_path, header=None, dtype=np.float32)
        charges = (charges.rename(columns={0: var})).T

        if data_df is not None:
            data_df = pd.concat([data_df, charges], axis=0)
        else:
            data_df = charges

    return data_df


def get_setting():
    # Setting
    print('Write followings...')
    print('List file of stypes:')
    type_file = input()

    print('Input file name (not include directory but only):')
    input_file = input()

    print('Variable in type names:')
    var_stype = input()

    print('Constants in type names in one line (e.g. \"b1\" or \"b1 c2\"):')
    const_stypes_str = input()

    print('File name of extracting charge numbers:')
    charge_file = input()

    print('Output directory (not include file name but only, file name is automatically named from variable and constants.):')
    output_dir = input()

    return type_file, input_file, var_stype, const_stypes_str, charge_file, output_dir


def write_data(path, df):
    df.to_csv(path, header=None, float_format='%9.6f')
    return


def disp_main():
    # Setting
    type_file, input_file, var_stype, const_stypes_str, charge_file, output_dir = get_setting()

    # Main
    stypes = get_stypes(type_file)

    input_paths = get_input_path(stypes, input_file, const_stypes_str)

    data_df = extract_disp_data(input_paths, charge_file, var_stype)

    output_path = get_output_path(var_stype, const_stypes_str, output_dir)

    write_data(output_path, data_df)

    return


def main():
    return


if __name__ == "__main__":
    main()