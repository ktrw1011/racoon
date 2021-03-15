import argparse
from os import name
from racoon.experiment import ExpManager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name")

    args = parser.parse_args()

    manger = ExpManager()

    manger.init(
        name=name
    )

if __name__ == '__main__':
    main()