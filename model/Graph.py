from vertex import Vertex
from SCC import StrongConnectedComponent as SCC
import queue
__author__ = 'ZJM'
__time__ = '2018/5/29 14:58'


class Graph(object):
    def __init__(self, file_path=''):
        self.vertex_ids = set()  # 图中结点 id 集
        self.vertices = dict()  # id-结点
        self.scc_dict = dict()  # SCC_id-SCC
        self.topo_id_list = list()  # 拓扑排序值
        self.condensation_graph = None  # 压缩图
        if not file_path:
            return
        split_by = ''
        with open(file_path) as file:
            i = 0
            for line in file:
                if line[0] is '#':
                    continue
                split_by = self.get_splite_char(file.readline())
                break
        with open(file_path) as file:
            print('...(' + split_by + ')...')
            for line in file:
                # 如果以 # 开头则跳过
                if line[0] is '#':
                    continue
                arr = line.split(split_by)
                from_id = int(arr[0])
                to_id = int(arr[1])
                if from_id == to_id:
                    continue
                # 向图中结点 id 的 set 中添加 id
                self.vertex_ids.add(from_id)
                self.vertex_ids.add(to_id)
                # 如果是第一次的结点创建并放进图的 vertices 中
                if not self.vertices.get(from_id):
                    self.vertices[from_id] = Vertex(from_id)
                if not self.vertices.get(to_id):
                    self.vertices[to_id] = Vertex(to_id)
                # 建立边（结点之间的关系）
                self.vertices.get(from_id).neighbors.add(to_id)
                self.vertices.get(to_id).pointed.add(from_id)
        print('The size of vertices in Origin Graph is: ' + str(len(self.vertex_ids)))

    # 找到每行数据的分隔符
    def get_splite_char(self, line):
        res = ''
        for i in range(len(line)):
            if '0' <= line[i] <= '9' or line[i] == '#':
                continue
            for j in range(i, len(line)):
                if '0' <= line[j] <= '9' or line[j] == '#':
                    break
                res += line[j]
            return res

    # 通过 kosaraju 算法求原图中所有强连通分量
    def get_scc_byKosaraju(self):
        visited = []
        stack = []

        # 逆后续遍历
        def reverse_post_order_tra(i):
            if i in visited:
                return
            visited.append(i)
            for j in self.vertices.get(i).pointed:
                reverse_post_order_tra(j)
            stack.append(i)     # 入栈
        index = 0
        try:
            for index in self.vertex_ids:
                print(index)
                reverse_post_order_tra(index)
        except RecursionError as e:
            print('stack: ', stack)
            print('visited', visited)
            print('now number: ', index)
        print('Reverse Post-Order', end=': ')
        print(stack)
        visited = set()

        def dfs(m, scc):
            if m in visited:
                return
            visited.add(m)
            for j in self.vertices.get(m).neighbors:
                dfs(j, scc)
            scc.append(m)
            return scc
        while stack:
            i = stack.pop()
            scc = dfs(i, [])
            if scc and len(scc) > 1:
                temp = SCC(scc[0], set(scc))
                self.scc_dict[scc[0]] = temp
                for v in scc:
                    self.vertices.get(v).scc_id = scc[0]
        print('Strong connected components:')
        for item in self.scc_dict.values():
            print(item.vertex_ids)
        print('The size of SCC in Condensation Graph is: ' + str(len(self.scc_dict)))

    # Tarjan 求原图的所有强连通分量
    def get_scc_by_tarjan(self):
        stack = []
        # 标记：访问次序
        num = 0
        # 返回的结果: a list of SCC
        res = []

        # u: 要遍历的结点 id
        def tarjan(u):
            nonlocal num
            vu = self.vertices.get(u)
            vu.dfn = vu.low = num
            num += 1
            vu.flag = 1
            stack.append(u)

            for index in vu.neighbors:
                vi = self.vertices.get(index)
                if not vi.dfn:
                    tarjan(index)
                    if vi.low < vu.low:
                        vu.low = vi.low
                    continue
                if vi.dfn < vu.low and vi.flag:
                    vu.low = vi.dfn
            # 回溯过程：如果发现 dfn == low 的结点，把该点之后的结点全部弹出，
            # 作为一个SCC
            scc = []
            if vu.dfn is vu.low:
                temp = stack.pop()
                self.vertices.get(temp).flag = 0
                while temp is not u:
                    scc.append(temp)
                    temp = stack.pop()
                    self.vertices.get(temp).flag = 0
                res.append(scc)
            pass
        tarjan(list(self.vertex_ids)[0])
        return res
        pass

    # 求压缩图
    def turn_to_condensation(self):
        # 修改压缩图中的SCC
        for scc in self.scc_dict.values():    # 遍历每个强连通分量，加入到图的结点中
            # 遍历SCC中的每一个结点
            for i in scc.vertex_ids:
                v_i = self.vertices.get(i)
                i_neighbors = v_i.neighbors - scc.vertex_ids
                i_pointed = v_i.pointed - scc.vertex_ids
                if i_neighbors:
                    scc.access_out_points.add(i)
                    for j in i_neighbors:
                        j_scc_id = self.vertices.get(j).scc_id
                        if j_scc_id:    # 邻居是一个SCC
                            scc.neighbors.add(j_scc_id)
                            # 两个SCC之间的连接路径
                            scc.out_connect[j_scc_id] = i
                            scc.out_connect[j] = i
                        else:   # 邻居是一个结点
                            scc.neighbors.add(j)
                            # 修改该结点的被指结点集
                            node = self.vertices.get(j)
                            node.pointed.remove(i)
                            node.pointed.add(scc.vid)
                            # SCC 到结点之间的连接路径
                            scc.out_connect[j] = i
                if i_pointed:
                    scc.access_out_points.add(i)
                    for j in i_pointed:
                        j_scc_id = self.vertices.get(j).scc_id
                        if j_scc_id:
                            scc.pointed.add(j_scc_id)
                            scc.in_connect[j_scc_id] = i
                            scc.in_connect[j] = i
                        else:
                            scc.pointed.add(j)
                            # 修改该结点的邻居集
                            node = self.vertices.get(j)
                            node.neighbors.remove(i)
                            node.neighbors.add(scc.vid)
                            scc.in_connect[j] = i
        for scc in self.scc_dict.values():
            self.vertices[scc.vid] = scc
            self.vertex_ids -= (scc.vertex_ids - {scc.vid})

    # 对每个强连通分量求接入接出点的路由表
    def route_table(self, origin_g):
        for k, v in self.scc_dict.items():
            for access_out_p_id in v.access_out_points:
                visited = set()
                q = queue.Queue()
                q.put(access_out_p_id)
                access_out_p = self.vertices.get(access_out_p_id)
                access_out_p.route_table[access_out_p_id] = [access_out_p_id]
                while not q.empty():
                    now = q.get()
                    if now in visited:
                        continue
                    visited.add(now)
                    for j in origin_g.vertices.get(now).neighbors:
                        if j in visited or j not in v.vertex_ids:
                            continue
                        q.put(j)
                        l = access_out_p.route_table[now][:]
                        l.append(j)
                        access_out_p.route_table[j] = l
                    pass
        pass

    # 展示路由表信息
    def show_route_table(self):
        print('Route Table for Strong Connected Component:')
        for k, i in self.scc_dict.items():
            print(k, ':')
            for j in i.access_out_points:
                print('access_out_point_id', j, ':', self.vertices.get(j).print_route_table())

    # 求压缩图中没有入度的点
    def find_zero_in_degree(self):
        start = list([])
        for vid in self.vertex_ids:
            if not len(self.vertices.get(vid).pointed):
                start.append(vid)
        return start

    # 拓扑排序
    def topological_build_path(self):
        start = self.find_zero_in_degree()
        print('start vertices for topological sort', end=': ')
        print(start)
        q = queue.Queue()
        # 为初始结点赋拓扑值
        for i in start:
            q.put(i)
        # 广度搜索为其他结点赋拓扑值
        topo_num = 1
        topo_id_list = [0]
        while not q.empty():
            now = q.get()
            node = self.vertices.get(now)
            if node.topological:
                continue
            node.topological = topo_num
            topo_id_list.append(node.vid)
            for i in node.neighbors:
                q.put(i)
            topo_num += 1
            self.topo_id_list = topo_id_list
        return topo_id_list

    # 按拓扑排序的逆序计算每个结点的属性
    def travel(self, origin_graph):
        for i in range(len(self.vertex_ids), 0, -1):
            node = self.vertices.get(self.topo_id_list[i])  # 当前遍历的结点
            for next_id in node.neighbors:
                next_node = self.vertices.get(next_id)
                node.shortest_path[next_id] = [next_id]
                for vid, shortest_path in next_node.shortest_path.items():
                    path = self.combine_path(node, next_node, shortest_path, origin_graph)
                    if vid not in node.shortest_path or len(path) < len(node.shortest_path[vid]):
                        node.shortest_path[vid] = path

    # 儿子结点的属性放到父亲结点里
    def combine_path(self, node, child, path, origin_graph):
        l = path[:]
        if not child.scc_id:
            l.insert(0, child.vid)
            return l
        first_node = path[0]
        out_point = child.out_connect.get(first_node)
        in_point = child.in_connect.get(node.vid)
        l = self.vertices.get(in_point).route_table.get(out_point) + l
        return l

    # 显示图的点
    def show_graph(self):
        print('--------The vertices in graph:---------')
        for vid, v in self.vertices.items():
            print(vid, v.pointed, v.neighbors)

    # 求两点的最短路径
    def get_shortest_path(self, origin_g, u, v):
        if u not in origin_g.vertex_ids or v not in origin_g.vertex_ids:
            print('u or v not in graph')
            return False
        u = self.vertices[u]
        v = self.vertices[v]
        if not u.scc_id and not v.scc_id:
            return u.shortest_path.get(v.vid, False)
        if not u.scc_id and v.scc_id:
            path1 = u.shortest_path.get(v.scc_id)
            if not path1:
                return False
            if len(path1) == 1:
                second_last_point = u.vid
            else:
                second_last_point = path1[-2]
            scc = self.scc_dict[v.scc_id]
            in_point = scc.in_connect[second_last_point]
            path_in_scc = self.vertices.get(in_point).route_table[v.vid]
            return [u.vid] + path1[:-1] + path_in_scc
        if u.scc_id and not v.scc_id:
            path1 = self.scc_dict[u.scc_id].shortest_path.get(v.vid)
            if not path1:
                return False
            if len(path1) == 1:
                second_point = v.vid
            else:
                second_point = path1[0]
            scc = self.scc_dict[u.scc_id]
            out_point = scc.out_connect[second_point]
            path_in_scc = self.vertices.get(u.vid).route_table[out_point]
            return [u.vid] + path_in_scc + path1
        if u.scc_id and v.scc_id:
            path1 = self.scc_dict[u.scc_id].shortest_path[v.scc_id]
            if not path1:
                return False
            if len(path1) == 1:
                second_point = v.scc_id
                second_last_point = u.scc_id
            elif len(path1) == 2:
                second_point = path1[0]
                second_last_point = path1[0]
            else:
                second_point = path1[0]
                second_last_point = path1[-2]
            scc1 = self.scc_dict[u.scc_id]
            out_point = scc1.out_connect[second_point]
            scc2 = self.scc_dict[v.scc_id]
            in_point = scc2.in_connect[second_last_point]
            path_in_scc1 = self.vertices.get(out_point).route_table[u.vid][::-1]
            path_in_scc2 = self.vertices.get(in_point).route_table[v.vid]
            return path_in_scc1 + path1[:-1] + path_in_scc2


