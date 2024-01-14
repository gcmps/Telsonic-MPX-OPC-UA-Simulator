try:
    from opcua import ua, uamethod, Server
    from opcua.server.user_manager import UserManager
    from time import sleep
    import os
    from telsonic.results import Results
    import numpy as np
except ImportError as e:
    print(e)

with open('.env', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        os.environ[key] = value

users_db =  {
                os.getenv('USERNAME'): os.getenv('PASSWORD')
            }

connected_clients = {}

def user_manager(isession, username, password):
    isession.user = UserManager.User
    session_id = isession.session_id
    connected_clients[session_id] = username
    return username in users_db and password == users_db[username]

"""
OPC-UA-Server Setup
"""
server = Server()

endpoint = "opc.tcp://127.0.0.1:4840"
server.set_endpoint(endpoint)

servername = "Telsonic MPX"
server.set_server_name(servername)
address_space = server.register_namespace("http://opcfoundation.org/UA/DI/")

uri = "urn:opcua:python:server"
server.set_application_uri(uri)

server.user_manager.set_user_manager(user_manager)

cmd = ""

"""
OPC-UA-Modeling
"""
root_node = server.get_root_node()
object_node = server.get_objects_node()
server_node = server.get_server_node()

results_folder = object_node.add_folder(address_space, "Results")

result_folder = results_folder.add_folder(address_space, "Result")

max_power = result_folder.add_variable(address_space, "MaxPower", 0, varianttype=ua.VariantType.Int32)
max_power.set_writable()

max_force = result_folder.add_variable(address_space, "MaxForce", 0, varianttype=ua.VariantType.Int32)
max_force.set_writable()

distance_diff = result_folder.add_variable(address_space, "DistanceDiff", float(0), varianttype=ua.VariantType.Float)
distance_diff.set_writable()

weld_ok = result_folder.add_variable(address_space, "WeldOk", 0, varianttype=ua.VariantType.Int32)
weld_ok.set_writable()

weld_bad = result_folder.add_variable(address_space, "WeldBad", 0, varianttype=ua.VariantType.Int32)
weld_bad.set_writable()

recipe_name_from_result = result_folder.add_variable(address_space, "RecipeNameFromResult", "")
recipe_name_from_result.set_writable()

counter_total = result_folder.add_variable(address_space, "CounterTotal", 0, varianttype=ua.VariantType.Int32)
counter_total.set_writable()

def update_opcua_variables(results_instance):
    random_force, random_power, random_distance, ok, bad, random_recipe, count = results_instance.generate_random_results()

    power_value = ua.Variant(np.int32(random_power), ua.VariantType.Int32)
    force_value = ua.Variant(np.int32(random_force), ua.VariantType.Int32)
    distance_value = random_distance
    ok_value = ua.Variant(np.int32(ok), ua.VariantType.Int32)
    bad_value = ua.Variant(np.int32(bad), ua.VariantType.Int32)
    count_value = ua.Variant(np.int32(count), ua.VariantType.Int32)
    recipe_value = random_recipe

    max_power.set_value(power_value)
    max_force.set_value(force_value)
    distance_diff.set_value(distance_value)
    weld_ok.set_value(ok_value)
    weld_bad.set_value(bad_value)
    counter_total.set_value(count_value)
    recipe_name_from_result.set_value(recipe_value)

    return random_force, random_power, random_distance, ok, bad, random_recipe, count

"""
OPC-UA-Server Start
"""
server.start()

if __name__ == "__main__":
    try:
        results_instance = Results()
        while True:
            cmd = input("Command: ")
            if cmd == "run":
                power, force, distance, ok, bad, recipe, count = update_opcua_variables(results_instance)
                print(f"Max Power: {power}, Max Force: {force}, Distance Diff: {distance}, Ok: {ok}, Bad: {bad}, Recipe: {recipe}, Count: {count}")
            elif cmd == "exit":
                print("Closing connection...")
                server.stop()
                break
            else:
                print("Command not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
        server.stop()