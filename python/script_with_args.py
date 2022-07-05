import argparse


def parse_args():
    """Parse script arguments."""
    parser = argparse.ArgumentParser(description="Perform graph analyses")
    parser.add_argument(
        "--add-fields",
        nargs="+",
        help="Add new fields to existing documents",
        default=False,
    )
    parser.add_argument(
        "--num-fields",
        help="The number of fields to process",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-i",
        "--input",
        action="store",
        help="Input path",
        default="./data/input_file.csv",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        help="Output path",
        default="../models/pipeline.pkl",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Run in test mode",
        default=False,
    )
    # for when this script gets moved to Docker; for now these args aren't used
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--local",
        action="store_true",
        help="Run script locally",
        default=False,
    )
    group.add_argument(
        "--docker",
        action="store_true",
        help="Run script in Docker",
        default=False,
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    test_mode = True if args.test else False
    
    input_path = args['input']
    output_path = args['output']

    if args.local:
        host = "localhost"
    elif args.docker:
        host = cfg.NEO4J_HOSTNAME
    