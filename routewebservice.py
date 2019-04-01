from __future__ import print_function

from flask import Response
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def create_data_model(getDistancesData, getDemandsData):
    data = {}
    _distances = eval(getDistancesData)

    demands = eval(getDemandsData)
    capacities = [5000, 5000, 5000]
    data["distances"] = _distances
    data["num_locations"] = len(_distances)
    data["num_vehicles"] = 3
    data["depot"] = 0
    data["demands"] = demands
    data["vehicle_capacities"] = capacities
    return data


def create_distance_callback(data):
    distances = data["distances"]
    def distance_callback(from_node, to_node):
        return distances[from_node][to_node]
    return distance_callback


def create_demand_callback(data):
    def demand_callback(from_node, to_node):
        return data["demands"][from_node]
    return demand_callback


def add_capacity_constraints(routing, data, demand_callback):
    capacity = "Capacity"
    routing.AddDimensionWithVehicleCapacity(
        demand_callback,
        0,
        data["vehicle_capacities"],
        True,
        capacity)


def print_solution(data, routing, assignment, rotalariyaz):
    total_dist = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = '{'
        plan_output += '"rota":"'
        route_dist = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = routing.IndexToNode(index)
            next_node_index = routing.IndexToNode(assignment.Value(routing.NextVar(index)))
            route_dist += routing.GetArcCostForVehicle(node_index, next_node_index, vehicle_id)
            route_load += data["demands"][node_index]
            plan_output += '{0},'.format(node_index)
            index = assignment.Value(routing.NextVar(index))
        node_index = routing.IndexToNode(index)
        total_dist += route_dist
        plan_output += '{0}'.format(node_index)
        plan_output += '"'
        # plan_output += 'Distance of the route: {0}m<br/>'.format(route_dist)
        # plan_output += 'Load of the route: {0}<br/>'.format(route_load)
        plan_output += '}'
        # print(plan_output)
        rotayikaydet(plan_output, rotalariyaz)
    # print('Total Distance of all routes: {0}m'.format(total_dist))


def rotayikaydet(plan_output2, rotalariyaz):
    rotalariyaz.append(plan_output2)
    rotalariyaz.append(',')



def main(getDistancesData, getDemandsData):
    rotalariyaz = []
    rotalariyaz.append('[')

    data = create_data_model(getDistancesData, getDemandsData)

    routing = pywrapcp.RoutingModel(
        data["num_locations"],
        data["num_vehicles"],
        data["depot"])

    distance_callback = create_distance_callback(data)
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)

    demand_callback = create_demand_callback(data)
    add_capacity_constraints(routing, data, demand_callback)

    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        print_solution(data, routing, assignment, rotalariyaz)
    rotalariyaz.pop();
    rotalariyaz.append(']')
    return Response(rotalariyaz)

if __name__ == '__main__':
    main()
