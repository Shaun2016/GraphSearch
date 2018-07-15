from model.Graph import Graph as G
import copy
import sys
sys.setrecursionlimit(1000000)
__author__ = 'ZJM'
__time__ = '2018/5/29 15:10'


if __name__ == '__main__':

    g = G('../data/Slashdot0811.txt', '	')
    g.get_scc_byKosaraju()
    condensationG = copy.deepcopy(g)
    condensationG.turn_to_condensation()
    condensationG.route_table(g)
    condensationG.show_route_table()
    condensationG.show_graph()
    g.show_graph()
    condensationG.topological_build_path()
    print(condensationG.topo_id_list)
    condensationG.travel(g)
    p = condensationG.get_shortest_path(g, 7, 11)
    print(p)

