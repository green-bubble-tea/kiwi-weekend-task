from argparse import ArgumentParser
import json


class Arguments:
    """namespace class for argument parser"""

    def __init__(self):
        self.origin = ""
        self.destination = ""
        self.input_file = []
        self.output_dir = None
        self.bags = None
        self.max_stops = None
        self.max_price = None
        self.max_base_price = None
        self.max_bag_price = None
        self.specific_city = None
        self.direct_only = False

    def io_dict(self):
        return {
            "origin": self.origin,
            "destination": self.destination,
            "input_file": self.input_file,
            "output_dir": self.output_dir
        }

    def optional_dict(self):
        return {
            "bags": self.bags,
            "max_stops": self.max_stops,
            "max_price": self.max_price,
            "max_base_price": self.max_base_price,
            "max_bag_price": self.max_bag_price,
            "specific_city": self.specific_city,
            "direct_only": self.direct_only
        }

    def check_exclusive_arguments(self):
        if self.direct_only and any(i is not None for i in [self.specific_city, self.max_stops]):
            raise ValueError("Flight can't be direct_only and have a mid-stop or max stops")

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)


def get_arg_parser():
    """console argument parser builder

    :returns ArgParser instance with all required and optional parameters
    """
    parser = ArgumentParser(description="Plan your trip!")
    # required arguments
    parser.add_argument("input_file", nargs='+', help="Path to input .csv file")
    parser.add_argument("origin", type=str, help="Origin code")
    parser.add_argument("destination", type=str, help="Destination code")

    # optional arguments
    parser.add_argument("--bags", type=int, required=False,
                        help="Number of bags")
    parser.add_argument('--max_stops', type=int, required=False,
                        help="Maximum number of stops for the trip.")
    parser.add_argument('--max_price', type=float, required=False,
                        help="Maximum price for the trip.")
    parser.add_argument('--max_base_price', type=float, required=False,
                        help="Maximum base price for the single flight.")
    parser.add_argument('--max_bag_price', type=int, required=False,
                        help="Maximum price for a bag in single flight.")
    parser.add_argument('--specific_city', type=str, required=False,
                        help="Trips that include specific airport code.")
    parser.add_argument("--direct_only", action="store_true",
                        help="Only direct flights.")
    parser.add_argument('--output_dir', type=str, required=False,
                        help="Save output to file or write it to console.")
    return parser


def parse_arguments():
    parser = get_arg_parser()
    args = parser.parse_args(namespace=Arguments())
    return args if not args.check_exclusive_arguments() else None
