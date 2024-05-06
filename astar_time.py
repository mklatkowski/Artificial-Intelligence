import heapq
from convert_file import Node, Edge
from datetime import datetime
import pickle
import math
import time
from map_service import show_track

hour_format = "%H:%M:%S"
AVERAGE_VELIOCITY = 18 #km/h


def astar_time(graph_dict, start, end, time):


    distances = {node: float('inf') for node in graph_dict}
    start = get_node_with_name(start)
    end = get_node_with_name(end)
    distances[start] = 0
    pq = [(0, (0, start))]
    prev_edges = {node: None for node in graph_dict}
    prev_edges[start] = Edge(None, None, time, None, None)

    while pq:
        (curr_h,(curr_dist, curr_node)) = heapq.heappop(pq)
        for neighbor_edge, weight in graph_dict[curr_node]:
            if weight < 0:
                weight += 1440
            new_dist = curr_dist + weight + diff_between_hours(neighbor_edge.departure_time, prev_edges[curr_node].arrival_time)
            neighbor = get_node_with_name(neighbor_edge.end_stop)

            value_with_heuristic = new_dist + h(neighbor, end)

            try:
                if new_dist < distances[neighbor]: #for old and new heuristic its comparation between new_dist + h and distances[neighbor] + h
                    distances[neighbor] = new_dist
                    prev_edges[neighbor] = neighbor_edge
                    heapq.heappush(pq, (value_with_heuristic, (new_dist,neighbor)))
            except KeyError:
                pass
        if curr_node == end:
            break

    return distances, prev_edges


def h(start, stop):
    earth_radius = 6371.0

    try:
        lat1 = float(start.lat)
        lon1 = float(start.lon)

        lat2 = float(stop.lat)
        lon2 = float(stop.lon)
    except AttributeError:
        return 1000000

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    time = (distance/AVERAGE_VELIOCITY)
    return time


def shortest_path(graph_dict, start, goal, time):
    distances, prev_edges = astar_time(graph_dict, start, goal, time)
    path = []
    curr_node = get_node_with_name(goal)
    while prev_edges[curr_node].start_stop is not None:
        path.append(prev_edges[curr_node])
        curr_node = get_node_with_name(prev_edges[curr_node].start_stop)
    path.reverse()
    return distances[get_node_with_name(goal)], path


def dist(graph_dict, node, goal, time):
    distance, path = shortest_path(graph_dict, node, goal, convert_hour_to_min(time))
    return distance, path


def diff_between_hours(hour2, hour1):
    result = int(hour2) - int(hour1)
    if result < 0:
        result += 1440
    return result

def convert_hour_to_min(time):
    godzina, minuta, _ = map(int, time.split(':'))
    value = godzina*60+minuta
    if value > 1440:
        return value - 1440
    return value

def minutes_to_time_string(minutes):
    hours = minutes // 60
    minutes %= 60
    seconds = 0

    time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

    return time_string


def load_node_dict():
    with open("node_graph.pickle", 'rb') as file:
        node_dict = pickle.load(file)
    return node_dict


def get_node_with_name(name):
    for node in node_list:
        if node.name == name:
            return node

def get_coordinates(path):
    lats = []
    lons = []
    texts = []
    current_node = get_node_with_name(path[0].start_stop)
    lats.append(float(current_node.lat))
    lons.append(float(current_node.lon))
    texts.append(f'{current_node.name}: {minutes_to_time_string(path[0].arrival_time)}')
    for edge in path:
        current_node = get_node_with_name(edge.end_stop)
        lats.append(float(current_node.lat))
        lons.append(float(current_node.lon))
        texts.append(f'{current_node.name}: {minutes_to_time_string(edge.arrival_time)}')
    return lats, lons, texts


if __name__ == '__main__':
    graph = load_node_dict()
    print("Graph loaded")
    node_list = list(graph.keys())

    time1 = time.time()

    # distance, path = dist(graph, 'Magellana', 'DWORZEC AUTOBUSOWY', "11:00:00")
    distance, path = dist(graph, 'Kwiska', 'PL. GRUNWALDZKI', "09:00:00")

    time2 = time.time()
    print("Shortest distance:", distance)
    print("Shortest path:")

    for edge in path:
        print(f'{edge.start_stop} -> {edge.end_stop}: {minutes_to_time_string(edge.departure_time)} - {minutes_to_time_string(edge.arrival_time)}, line: {edge.line}')

    print(f'Time: {round(time2-time1, 4)} seconds')

    show_track(get_coordinates(path))