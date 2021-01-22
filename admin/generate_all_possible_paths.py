import math
import logging
from config import db_connector
from bson.objectid import ObjectId

logger = logging.getLogger('shortest_path')

appender = "--->"
global final_paths
final_paths = []


def get_distance(i, j, co_ordinats_dict):
    try:
        x = co_ordinats_dict[int(i)]["x"]
        y = co_ordinats_dict[int(i)]["y"]
        a = co_ordinats_dict[int(j)]["x"]
        b = co_ordinats_dict[int(j)]["y"]
        if x == a:
            return abs(y - b)
        elif y == b:
            return abs(x - a)
        else:
            dist = math.sqrt(math.pow((x - a), 2) + math.pow((y - b), 2))
            return dist
    except Exception as e:
        print(e)


def get_shortest_path(final_paths, positions_coordinats_dict):
    index = 0
    path_dist = {}
    for path in final_paths:
        pos_ids = path.split(appender)
        dist = int(0)
        i = 0
        while i < (len(pos_ids) - 2):
            dist = dist + int(get_distance(pos_ids[i], pos_ids[i + 1], positions_coordinats_dict))
            i += 1
        path_dist[dist] = index
        index += 1

    shortest_distance = sorted(path_dist.keys())[0]
    index = path_dist[shortest_distance]
    return final_paths[index]


def get_longest_path(final_paths, positions_coordinats_dict):
    index = 0
    path_dist = {}
    for path in final_paths:
        pos_ids = path.split(appender)
        dist = int(0)
        i = 0
        while i < (len(pos_ids) - 2):
            dist = dist + int(get_distance(pos_ids[i], pos_ids[i + 1], positions_coordinats_dict))
            i += 1
        path_dist[dist] = index
        index += 1

    longest_distance = sorted(path_dist.keys())[1]
    index = path_dist[longest_distance]
    return final_paths[index]


def shortest_path_coordinates(shortest_path, positions_coordinats_dict):
    shortest_path_co_ordinates_array =[]
    pos_ids = shortest_path.split(appender)
    for i in range(0, len(pos_ids)):
        shortest_path_co_ordinates_array.append(positions_coordinats_dict[int(pos_ids[i])])
    return shortest_path_co_ordinates_array


def get_path(loc_id, source_pid, destination_pid):
    final_paths.clear()
    database_name = "gmp_db"
    collection_gmp = "gmp_locations"
    try:
        conn = db_connector.Connection()
        client = conn.getConnection()
        db = client[database_name]
        collection_locations = db[collection_gmp]
        cursor = collection_locations.find_one({"_id": ObjectId(loc_id)})
        locationObj = cursor["location"]

        global positions_rel_dict, positions_coordinats_dict, position_id_names_dict, final_path
        positions_rel_dict = {}
        positions_coordinats_dict = {}
        position_id_names_dict = {}
        final_path = str(None)
        for document in locationObj["positions"]:
            position_relations = document["position_relations"]
            relations_array = []
            for position_rel in position_relations:
                relations_array.append(position_rel["related_position_id"])
            positions_rel_dict[document["position_id"]] = relations_array
            position_id_names_dict[document["position_id"]] = document["position_name"]
            positions_coordinats_dict[document["position_id"]] = document["position_coordinates"]

        # final_path = position_id_names_dict[source_pid] + appender
        final_path = str(source_pid) + appender
        get_path_to_destination(source_pid, destination_pid, final_path, [source_pid])
        logger.info(final_paths)
        shortest_path = get_shortest_path(final_paths, positions_coordinats_dict)
        logger.info(shortest_path)
        shortest_path_with_coordinates = shortest_path_coordinates(shortest_path, positions_coordinats_dict)
        logger.info(shortest_path_with_coordinates)
        return shortest_path_with_coordinates
    except Exception as e:
        logger.error("Error while getting shortest path  with trace back :%s", e)
    finally:
        conn.closeConnection()


def get_preferred_path(loc_id, source_pid, destination_pid, path_type):
    final_paths.clear()
    database_name = "gmp_db"
    collection_gmp = "gmp_locations"
    try:
        conn = db_connector.Connection()
        client = conn.getConnection()
        db = client[database_name]
        collection_locations = db[collection_gmp]
        cursor = collection_locations.find_one({"_id": ObjectId(loc_id)})
        locationObj = cursor["location"]

        global positions_rel_dict, positions_coordinats_dict, position_id_names_dict, final_path
        positions_rel_dict = {}
        positions_coordinats_dict = {}
        position_id_names_dict = {}
        final_path = str(None)
        
        for document in locationObj["positions"]:
            position_relations = document["position_relations"]
            relations_array = []
            for position_rel in position_relations:
                relations_array.append(position_rel["related_position_id"])
            positions_rel_dict[document["position_id"]] = relations_array
            position_id_names_dict[document["position_id"]] = document["position_name"]
            positions_coordinats_dict[document["position_id"]] = document["position_coordinates"]

        final_path = str(source_pid) + appender
        get_path_to_destination(source_pid, destination_pid, final_path, [source_pid])

        if path_type == 'L':
            path = get_longest_path(final_paths, positions_coordinats_dict)
        else:
            path = get_shortest_path(final_paths, positions_coordinats_dict)
        
        path_with_coordinates = shortest_path_coordinates(path, positions_coordinats_dict)
        
        return path_with_coordinates

    except Exception as e:
        logger.error("Error while getting shortest path  with trace back :%s", e)
    finally:
        conn.closeConnection()


def get_path_to_destination(source_pid, destination_pid, path, visited_positions):
    destinations = positions_rel_dict[source_pid]
    for destination in destinations:
        if destination not in visited_positions:
            temp_visited_positions = visited_positions[:]
            if destination is destination_pid:
                temp_visited_positions.append(destination_pid)
                final_paths.append(path + str(destination_pid))
                return
            temp_visited_positions.append(destination)
            temp_path = path + str(destination) + appender
            get_path_to_destination(destination, destination_pid, temp_path, temp_visited_positions)

