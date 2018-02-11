#!/bin/usr/env python
# -*- coding: utf-8 -*-
import sys
from disp import disp_main


def main():
    print("Select process mode [disp]")
    proc_mode = input()

    if proc_mode == "disp":
        disp_main()
    elif proc_mode == "mean":
        pass
    else:
        sys.stderr.write('Error: The mode is not defined.\n')

    print('Normally ended.')

    return


if __name__ == "__main__":
    main()
