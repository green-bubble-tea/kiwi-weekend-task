import codecs
import os

from arg_parser import parse_arguments
from parse_flights import build_trip_list

OUT_FILE = "result.json"

if __name__ == "__main__":
    try:
        args = parse_arguments()
        all_flights = build_trip_list(args)
        print(all_flights)
        # print(len(all_flights))
        if args.output_dir is not None:
            output_path = os.path.join(args.output_dir, OUT_FILE)
            try:
                with codecs.open(output_path, "w") as output_file:
                    output_file.write(str(all_flights))
            except FileNotFoundError:
                output_path = os.path.join("data", OUT_FILE)
                with codecs.open(output_path, "w") as output_file:
                    output_file.write(str(all_flights))
    except ValueError as err:
        print(err)
