from argparse import ArgumentParser
from json import load, dump


def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--input", type=str, help="pre existing config file")
    ap.add_argument("-o", "--output", type=str, help="outfile")
    ap.add_argument("-gu", "--github-username", help="github username")
    a = ap.parse_args()




if __name__ == '__main__':
    main()
