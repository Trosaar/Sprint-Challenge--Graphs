from room import Room
from player import Player
from world import World
from stack import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}

def update_visited(direction = None, last_room_id = None):
    if player.current_room.id not in visited:
        visited[player.current_room.id] = {
            'visit_count': 0,
            'exits': {}
        }

    for exit in player.current_room.get_exits():
        if exit not in visited[player.current_room.id]['exits']:
            visited[player.current_room.id]['exits'][exit] = '?'

    if direction == 'n':
        if last_room_id is not None:
            visited[player.current_room.id]['exits']['s'] = last_room_id
            visited[last_room_id]['exits']['n'] = player.current_room.id

    elif direction == 'e':
        if last_room_id is not None:
            visited[player.current_room.id]['exits']['w'] = last_room_id
            visited[last_room_id]['exits']['e'] = player.current_room.id

    elif direction == 'w':
        if last_room_id is not None:
            visited[player.current_room.id]['exits']['e'] = last_room_id
            visited[last_room_id]['exits']['w'] = player.current_room.id

    elif direction == 's':
        if last_room_id is not None:
            visited[player.current_room.id]['exits']['n'] = last_room_id
            visited[last_room_id]['exits']['s'] = player.current_room.id

    visited[player.current_room.id]['visit_count'] += 1


    print(f'{len(visited)} / {len(room_graph)}')

def BFS_destination_check(vertrex):
    if '?' in visited[vertrex]['exits'].values():
        return True
    else:
        return False

def add_traversal_to_path(direction, path):
    updated_path = list(path)
    updated_path = updated_path + [direction]    
    traversal_path = updated_path
    return traversal_path
    

update_visited()

while len(visited) < len(room_graph):
    options = [exit for exit in visited[player.current_room.id]['exits']]

    for option in options:
        if visited[player.current_room.id]['exits'][option] == '?':
            remember_last_room = player.current_room.id
            player.travel(option)
            traversal_path = add_traversal_to_path(option, traversal_path)
            update_visited(option, remember_last_room)
            break

    if BFS_destination_check(player.current_room.id) is False:
        plan_to_visit = Queue()
        plan_to_visit.enqueue( (player.current_room.id, []))
        checked_vertex = set()
        # while the plan_to_visit queue is not Empty:
        while plan_to_visit.size > 0:
            current_tuple = plan_to_visit.dequeue()
            current_path = current_tuple[1]
            current_vertex = current_tuple[0]

            # if we find a '?'
            if BFS_destination_check(current_vertex):
                # travel to '?'
                for direction in current_path:
                    player.travel(direction)
                    traversal_path = add_traversal_to_path(direction, traversal_path)
                plan_to_visit = Queue()

            if BFS_destination_check(current_vertex) == False:
                # print(player.current_room.id)
                # add all neighbors to the queue
                for neighbor in visited[current_vertex]['exits']:
                    # if neighbor room number not already checked
                    if visited[current_vertex]['exits'][neighbor] not in checked_vertex:
                        # get neight room number
                        neighbor_room_id = visited[current_vertex]['exits'][neighbor]
                        # identify max visits allowed for optimization
                        visit_max = len(visited[neighbor_room_id]['exits'])
                        
                        # if we've not hit max visits
                        if visited[neighbor_room_id]['visit_count'] < visit_max:
                            # create new array for path
                            next_path = list(current_path)
                            # concat arrays to add neighbor
                            next_path = next_path + [neighbor]
                            # add desired room to check and path to room to Queue
                            plan_to_visit.enqueue( ( visited[current_vertex]['exits'][neighbor], next_path))
                            # add current vertex to set
                            checked_vertex.add(current_vertex)
                            # print("Checked vert", checked_vertex)

# print(len(traversal_path), traversal_path)
# print("current room", player.current_room.id)
# print(player.current_room.get_exits())
# print(player.travel('n'))
# print(player.current_room.id)
# print(traversal_path)
# print("visited", visited)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
'''
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''