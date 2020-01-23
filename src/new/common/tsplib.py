import os
from os.path import dirname as dn

from common.distances import City, distance_par_nom


def read_tsp_file(basename):
    if not basename.endswith(".tsp"):
        basename += ".tsp"
    tsp_path = os.path.join(dn(dn(__file__)), "tsplib", basename)
    return read_tsplib_path(tsp_path)

def read_tsplib_path(tsp_path):
    ignorer = {"COMMENT", "NODE_COORD_SECTION", "EOF", "NAME", "TYPE", "DIMENSION", "DISPLAY_DATA_TYPE"}
    nom_distance = "EUC_2D"
    with open(tsp_path, "r") as tspf:
        lines = tspf.readlines()


        g = []
        for l in lines:
            line = l.strip()
            if not line:
                continue
            elif any(line.startswith(k) for k in ignorer):
                continue
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                row = line.split(':')
                if len(row) >= 2:
                    nom_distance = row[1]
                continue
            else:
                row = line.split(' ')
                if row:
                    n = row[0]
                    x1 = float(row[1])
                    x2  = float(row[2])
                    g.append(City(x1, x2, n))
        return  g, distance_par_nom(nom_distance)

if __name__ == "__main__":
    # g136, _ = read_tsp_file("pr136")
    # assert len(g136) == 136
    g, _ = read_tsp_file("att48")