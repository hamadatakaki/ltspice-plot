import argparse
from pathlib import Path
import sys

from ltspice.reader.Polar import LTspicePolarReader
from ltspice.drawer.SimpleFreq import SimpleFreqDrawer
from ltspice.utils import load_yaml


def check_args(args):
    confpath = Path(args.config) if args.config is not None else None
    config = None

    if bool(confpath) and confpath.exists():
        config = load_yaml(confpath)
    else:
        print(f"[error] config `{confpath}` not exist.")
        sys.exit(1)

    return LTspicePolarReader(args.input_txt), config


def main(args):
    reader, config = check_args(args)

    drawer = SimpleFreqDrawer(reader, args.output_image, config)
    drawer.save_figure()
    drawer.logging()


if __name__ == "__main__":
    desc_msg = "plotting frequency characteristics (amplitudes, phases)."
    parser = argparse.ArgumentParser(description=desc_msg)

    parser.add_argument(
        "-i", "--input_txt", required=True, help="LTspice export data path."
    )
    parser.add_argument(
        "-o", "--output_image", required=True, help="Plot image save path."
    )
    parser.add_argument("-c", "--config", required=False, help="Plot configure.")

    args = parser.parse_args()

    main(args)
