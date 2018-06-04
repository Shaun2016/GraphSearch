from model.vertex import Vertex
import queue
__author__ = 'ZJM'
__time__ = '2018/5/24 15:51'


# 强连通分量
class StrongConnectedComponent(Vertex):
    def __init__(self, scc_id, vertex_ids=set()):
        super(StrongConnectedComponent, self).__init__(scc_id)
        self.vertex_ids = vertex_ids  # 含有的结点 id
        self.access_out_points = set()     # 接入点或接出点 id
        self.scc_id = self.vid




