# ==========================================
# TREE DSA

class RouteNode:

    def __init__(self, location):
        self.location = location
        self.children = []

        # Every ride whose route passes through this exact
        # node (i.e. reaches this location by this exact path)
        self.ride_ids = set()

    # Find an existing child for this location, if any
    def find_child(self, location):

        for child in self.children:

            if child.location.lower() == location.lower():
                return child

        return None


class RouteTree:

    def __init__(self):

        self.root = RouteNode("ROOT")

    # ==========================================
    # INSERT A RIDE'S ROUTE INTO THE TREE
    # ==========================================

    def insert_route(self, locations, ride_id):

        current = self.root

        for location in locations:

            location = location.strip()

            if not location:
                continue

            existing_child = current.find_child(location)

            if existing_child is not None:
                # Shared prefix with an earlier route - reuse the node
                current = existing_child

            else:
                # Routes diverge here - create a new branch
                new_node = RouteNode(location)
                current.children.append(new_node)
                current = new_node

            current.ride_ids.add(ride_id)

    # ==========================================
    # FIND EVERY RIDE THAT GOES source -> destination
    # (source must appear before destination on the SAME branch)
    # ==========================================

    def find_matching_rides(self, source, destination):

        matched_ride_ids = set()

        # DFS below a "source" node, looking for a
        # "destination" node further down the same branch
        def collect_destinations(node):

            for child in node.children:

                if child.location.lower() == destination.lower():
                    matched_ride_ids.update(child.ride_ids)

                # Keep going in case destination also appears
                # further down another branch
                collect_destinations(child)

        # DFS over the whole tree, looking for every node
        # that matches "source"
        def find_source_nodes(node):

            if node.location.lower() == source.lower():
                collect_destinations(node)

            for child in node.children:
                find_source_nodes(child)

        find_source_nodes(self.root)

        return matched_ride_ids

    # ==========================================
    # CHECK IF A LOCATION EXISTS ANYWHERE IN THE TREE
    # ==========================================

    def find_location(self, location):

        def search(node):

            if node.location.lower() == location.lower():
                return True

            for child in node.children:

                if search(child):
                    return True

            return False

        return search(self.root)