import json
from time_utils import calculate_time_delta


class Flight:
    """single flight class"""

    def __init__(self, row):
        self.flight_no, self.origin, self.destination, self.departure, self.arrival, self.base_price, self.bag_price, self.bags_allowed = row
        self.base_price = float(self.base_price)
        self.bag_price = int(self.bag_price)
        self.bags_allowed = int(self.bags_allowed)

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)


class Trip:
    """output valid trip class"""

    def __init__(self, flights):
        self.flights = flights
        self.bags_allowed = min([flight.bags_allowed for flight in self.flights])
        self.bags_count = 0
        self.destination = flights[-1].destination
        self.origin = flights[0].origin
        self.total_price = sum([flight.base_price + float(flight.bag_price * self.bags_count)
                                for flight in self.flights])
        self.travel_time = str(calculate_time_delta(self.flights[0].departure, self.flights[-1].arrival))

    def set_bags_count(self, bags_count):
        self.bags_count = bags_count
        # update the total price
        self.total_price = sum([flight.base_price + float(flight.bag_price * self.bags_count)
                                for flight in self.flights])

    def __repr__(self):
        return json.dumps({
            "flights": [json.loads(str(flight)) for flight in self.flights],
            "bags_allowed": self.bags_allowed,
            "bags_count": self.bags_count,
            "destination": self.destination,
            "origin": self.origin,
            "total_price": self.total_price,
            "travel_time": self.travel_time
        }, indent=4)


def build_trip(flight_list, optional_args):
    """checks if found path meets the additional criteria
    :param flight_list valid list of flights from A to B
    :param optional_args dict with optional args
    :returns trip if yes or no criteria given or None
    """

    trip = Trip([Flight(connection) for connection in flight_list])

    def bags_valid(bags_count):
        if bags_count is not None:
            if trip.bags_allowed >= bags_count:
                trip.set_bags_count(bags_count)
                return True
        else:
            return False

    def max_stops_valid(max_stops):
        return len(trip.flights) - 1 <= max_stops

    def max_price_valid(max_price):
        return trip.total_price <= max_price

    def specific_city_valid(city_code):
        return city_code in [flight.origin for flight in trip.flights]

    def direct_only_valid(direct_only):
        return len(trip.flights) == 1 if direct_only else True

    def max_base_price_valid(max_base_price):
        return max(flight.base_price for flight in trip.flights) <= max_base_price

    def max_bag_price_valid(max_bag_price):
        return max(flight.bag_price for flight in trip.flights) <= max_bag_price

    is_valid = True
    for key, value in optional_args.items():
        function_name = key + "_valid"
        if value is not None:
            try:
                ret_value = locals()[function_name](value)
                if not ret_value:
                    is_valid = False
            except KeyError:
                print(f"Key error: bad argument {key}, cannot find corresponding validating function")
    return trip if is_valid else None
