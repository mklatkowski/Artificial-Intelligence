import pandas as pd
import csv
import re
from datetime import datetime
import pickle

hour_format = "%H:%M:%S"

class Edge:
    def __init__(self, line, departure_time, arrival_time, start_stop, end_stop):
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.start_stop = start_stop
        self.end_stop = end_stop

    def __repr__(self):
        return f"Edge(line={self.line}, departure_time={self.departure_time}, arrival_time={self.arrival_time}, start_stop={self.start_stop}, end_stop={self.end_stop})"


class Node:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon


    def __repr__(self):
        return f"{self.name}, {self.lat}, {self.lon}"

    def __eq__(self, other):
        if other == None:
            return False
        return self.name == other.name

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __ne__(self, other):
        return True

    def __hash__(self):
        return hash((self.name, self.lat, self.lon))


edge_list = []
node_list = []
node_dict = {}

def get_graph():
    with open("connection_graph.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in rows[1:]:
            line = row[2]
            departure_time = time_after_midnight(validate_and_correct_time(row[3]))
            arrival_time = time_after_midnight(validate_and_correct_time(row[4]))
            start_stop = row[5]
            end_stop = row[6]
            start_stop_lat = row[7]
            start_stop_lon = row[8]
            end_stop_lat = row[9]
            end_stop_lon = row[10]
            if end_stop!= "Żórawina - Niepodległości (Mostek)":
                edge = Edge(line, departure_time, arrival_time, start_stop, end_stop)
                edge_list.append(edge)

                node = get_node_with_name(edge.start_stop)

                if(node == None):
                    node = Node(start_stop, start_stop_lon, start_stop_lat)
                    node_list.append(node)
                    node_dict[node] = []
                node_dict[node].append((edge, diff_between_hours(edge.arrival_time, edge.departure_time)))
    return node_dict


def get_node_with_name(name):
    for node in node_list:
        if(node.name) == name:
            return node

def time_after_midnight(time):
    godzina, minuta, _  = map(int, time.split(':'))
    return godzina*60+minuta

def validate_and_correct_time(time_str):
    try:
        time_obj = datetime.strptime(time_str, hour_format)
        return time_str
    except ValueError:
        godzina, minuta, sekunda = map(int, time_str.split(':'))
        calkowita_sekunda = godzina * 3600 + minuta * 60 + sekunda
        calkowita_sekunda -= 24 * 3600
        godzina = calkowita_sekunda // 3600
        minuta = (calkowita_sekunda % 3600) // 60
        sekunda = calkowita_sekunda % 60
        poprawiona_godzina = '{:02d}:{:02d}:{:02d}'.format(godzina, minuta, sekunda)

        return poprawiona_godzina

def save_node_dict(node_dict, filename):
    with open(filename, 'wb') as file:
        pickle.dump(node_dict, file)
    print(f"Node dictionary saved to {filename}")

def diff_between_hours(hour2, hour1):
    result = hour2-hour1
    while result < 0:
        result += 1440
    return result

