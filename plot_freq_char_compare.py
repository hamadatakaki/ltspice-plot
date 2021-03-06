import argparse
from pathlib import Path
import sys

from ltspice.drawer.CompareFreqBWChebysev import CompareFreqCharsDrawer
from ltspice.reader.Polar import LTspicePolarReader
from ltspice.utils import load_yaml


def check_args(args):
    confpath = Path(args.config) if args.config is not None else None
    config = None

    if bool(confpath) and confpath.exists():
        config = load_yaml(confpath)
    else:
        print(f"[error] config `{confpath}` not exist.")
        sys.exit(1)

    bw = LTspicePolarReader(args.butter_worth)
    che = LTspicePolarReader(args.chebyshev)

    return bw, che, config


def main(args):
    bw_reader, ch_reader, config = check_args(args)

    drawer = CompareFreqCharsDrawer(bw_reader, ch_reader, args.output_image, config)
    drawer.save_figure()
    drawer.logging()


if __name__ == "__main__":
    desc_msg = "plotting frequency characteristics (amplitudes, phases)."
    parser = argparse.ArgumentParser(description=desc_msg)

    parser.add_argument(
        "-bw", "--butter_worth", required=True, help="Butter-Worth exported txt data."
    )

    parser.add_argument(
        "-ch", "--chebyshev", required=True, help="Chebyshev exported txt data."
    )

    parser.add_argument(
        "-o", "--output_image", required=True, help="Plot image save path."
    )
    parser.add_argument("-c", "--config", required=False, help="Plot configure.")

    args = parser.parse_args()

    main(args)
