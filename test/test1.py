from model.Graph import Graph as G
import copy
import sys
import threading
sys.setrecursionlimit(100000)
__author__ = 'ZJM'
__time__ = '2018/5/29 15:10'


if __name__ == '__main__':
    def shortestPath():
        g = G('../data/0811.txt')
        g.get_scc_byKosaraju()
        print(len(g.scc_dict))
        condensationG = copy.deepcopy(g)
        condensationG.turn_to_condensation()
        condensationG.route_table(g)
        condensationG.show_route_table()
        condensationG.topological_build_path()
        condensationG.show_graph()
        print(condensationG.topo_id_list)
        condensationG.travel(g)
        p = condensationG.get_shortest_path(g, 7, 11)
        print(p)
        pass

    # g.get_scc_by_tarjan()
    # print('---------------------------')
    # for k, v in g.scc_dict.items():
    #     print(k, ': ', v)
    threading.stack_size(200000000)
    thread = threading.Thread(target=shortestPath)  # your_code是函数
    thread.start()
    # print(".............len of scc_dict: ", len(g.scc_dict))
    # for k, v in g.scc_dict.items():
    #    print(k, v.vertex_ids)
