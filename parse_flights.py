import os
import codecs
import csv
from time_utils import calculate_time_delta, validate_layover
from Flights import build_trip


def build_flights_dict(database):
    """takes list of all input files and creates
    a data dictionary of all possible flight connections that fulfill the layover rule
    :param database list of file paths
    :returns dictionary with connections
    """
    flights_dict = dict()
    for file_path in database:
        if os.path.isfile(file_path):
            with codecs.open(file_path) as data_file:
                data = csv.reader(data_file)
                header_row = next(data)
                if header_row[0] != "flight_no":
                    print(f"File {file_path} has incorrect header line")
                else:
                    x = {tuple(row): list() for row in data if tuple(row) not in flights_dict}
                    flights_dict.update(x)
                    data_file.seek(1)
                    data = csv.reader(data_file)
                    for row in data:
                        if len(row) != 8:
                            print(f"Incorrect row: {row}")
                            del flights_dict[tuple(row)]
                        else:
                            connecting_flight = tuple(row)
                            for key in flights_dict.keys():
                                if key[2] == connecting_flight[1]:
                                    layover_time = calculate_time_delta(key[4], connecting_flight[3])
                                    if validate_layover(layover_time):
                                        flights_dict[key].append(connecting_flight)
    return flights_dict


def find_all_flights(flights_graph, origin, destination, f=[], visited=[]):
    """searches for all possible flights from A to B using the valid flights map

    :param flights_graph dictionary with valid flight connections
    :param origin starting flight
    :param destination final airport code
    :param f current path
    :param visited already visited airports to avoid cycles
    :returns list of all valid flights
    """
    f = f + [origin]
    visited.append(origin[1])
    visited = list(set(visited))
    if origin[2] == destination:
        return [f]
    if flights_graph.get(origin) is None:
        return []
    flights = []
    for node in flights_graph.get(origin):
        if node not in f and node[2] not in visited:
            new_flights = find_all_flights(flights_graph, node, destination, f, visited)
            for new_flight in new_flights:
                flights.append(new_flight)
    return flights


def build_trip_list(args):
    """builds a list of all trips from given origin to destination that comply with [any] extra search requirements
    :param args Arguments class that represents all arguments specified by user
    :returns list of Flight object (each item in list represent a simple origin - [any stops] - destination connection
    """
    flights_dict = build_flights_dict(args.input_file)
    input_flights = [flight for flight in flights_dict if flight[1] == args.origin]
    destinations = list(set([flight[2] for flight in flights_dict]))
    if not input_flights or args.destination not in destinations:
        print(f"Unknown origin: {args.origin} or destination: {args.destination} - no flights found.")
        exit(-1)
    else:
        all_flights = []
        for starting_flight in input_flights:
            found_flights = find_all_flights(flights_dict, starting_flight, args.destination)
            if len(found_flights) != 0:
                for flight in found_flights:
                    trip = build_trip(flight, args.optional_dict())
                    if trip is not None:
                        all_flights.append(trip)
        all_flights = sorted(all_flights, key=lambda flight: flight.total_price)
        return all_flights
