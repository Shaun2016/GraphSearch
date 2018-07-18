__author__ = 'ZJM'
__time__ = '2018/5/20 17:48'


class Vertex(object):
    def __init__(self, vid):
        self.vid = vid          # int: 结点id
        self.neighbors = set()      # set: 邻居结点
        self.pointed = set()       # set: 逆图中的邻居
        self.topological = 0        # int:拓扑值
        self.shortest_path = dict()       # dict<int vid, list[list]>: 到可达节点的路径
        self.shortest_path_len = dict()
        self.shortest_path_len[self.vid] = 0
        self.shortest_path_mid_point = dict()
        self.shortest_path_mid_point[self.vid] = self.vid
        self.reachable_Pri = set()  # set<Vertex>: 在私有网络中的可达集
        self.path_pri = dict()
        self.scc_id = None
        self.route_table = dict()  # 接入接出结点到SSC中其他结点的路由表
        self.in_connect = dict()
        self.out_connect = dict()
        # Tarjan 算法中的搜索次序和最先访问祖先的记号
        self.dfn = 0
        self.low = 0
        self.flag = 0   # 结点是否在栈中： 0 不在，1 在

    def __str__(self):
        id = 'vid: ' + str(self.vid)
        s = ', Pointed: {'
        for i in self.pointed:
            s += str(i) + ', '
        s += '}, Neighbors: {'
        for i in self.neighbors:
            s += str(i) + ', '
        s += '}'
        return id + s

    def print_route_table(self):
        res = ''
        for k, v in self.route_table.items():
            res += (str(k) + ': ' + str(v) + '; ')
        return res

    def get_path(self, obj_id):
        if obj_id in self.reachable:
            return self.shortest_path[obj_id]
        return False
