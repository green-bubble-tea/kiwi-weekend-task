#Kiwi 10-year anniversary Python weekend

##Project structure 
    .
    ├── data                    # Data files provided by Kiwi
        ├────example0.csv       # sample data #0
        ├────example1.csv       # sample data #1
        ├────example2.csv       # sample data #2
        ├────example3.csv       # sample data #3
        ├────result.json        # sample output from a search mention below 
    ├── Flights.py              # Flight and Trip class representation and a trip validation method
    ├── utils.py                # all the logic and algorithms that are used to provide the solution
    ├── main.py                 # simple command line interface
    └── README.md

## Simple run 

    cd kiwi-task
    python main.py <paths to your files> OR data/example[0-3].csv origin destination

## Optional arguments 
To narrow down your flight list (it may be close to 200 possible trips) you can enter any number of optional arguments:

| Argument name      | type  | Description                                                     | Notes                                                                                                            |
|--------------------|-------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| `--bags`           | int   | How many bags do you travel with?                               | default to 0                                                                                                     |
| `--max_bag_price`  | int   | How much are you willing to pay for a bag in a single flight?   |                                                                                                                  |
| `--max_base_price` | float | How much are you willing to pay for a single flight?            |                                                                                                                  |
| `--bags_count`     | int   | Show me only flights that allow up to X bags                    |                                                                                                                  |
| `--max_price`      | float | How much are you willing to pay for the whole trip?             |                                                                                                                  |
| `--direct_only`    | bool  | Show me only direct flights                                     |                                                                                                                  |
| `--max_stops`      | int   | How many additional transfers are you willing to take?          | mutually exclusive with direct_only                                                                              |
| `--specific_city`  | str   | Do you want to catch a connecting flight from specific airport? | mutually exclusive with direct_only                                                                              |
| `--output_dir`     | str   | Do you also want to save your output to external .json file?    | if specified dir doesn't exist, but output_dir is present, the output will be saved to current working directory |

Note: if you put too many or too strict you may end up with zero results :)

## Sample output
User: I want to fly from WIW to ECV with 1 bag, but I don't wish to take any connecting flights 
(I once had to catch a connection in Charles de Gaulle airport, and it scarred me for life...)
Run:
```commandline
    python main.py data/example0.csv WIW ECV --direct_only --bags=1
```
And the output will be:
```json
[{
    "flights": [
        {
            "flight_no": "ZH151",
            "origin": "WIW",
            "destination": "ECV",
            "departure": "2021-09-01T07:25:00",
            "arrival": "2021-09-01T12:35:00",
            "base_price": 245.0,
            "bag_price": 12,
            "bags_allowed": 2
        }
    ],
    "bags_allowed": 2,
    "bags_count": 1,
    "destination": "ECV",
    "origin": "WIW",
    "total_price": 257.0,
    "travel_time": "5:10:00"
}, {
    "flights": [
        {
            "flight_no": "ZH151",
            "origin": "WIW",
            "destination": "ECV",
            "departure": "2021-09-02T07:25:00",
            "arrival": "2021-09-02T12:35:00",
            "base_price": 245.0,
            "bag_price": 12,
            "bags_allowed": 2
        }
    ],
    "bags_allowed": 2,
    "bags_count": 1,
    "destination": "ECV",
    "origin": "WIW",
    "total_price": 257.0,
    "travel_time": "5:10:00"
}, {
    "flights": [
        {
            "flight_no": "ZH151",
            "origin": "WIW",
            "destination": "ECV",
            "departure": "2021-09-06T07:25:00",
            "arrival": "2021-09-06T12:35:00",
            "base_price": 245.0,
            "bag_price": 12,
            "bags_allowed": 2
        }
    ],
    "bags_allowed": 2,
    "bags_count": 1,
    "destination": "ECV",
    "origin": "WIW",
    "total_price": 257.0,
    "travel_time": "5:10:00"
}, {
    "flights": [
        {
            "flight_no": "ZH151",
            "origin": "WIW",
            "destination": "ECV",
            "departure": "2021-09-11T07:25:00",
            "arrival": "2021-09-11T12:35:00",
            "base_price": 245.0,
            "bag_price": 12,
            "bags_allowed": 2
        }
    ],
    "bags_allowed": 2,
    "bags_count": 1,
    "destination": "ECV",
    "origin": "WIW",
    "total_price": 257.0,
    "travel_time": "5:10:00"
}]
```
##How it's done 
As stated above, the program takes at least one path to .csv file, an origin code and destination code. 
After the arguments are parsed and validated it's time to build the main structure.
Given the first entry (path) it builds the data structure - a dictionary, where keys are rows from csv, but converted to tuples and values are empty lists (so far).
It then resets and traverses the csv data again to find the connecting flights for each key that fulfill the layover rule and appends it to value list.
In the end of this operation we have structure like that: 
```python
flight_dict = {
    ("ABC11", "ABC", "DEF", "departure", "arrival", ...): [("DEF12", "DEF", "GHI", "departure1",...), ("DEF31", "DEF", "KLM",...)]
}
```
Knowing where we want to go (origin, destination), we get all the flights that start from the origin airport. 
Additionally we filter all possible destination codes to see if the search parameters are valid, i.e it's even possible to fly this route. 
If not, the error message is shown and the program exits. 
In the opposite case, we search for all possible flights on this route; then, for each found flight we apply the validating criteria (if there are any) and if they're met, the route is returned as Trip instance. 
For the final touch, we apply output rules - either write the output structure to console (pretty print with indentations etc.) or to chosen output file. 
In the second case, the console shows minimal message for the user, such as: where the file is stored (full path ready to copy and paste), how many flights were found and how much time it took. 

##Time measurements
The solution was tested on Dell Precision 7520, Windows 10, 16GB RAM, Intel core i7. 
My shoe size is 37, I am 167cm tall wearing glasses with -1.5 lenses :) 
I did my best trying to simplify and sped up the algorithms and here are the time results:
1. For the simple search (one small database, direct only flights):
```commandline
    python main.py data/example0.csv WIW RFZ --direct_only 
```
> Found 3 flights that meet the criteria
> 
> That took 0.02 seconds.

2. For the largest database and no narrowing the flights down 

```commandline
    python main.py data/example0.csv data/example1.csv data/example2.csv data/example3.csv WUE JBN 
```
> Found 182 flights that meet the criteria
> 
> That took 3.64 seconds.


==================================

##Corrections

Refactoring log after the initial feedback:
* utils script was split into parse_flights - script designed only to deal with finding, filtering and building flight connections, time_utils - functions related to working with timestamps and arg_parser - parsing cli arguments
* main.py was cleared of all the code except for calling the parsing functions and showing/saving the output
* fixed bug with bags_count deleted the "max_bas" argument and applied the 0 bag condition (previously it was incorrectly copied from bags_allowed)
* enhanced the time parsing and management using proper datetime functions/classes instead of working on them "manually"
