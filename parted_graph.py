import math
import random
import pandas as pd


class PartedGraph:
    def __init__(self, vertices, edges: list, percent=2/3):
        self.node_weights_lin = {}
        self.node_weights_exp = {}
        self.node_weights_sq = {}
        self.t_max = 0
        self.static_features = {'CN_true': [],
                                'CN_false': [],
                                'AA_true': [],
                                'AA_false': [],
                                'JC_true': [],
                                'JC_false': [],
                                'PA_true': [],
                                'PA_false': []}
        self.node_activity_features = {
            'lin_0_sum': [],
            'lin_1_sum': [],
            'lin_2_sum': [],
            'lin_3_sum': [],
            'lin_4_sum': [],
            'lin_5_sum': [],
            'lin_6_sum': [],

            'lin_0_dif': [],
            'lin_1_dif': [],
            'lin_2_dif': [],
            'lin_3_dif': [],
            'lin_4_dif': [],
            'lin_5_dif': [],
            'lin_6_dif': [],

            'lin_0_min': [],
            'lin_1_min': [],
            'lin_2_min': [],
            'lin_3_min': [],
            'lin_4_min': [],
            'lin_5_min': [],
            'lin_6_min': [],

            'lin_0_max': [],
            'lin_1_max': [],
            'lin_2_max': [],
            'lin_3_max': [],
            'lin_4_max': [],
            'lin_5_max': [],
            'lin_6_max': [],

            # ---------------------------------------

            'exp_0_sum': [],
            'exp_1_sum': [],
            'exp_2_sum': [],
            'exp_3_sum': [],
            'exp_4_sum': [],
            'exp_5_sum': [],
            'exp_6_sum': [],

            'exp_0_dif': [],
            'exp_1_dif': [],
            'exp_2_dif': [],
            'exp_3_dif': [],
            'exp_4_dif': [],
            'exp_5_dif': [],
            'exp_6_dif': [],

            'exp_0_min': [],
            'exp_1_min': [],
            'exp_2_min': [],
            'exp_3_min': [],
            'exp_4_min': [],
            'exp_5_min': [],
            'exp_6_min': [],

            'exp_0_max': [],
            'exp_1_max': [],
            'exp_2_max': [],
            'exp_3_max': [],
            'exp_4_max': [],
            'exp_5_max': [],
            'exp_6_max': [],

            # ---------------------------------------

            'sq_0_sum': [],
            'sq_1_sum': [],
            'sq_2_sum': [],
            'sq_3_sum': [],
            'sq_4_sum': [],
            'sq_5_sum': [],
            'sq_6_sum': [],

            'sq_0_dif': [],
            'sq_1_dif': [],
            'sq_2_dif': [],
            'sq_3_dif': [],
            'sq_4_dif': [],
            'sq_5_dif': [],
            'sq_6_dif': [],

            'sq_0_min': [],
            'sq_1_min': [],
            'sq_2_min': [],
            'sq_3_min': [],
            'sq_4_min': [],
            'sq_5_min': [],
            'sq_6_min': [],

            'sq_0_max': [],
            'sq_1_max': [],
            'sq_2_max': [],
            'sq_3_max': [],
            'sq_4_max': [],
            'sq_5_max': [],
            'sq_6_max': [],

        }
        self.educ_pairs_false = None
        self.educ_pairs_true = None
        edges.sort(key=lambda x: x[3])
        t1 = edges[0][3]
        t2 = edges[-1][3] - t1
        edges = list(map(lambda x: (x[0], x[1], x[2], (x[3] - t1) / t2), edges))
        self.edges = {}
        self.adj_list = {}
        self.remaining_adj_list = {}
        self.remaining_edges = {}
        self.temporal_weighted_edges = {}
        for i in vertices:
            self.adj_list[i] = set()
            self.remaining_adj_list[i] = set()
        for edge in edges:
            if edge[3] <= percent:
                self.adj_list[edge[0]].add(edge[1])
                self.adj_list[edge[1]].add(edge[0])
                self.edges[(min(edge[0], edge[1]), max(edge[0], edge[1]))] = edge[3]
                if edge[3] > self.t_max:
                    self.t_max = edge[3]
            else:
                self.remaining_adj_list[edge[0]].add(edge[1])
                self.remaining_adj_list[edge[1]].add(edge[0])
                self.remaining_edges[(min(edge[0], edge[1]), max(edge[0], edge[1]))] = edge[3]

    def set_pairs(self):
        if self.educ_pairs_true is not None and self.educ_pairs_false is not None:
            return
        self.educ_pairs_true = []
        self.educ_pairs_false = []
        for pair in self.remaining_edges.keys():
            if len(self.educ_pairs_true) > 10000:
                break
            if len(self.adj_list[pair[0]].intersection(self.adj_list[pair[1]])) > 0 and len(
                    self.educ_pairs_true) < 10000:
                self.educ_pairs_true.append(pair)
        while len(self.educ_pairs_false) < len(self.educ_pairs_true):
            rand_v = random.randint(1, len(self.adj_list))
            second_neighbours = set()
            for i in self.adj_list[rand_v]:
                second_neighbours = second_neighbours.union(self.adj_list[i])
            second_neighbours = second_neighbours.difference(self.adj_list[rand_v])
            if len(second_neighbours) <= 1:
                continue
            rand_u = list(second_neighbours)[random.randint(1, len(second_neighbours) - 1)]
            pair = (min(rand_v, rand_u), max(rand_v, rand_u))
            if pair not in self.remaining_edges and pair not in self.edges and rand_v != rand_u:
                self.educ_pairs_false.append(pair)
                print("Suitable pair found, ", len(self.educ_pairs_false), " of ", len(self.educ_pairs_true))
        for i in range(len(self.educ_pairs_false) - len(self.educ_pairs_true)):
            self.educ_pairs_false.pop()

    def set_common_neighbours(self):
        for pair in self.educ_pairs_true:
            self.static_features['CN_true'].append(len(self.adj_list[pair[0]].intersection(self.adj_list[pair[1]])))
        for pair in self.educ_pairs_false:
            self.static_features['CN_false'].append(len(self.adj_list[pair[0]].intersection(self.adj_list[pair[1]])))
        M = max(max(self.static_features['CN_true']), max(self.static_features['CN_false']))
        m = min(min(self.static_features['CN_true']), min(self.static_features['CN_false']))
        M -= m
        for i in range(len(self.static_features['CN_true'])):
            self.static_features['CN_true'][i] -= m
            self.static_features['CN_false'][i] -= m
            self.static_features['CN_true'][i] /= M
            self.static_features['CN_false'][i] /= M

    def set_adamic_adar(self):
        for pair in self.educ_pairs_true:
            neighbours = self.adj_list[pair[0]].intersection(self.adj_list[pair[1]])
            sum = 0
            for n in neighbours:
                sum += 1 / math.log2(len(self.adj_list[n]))
            self.static_features['AA_true'].append(sum)
        for pair in self.educ_pairs_false:
            neighbours = self.adj_list[pair[0]].intersection(self.adj_list[pair[1]])
            sum = 0
            for n in neighbours:
                sum += 1 / math.log2(len(self.adj_list[n]))
            self.static_features['AA_false'].append(sum)
        M = max(max(self.static_features['AA_true']), max(self.static_features['AA_false']))
        m = min(min(self.static_features['AA_true']), min(self.static_features['AA_false']))
        M -= m
        for i in range(len(self.static_features['AA_true'])):
            self.static_features['AA_true'][i] -= m
            self.static_features['AA_false'][i] -= m
            self.static_features['AA_true'][i] /= M
            self.static_features['AA_false'][i] /= M

    def set_jaccard_coefficient(self):
        for pair in self.educ_pairs_true:
            neighbours_inter = len(self.adj_list[pair[0]].intersection(self.adj_list[pair[1]]))
            neighbours_union = len(self.adj_list[pair[0]].union(self.adj_list[pair[1]]))
            self.static_features['JC_true'].append(neighbours_inter / neighbours_union)
        for pair in self.educ_pairs_false:
            neighbours_inter = len(self.adj_list[pair[0]].intersection(self.adj_list[pair[1]]))
            neighbours_union = len(self.adj_list[pair[0]].union(self.adj_list[pair[1]]))
            self.static_features['JC_false'].append(neighbours_inter / neighbours_union)
        M = max(max(self.static_features['JC_true']), max(self.static_features['JC_false']))
        m = min(min(self.static_features['JC_true']), min(self.static_features['JC_false']))
        M -= m
        for i in range(len(self.static_features['JC_true'])):
            self.static_features['JC_true'][i] -= m
            self.static_features['JC_false'][i] -= m
            self.static_features['JC_true'][i] /= M
            self.static_features['JC_false'][i] /= M

    def set_preferential_attachment(self):
        for pair in self.educ_pairs_true:
            self.static_features['PA_true'].append(len(self.adj_list[pair[0]]) * len(self.adj_list[pair[1]]))
        for pair in self.educ_pairs_false:
            self.static_features['PA_false'].append(len(self.adj_list[pair[0]]) * len(self.adj_list[pair[1]]))
        M = max(max(self.static_features['PA_true']), max(self.static_features['PA_false']))
        m = min(min(self.static_features['PA_true']), min(self.static_features['PA_false']))
        M -= m
        for i in range(len(self.static_features['PA_true'])):
            self.static_features['PA_true'][i] -= m
            self.static_features['PA_false'][i] -= m
            self.static_features['PA_true'][i] /= M
            self.static_features['PA_false'][i] /= M

    def set_static_features(self):
        self.set_pairs()
        self.set_common_neighbours()
        self.set_adamic_adar()
        self.set_jaccard_coefficient()
        self.set_preferential_attachment()

    def print_static_features(self):
        for i in range(len(self.educ_pairs_true)):
            print(self.static_features['CN_true'][i],
                  self.static_features['AA_true'][i],
                  self.static_features['JC_true'][i],
                  self.static_features['PA_true'][i])
            print(self.static_features['CN_false'][i],
                  self.static_features['AA_false'][i],
                  self.static_features['JC_false'][i],
                  self.static_features['PA_false'][i])

    def get_static_features_dataframe(self) -> pd.DataFrame:
        features = {
            'CN': [],
            'AA': [],
            'JC': [],
            'PA': [],
            'flag': []
        }
        for i in range(len(self.static_features['CN_true'])):
            features['CN'].append(self.static_features['CN_true'][i])
            features['CN'].append(self.static_features['CN_false'][i])

            features['AA'].append(self.static_features['AA_true'][i])
            features['AA'].append(self.static_features['AA_false'][i])

            features['JC'].append(self.static_features['JC_true'][i])
            features['JC'].append(self.static_features['JC_false'][i])

            features['PA'].append(self.static_features['PA_true'][i])
            features['PA'].append(self.static_features['PA_false'][i])

            features['flag'].append(True)
            features['flag'].append(False)

        df = pd.DataFrame(features)
        return df

    def set_temporal_weighting(self, lower_bound=0.2):
        for edge in self.edges:
            tmp = self.edges[edge] / self.t_max
            w_lin = lower_bound + (1 - lower_bound) * tmp
            w_exp = lower_bound + (1 - lower_bound) * (math.exp(3 * tmp) - 1) / (math.exp(3) - 1)
            w_sq = lower_bound + (1 - lower_bound) * math.sqrt(tmp)
            self.temporal_weighted_edges[edge] = (w_lin, w_exp, w_sq)

    def set_node_activity(self):
        def calc_features(incident_weights: list) -> tuple:
            n = len(incident_weights)
            if n < 1:
                return 0, 0, 0, 0, 0, 0, 0
            incident_weights.sort()
            a = incident_weights[0]
            b = incident_weights[:n // 4][-1] if n // 4 > 0 else incident_weights[0]
            c = incident_weights[:n // 2][-1] if n // 2 > 0 else incident_weights[-1]
            d = incident_weights[:n * 3 // 4][-1] if n * 3 // 4 > 0 else incident_weights[-1]
            e = incident_weights[-1]
            f = sum(incident_weights)
            g = f / n
            return a, b, c, d, e, f, g

        for v in self.adj_list:
            w_lin_neighbours = []
            w_exp_neighbours = []
            w_sq_neighbours = []
            for u in self.adj_list[v]:
                w_lin_neighbours.append(self.temporal_weighted_edges[(min(v, u), max(v, u))][0])
                w_exp_neighbours.append(self.temporal_weighted_edges[(min(v, u), max(v, u))][1])
                w_sq_neighbours.append(self.temporal_weighted_edges[(min(v, u), max(v, u))][2])
            self.node_weights_lin[v] = calc_features(w_lin_neighbours)
            self.node_weights_exp[v] = calc_features(w_exp_neighbours)
            self.node_weights_sq[v] = calc_features(w_sq_neighbours)

    def combine_node_activity(self):
        for i in range(len(self.educ_pairs_true)):
            def summ(x, y): return x + y
            t = self.educ_pairs_true[i]
            f = self.educ_pairs_false[i]
            self.node_activity_features['lin_0_sum'].append(summ(self.node_weights_lin[t[0]][0], self.node_weights_lin[t[1]][0]))
            self.node_activity_features['lin_0_sum'].append(summ(self.node_weights_lin[f[0]][0], self.node_weights_lin[f[1]][0]))
            self.node_activity_features['exp_0_sum'].append(summ(self.node_weights_exp[t[0]][0], self.node_weights_exp[t[1]][0]))
            self.node_activity_features['exp_0_sum'].append(summ(self.node_weights_exp[f[0]][0], self.node_weights_exp[f[1]][0]))
            self.node_activity_features['sq_0_sum'].append(summ(self.node_weights_sq[t[0]][0], self.node_weights_sq[t[1]][0]))
            self.node_activity_features['sq_0_sum'].append(summ(self.node_weights_sq[f[0]][0], self.node_weights_sq[f[1]][0]))

            self.node_activity_features['lin_1_sum'].append(summ(self.node_weights_lin[t[0]][1], self.node_weights_lin[t[1]][1]))
            self.node_activity_features['lin_1_sum'].append(summ(self.node_weights_lin[f[0]][1], self.node_weights_lin[f[1]][1]))
            self.node_activity_features['exp_1_sum'].append(summ(self.node_weights_exp[t[0]][1], self.node_weights_exp[t[1]][1]))
            self.node_activity_features['exp_1_sum'].append(summ(self.node_weights_exp[f[0]][1], self.node_weights_exp[f[1]][1]))
            self.node_activity_features['sq_1_sum'].append(summ(self.node_weights_sq[t[0]][1], self.node_weights_sq[t[1]][1]))
            self.node_activity_features['sq_1_sum'].append(summ(self.node_weights_sq[f[0]][1], self.node_weights_sq[f[1]][1]))

            self.node_activity_features['lin_2_sum'].append(summ(self.node_weights_lin[t[0]][2], self.node_weights_lin[t[1]][2]))
            self.node_activity_features['lin_2_sum'].append(summ(self.node_weights_lin[f[0]][2], self.node_weights_lin[f[1]][2]))
            self.node_activity_features['exp_2_sum'].append(summ(self.node_weights_exp[t[0]][2], self.node_weights_exp[t[1]][2]))
            self.node_activity_features['exp_2_sum'].append(summ(self.node_weights_exp[f[0]][2], self.node_weights_exp[f[1]][2]))
            self.node_activity_features['sq_2_sum'].append(summ(self.node_weights_sq[t[0]][2], self.node_weights_sq[t[1]][2]))
            self.node_activity_features['sq_2_sum'].append(summ(self.node_weights_sq[f[0]][2], self.node_weights_sq[f[1]][2]))

            self.node_activity_features['lin_3_sum'].append(summ(self.node_weights_lin[t[0]][3], self.node_weights_lin[t[1]][3]))
            self.node_activity_features['lin_3_sum'].append(summ(self.node_weights_lin[f[0]][3], self.node_weights_lin[f[1]][3]))
            self.node_activity_features['exp_3_sum'].append(summ(self.node_weights_exp[t[0]][3], self.node_weights_exp[t[1]][3]))
            self.node_activity_features['exp_3_sum'].append(summ(self.node_weights_exp[f[0]][3], self.node_weights_exp[f[1]][3]))
            self.node_activity_features['sq_3_sum'].append(summ(self.node_weights_sq[t[0]][3], self.node_weights_sq[t[1]][3]))
            self.node_activity_features['sq_3_sum'].append(summ(self.node_weights_sq[f[0]][3], self.node_weights_sq[f[1]][3]))

            self.node_activity_features['lin_4_sum'].append(summ(self.node_weights_lin[t[0]][4], self.node_weights_lin[t[1]][4]))
            self.node_activity_features['lin_4_sum'].append(summ(self.node_weights_lin[f[0]][4], self.node_weights_lin[f[1]][4]))
            self.node_activity_features['exp_4_sum'].append(summ(self.node_weights_exp[t[0]][4], self.node_weights_exp[t[1]][4]))
            self.node_activity_features['exp_4_sum'].append(summ(self.node_weights_exp[f[0]][4], self.node_weights_exp[f[1]][4]))
            self.node_activity_features['sq_4_sum'].append(summ(self.node_weights_sq[t[0]][4], self.node_weights_sq[t[1]][4]))
            self.node_activity_features['sq_4_sum'].append(summ(self.node_weights_sq[f[0]][4], self.node_weights_sq[f[1]][4]))

            self.node_activity_features['lin_5_sum'].append(summ(self.node_weights_lin[t[0]][5], self.node_weights_lin[t[1]][5]))
            self.node_activity_features['lin_5_sum'].append(summ(self.node_weights_lin[f[0]][5], self.node_weights_lin[f[1]][5]))
            self.node_activity_features['exp_5_sum'].append(summ(self.node_weights_exp[t[0]][5], self.node_weights_exp[t[1]][5]))
            self.node_activity_features['exp_5_sum'].append(summ(self.node_weights_exp[f[0]][5], self.node_weights_exp[f[1]][5]))
            self.node_activity_features['sq_5_sum'].append(summ(self.node_weights_sq[t[0]][5], self.node_weights_sq[t[1]][5]))
            self.node_activity_features['sq_5_sum'].append(summ(self.node_weights_sq[f[0]][5], self.node_weights_sq[f[1]][5]))

            self.node_activity_features['lin_6_sum'].append(summ(self.node_weights_lin[t[0]][6], self.node_weights_lin[t[1]][6]))
            self.node_activity_features['lin_6_sum'].append(summ(self.node_weights_lin[f[0]][6], self.node_weights_lin[f[1]][6]))
            self.node_activity_features['exp_6_sum'].append(summ(self.node_weights_exp[t[0]][6], self.node_weights_exp[t[1]][6]))
            self.node_activity_features['exp_6_sum'].append(summ(self.node_weights_exp[f[0]][6], self.node_weights_exp[f[1]][6]))
            self.node_activity_features['sq_6_sum'].append(summ(self.node_weights_sq[t[0]][6], self.node_weights_sq[t[1]][6]))
            self.node_activity_features['sq_6_sum'].append(summ(self.node_weights_sq[f[0]][6], self.node_weights_sq[f[1]][6]))

            dif = lambda x, y: abs(x - y)

            self.node_activity_features['lin_0_dif'].append(dif(self.node_weights_lin[t[0]][0], self.node_weights_lin[t[1]][0]))
            self.node_activity_features['lin_0_dif'].append(dif(self.node_weights_lin[f[0]][0], self.node_weights_lin[f[1]][0]))
            self.node_activity_features['exp_0_dif'].append(dif(self.node_weights_exp[t[0]][0], self.node_weights_exp[t[1]][0]))
            self.node_activity_features['exp_0_dif'].append(dif(self.node_weights_exp[f[0]][0], self.node_weights_exp[f[1]][0]))
            self.node_activity_features['sq_0_dif'].append(dif(self.node_weights_sq[t[0]][0], self.node_weights_sq[t[1]][0]))
            self.node_activity_features['sq_0_dif'].append(dif(self.node_weights_sq[f[0]][0], self.node_weights_sq[f[1]][0]))

            self.node_activity_features['lin_1_dif'].append(dif(self.node_weights_lin[t[0]][1], self.node_weights_lin[t[1]][1]))
            self.node_activity_features['lin_1_dif'].append(dif(self.node_weights_lin[f[0]][1], self.node_weights_lin[f[1]][1]))
            self.node_activity_features['exp_1_dif'].append(dif(self.node_weights_exp[t[0]][1], self.node_weights_exp[t[1]][1]))
            self.node_activity_features['exp_1_dif'].append(dif(self.node_weights_exp[f[0]][1], self.node_weights_exp[f[1]][1]))
            self.node_activity_features['sq_1_dif'].append(dif(self.node_weights_sq[t[0]][1], self.node_weights_sq[t[1]][1]))
            self.node_activity_features['sq_1_dif'].append(dif(self.node_weights_sq[f[0]][1], self.node_weights_sq[f[1]][1]))

            self.node_activity_features['lin_2_dif'].append(dif(self.node_weights_lin[t[0]][2], self.node_weights_lin[t[1]][2]))
            self.node_activity_features['lin_2_dif'].append(dif(self.node_weights_lin[f[0]][2], self.node_weights_lin[f[1]][2]))
            self.node_activity_features['exp_2_dif'].append(dif(self.node_weights_exp[t[0]][2], self.node_weights_exp[t[1]][2]))
            self.node_activity_features['exp_2_dif'].append(dif(self.node_weights_exp[f[0]][2], self.node_weights_exp[f[1]][2]))
            self.node_activity_features['sq_2_dif'].append(dif(self.node_weights_sq[t[0]][2], self.node_weights_sq[t[1]][2]))
            self.node_activity_features['sq_2_dif'].append(dif(self.node_weights_sq[f[0]][2], self.node_weights_sq[f[1]][2]))

            self.node_activity_features['lin_3_dif'].append(dif(self.node_weights_lin[t[0]][3], self.node_weights_lin[t[1]][3]))
            self.node_activity_features['lin_3_dif'].append(dif(self.node_weights_lin[f[0]][3], self.node_weights_lin[f[1]][3]))
            self.node_activity_features['exp_3_dif'].append(dif(self.node_weights_exp[t[0]][3], self.node_weights_exp[t[1]][3]))
            self.node_activity_features['exp_3_dif'].append(dif(self.node_weights_exp[f[0]][3], self.node_weights_exp[f[1]][3]))
            self.node_activity_features['sq_3_dif'].append(dif(self.node_weights_sq[t[0]][3], self.node_weights_sq[t[1]][3]))
            self.node_activity_features['sq_3_dif'].append(dif(self.node_weights_sq[f[0]][3], self.node_weights_sq[f[1]][3]))

            self.node_activity_features['lin_4_dif'].append(dif(self.node_weights_lin[t[0]][4], self.node_weights_lin[t[1]][4]))
            self.node_activity_features['lin_4_dif'].append(dif(self.node_weights_lin[f[0]][4], self.node_weights_lin[f[1]][4]))
            self.node_activity_features['exp_4_dif'].append(dif(self.node_weights_exp[t[0]][4], self.node_weights_exp[t[1]][4]))
            self.node_activity_features['exp_4_dif'].append(dif(self.node_weights_exp[f[0]][4], self.node_weights_exp[f[1]][4]))
            self.node_activity_features['sq_4_dif'].append(dif(self.node_weights_sq[t[0]][4], self.node_weights_sq[t[1]][4]))
            self.node_activity_features['sq_4_dif'].append(dif(self.node_weights_sq[f[0]][4], self.node_weights_sq[f[1]][4]))

            self.node_activity_features['lin_5_dif'].append(dif(self.node_weights_lin[t[0]][5], self.node_weights_lin[t[1]][5]))
            self.node_activity_features['lin_5_dif'].append(dif(self.node_weights_lin[f[0]][5], self.node_weights_lin[f[1]][5]))
            self.node_activity_features['exp_5_dif'].append(dif(self.node_weights_exp[t[0]][5], self.node_weights_exp[t[1]][5]))
            self.node_activity_features['exp_5_dif'].append(dif(self.node_weights_exp[f[0]][5], self.node_weights_exp[f[1]][5]))
            self.node_activity_features['sq_5_dif'].append(dif(self.node_weights_sq[t[0]][5], self.node_weights_sq[t[1]][5]))
            self.node_activity_features['sq_5_dif'].append(dif(self.node_weights_sq[f[0]][5], self.node_weights_sq[f[1]][5]))

            self.node_activity_features['lin_6_dif'].append(dif(self.node_weights_lin[t[0]][6], self.node_weights_lin[t[1]][6]))
            self.node_activity_features['lin_6_dif'].append(dif(self.node_weights_lin[f[0]][6], self.node_weights_lin[f[1]][6]))
            self.node_activity_features['exp_6_dif'].append(dif(self.node_weights_exp[t[0]][6], self.node_weights_exp[t[1]][6]))
            self.node_activity_features['exp_6_dif'].append(dif(self.node_weights_exp[f[0]][6], self.node_weights_exp[f[1]][6]))
            self.node_activity_features['sq_6_dif'].append(dif(self.node_weights_sq[t[0]][6], self.node_weights_sq[t[1]][6]))
            self.node_activity_features['sq_6_dif'].append(dif(self.node_weights_sq[f[0]][6], self.node_weights_sq[f[1]][6]))

            # --------------------------------------------------

            self.node_activity_features['lin_0_min'].append(min(self.node_weights_lin[t[0]][0], self.node_weights_lin[t[1]][0]))
            self.node_activity_features['lin_0_min'].append(min(self.node_weights_lin[f[0]][0], self.node_weights_lin[f[1]][0]))
            self.node_activity_features['exp_0_min'].append(min(self.node_weights_exp[t[0]][0], self.node_weights_exp[t[1]][0]))
            self.node_activity_features['exp_0_min'].append(min(self.node_weights_exp[f[0]][0], self.node_weights_exp[f[1]][0]))
            self.node_activity_features['sq_0_min'].append(min(self.node_weights_sq[t[0]][0], self.node_weights_sq[t[1]][0]))
            self.node_activity_features['sq_0_min'].append(min(self.node_weights_sq[f[0]][0], self.node_weights_sq[f[1]][0]))

            self.node_activity_features['lin_1_min'].append(min(self.node_weights_lin[t[0]][1], self.node_weights_lin[t[1]][1]))
            self.node_activity_features['lin_1_min'].append(min(self.node_weights_lin[f[0]][1], self.node_weights_lin[f[1]][1]))
            self.node_activity_features['exp_1_min'].append(min(self.node_weights_exp[t[0]][1], self.node_weights_exp[t[1]][1]))
            self.node_activity_features['exp_1_min'].append(min(self.node_weights_exp[f[0]][1], self.node_weights_exp[f[1]][1]))
            self.node_activity_features['sq_1_min'].append(min(self.node_weights_sq[t[0]][1], self.node_weights_sq[t[1]][1]))
            self.node_activity_features['sq_1_min'].append(min(self.node_weights_sq[f[0]][1], self.node_weights_sq[f[1]][1]))

            self.node_activity_features['lin_2_min'].append(min(self.node_weights_lin[t[0]][2], self.node_weights_lin[t[1]][2]))
            self.node_activity_features['lin_2_min'].append(min(self.node_weights_lin[f[0]][2], self.node_weights_lin[f[1]][2]))
            self.node_activity_features['exp_2_min'].append(min(self.node_weights_exp[t[0]][2], self.node_weights_exp[t[1]][2]))
            self.node_activity_features['exp_2_min'].append(min(self.node_weights_exp[f[0]][2], self.node_weights_exp[f[1]][2]))
            self.node_activity_features['sq_2_min'].append(min(self.node_weights_sq[t[0]][2], self.node_weights_sq[t[1]][2]))
            self.node_activity_features['sq_2_min'].append(min(self.node_weights_sq[f[0]][2], self.node_weights_sq[f[1]][2]))

            self.node_activity_features['lin_3_min'].append(min(self.node_weights_lin[t[0]][3], self.node_weights_lin[t[1]][3]))
            self.node_activity_features['lin_3_min'].append(min(self.node_weights_lin[f[0]][3], self.node_weights_lin[f[1]][3]))
            self.node_activity_features['exp_3_min'].append(min(self.node_weights_exp[t[0]][3], self.node_weights_exp[t[1]][3]))
            self.node_activity_features['exp_3_min'].append(min(self.node_weights_exp[f[0]][3], self.node_weights_exp[f[1]][3]))
            self.node_activity_features['sq_3_min'].append(min(self.node_weights_sq[t[0]][3], self.node_weights_sq[t[1]][3]))
            self.node_activity_features['sq_3_min'].append(min(self.node_weights_sq[f[0]][3], self.node_weights_sq[f[1]][3]))

            self.node_activity_features['lin_4_min'].append(min(self.node_weights_lin[t[0]][4], self.node_weights_lin[t[1]][4]))
            self.node_activity_features['lin_4_min'].append(min(self.node_weights_lin[f[0]][4], self.node_weights_lin[f[1]][4]))
            self.node_activity_features['exp_4_min'].append(min(self.node_weights_exp[t[0]][4], self.node_weights_exp[t[1]][4]))
            self.node_activity_features['exp_4_min'].append(min(self.node_weights_exp[f[0]][4], self.node_weights_exp[f[1]][4]))
            self.node_activity_features['sq_4_min'].append(min(self.node_weights_sq[t[0]][4], self.node_weights_sq[t[1]][4]))
            self.node_activity_features['sq_4_min'].append(min(self.node_weights_sq[f[0]][4], self.node_weights_sq[f[1]][4]))

            self.node_activity_features['lin_5_min'].append(min(self.node_weights_lin[t[0]][5], self.node_weights_lin[t[1]][5]))
            self.node_activity_features['lin_5_min'].append(min(self.node_weights_lin[f[0]][5], self.node_weights_lin[f[1]][5]))
            self.node_activity_features['exp_5_min'].append(min(self.node_weights_exp[t[0]][5], self.node_weights_exp[t[1]][5]))
            self.node_activity_features['exp_5_min'].append(min(self.node_weights_exp[f[0]][5], self.node_weights_exp[f[1]][5]))
            self.node_activity_features['sq_5_min'].append(min(self.node_weights_sq[t[0]][5], self.node_weights_sq[t[1]][5]))
            self.node_activity_features['sq_5_min'].append(min(self.node_weights_sq[f[0]][5], self.node_weights_sq[f[1]][5]))

            self.node_activity_features['lin_6_min'].append(min(self.node_weights_lin[t[0]][6], self.node_weights_lin[t[1]][6]))
            self.node_activity_features['lin_6_min'].append(min(self.node_weights_lin[f[0]][6], self.node_weights_lin[f[1]][6]))
            self.node_activity_features['exp_6_min'].append(min(self.node_weights_exp[t[0]][6], self.node_weights_exp[t[1]][6]))
            self.node_activity_features['exp_6_min'].append(min(self.node_weights_exp[f[0]][6], self.node_weights_exp[f[1]][6]))
            self.node_activity_features['sq_6_min'].append(min(self.node_weights_sq[t[0]][6], self.node_weights_sq[t[1]][6]))
            self.node_activity_features['sq_6_min'].append(min(self.node_weights_sq[f[0]][6], self.node_weights_sq[f[1]][6]))

            # --------------------------------------------------

            self.node_activity_features['lin_0_max'].append(max(self.node_weights_lin[t[0]][0], self.node_weights_lin[t[1]][0]))
            self.node_activity_features['lin_0_max'].append(max(self.node_weights_lin[f[0]][0], self.node_weights_lin[f[1]][0]))
            self.node_activity_features['exp_0_max'].append(max(self.node_weights_exp[t[0]][0], self.node_weights_exp[t[1]][0]))
            self.node_activity_features['exp_0_max'].append(max(self.node_weights_exp[f[0]][0], self.node_weights_exp[f[1]][0]))
            self.node_activity_features['sq_0_max'].append(max(self.node_weights_sq[t[0]][0], self.node_weights_sq[t[1]][0]))
            self.node_activity_features['sq_0_max'].append(max(self.node_weights_sq[f[0]][0], self.node_weights_sq[f[1]][0]))

            self.node_activity_features['lin_1_max'].append(max(self.node_weights_lin[t[0]][1], self.node_weights_lin[t[1]][1]))
            self.node_activity_features['lin_1_max'].append(max(self.node_weights_lin[f[0]][1], self.node_weights_lin[f[1]][1]))
            self.node_activity_features['exp_1_max'].append(max(self.node_weights_exp[t[0]][1], self.node_weights_exp[t[1]][1]))
            self.node_activity_features['exp_1_max'].append(max(self.node_weights_exp[f[0]][1], self.node_weights_exp[f[1]][1]))
            self.node_activity_features['sq_1_max'].append(max(self.node_weights_sq[t[0]][1], self.node_weights_sq[t[1]][1]))
            self.node_activity_features['sq_1_max'].append(max(self.node_weights_sq[f[0]][1], self.node_weights_sq[f[1]][1]))

            self.node_activity_features['lin_2_max'].append(max(self.node_weights_lin[t[0]][2], self.node_weights_lin[t[1]][2]))
            self.node_activity_features['lin_2_max'].append(max(self.node_weights_lin[f[0]][2], self.node_weights_lin[f[1]][2]))
            self.node_activity_features['exp_2_max'].append(max(self.node_weights_exp[t[0]][2], self.node_weights_exp[t[1]][2]))
            self.node_activity_features['exp_2_max'].append(max(self.node_weights_exp[f[0]][2], self.node_weights_exp[f[1]][2]))
            self.node_activity_features['sq_2_max'].append(max(self.node_weights_sq[t[0]][2], self.node_weights_sq[t[1]][2]))
            self.node_activity_features['sq_2_max'].append(max(self.node_weights_sq[f[0]][2], self.node_weights_sq[f[1]][2]))

            self.node_activity_features['lin_3_max'].append(max(self.node_weights_lin[t[0]][3], self.node_weights_lin[t[1]][3]))
            self.node_activity_features['lin_3_max'].append(max(self.node_weights_lin[f[0]][3], self.node_weights_lin[f[1]][3]))
            self.node_activity_features['exp_3_max'].append(max(self.node_weights_exp[t[0]][3], self.node_weights_exp[t[1]][3]))
            self.node_activity_features['exp_3_max'].append(max(self.node_weights_exp[f[0]][3], self.node_weights_exp[f[1]][3]))
            self.node_activity_features['sq_3_max'].append(max(self.node_weights_sq[t[0]][3], self.node_weights_sq[t[1]][3]))
            self.node_activity_features['sq_3_max'].append(max(self.node_weights_sq[f[0]][3], self.node_weights_sq[f[1]][3]))

            self.node_activity_features['lin_4_max'].append(max(self.node_weights_lin[t[0]][4], self.node_weights_lin[t[1]][4]))
            self.node_activity_features['lin_4_max'].append(max(self.node_weights_lin[f[0]][4], self.node_weights_lin[f[1]][4]))
            self.node_activity_features['exp_4_max'].append(max(self.node_weights_exp[t[0]][4], self.node_weights_exp[t[1]][4]))
            self.node_activity_features['exp_4_max'].append(max(self.node_weights_exp[f[0]][4], self.node_weights_exp[f[1]][4]))
            self.node_activity_features['sq_4_max'].append(max(self.node_weights_sq[t[0]][4], self.node_weights_sq[t[1]][4]))
            self.node_activity_features['sq_4_max'].append(max(self.node_weights_sq[f[0]][4], self.node_weights_sq[f[1]][4]))

            self.node_activity_features['lin_5_max'].append(max(self.node_weights_lin[t[0]][5], self.node_weights_lin[t[1]][5]))
            self.node_activity_features['lin_5_max'].append(max(self.node_weights_lin[f[0]][5], self.node_weights_lin[f[1]][5]))
            self.node_activity_features['exp_5_max'].append(max(self.node_weights_exp[t[0]][5], self.node_weights_exp[t[1]][5]))
            self.node_activity_features['exp_5_max'].append(max(self.node_weights_exp[f[0]][5], self.node_weights_exp[f[1]][5]))
            self.node_activity_features['sq_5_max'].append(max(self.node_weights_sq[t[0]][5], self.node_weights_sq[t[1]][5]))
            self.node_activity_features['sq_5_max'].append(max(self.node_weights_sq[f[0]][5], self.node_weights_sq[f[1]][5]))

            self.node_activity_features['lin_6_max'].append(max(self.node_weights_lin[t[0]][6], self.node_weights_lin[t[1]][6]))
            self.node_activity_features['lin_6_max'].append(max(self.node_weights_lin[f[0]][6], self.node_weights_lin[f[1]][6]))
            self.node_activity_features['exp_6_max'].append(max(self.node_weights_exp[t[0]][6], self.node_weights_exp[t[1]][6]))
            self.node_activity_features['exp_6_max'].append(max(self.node_weights_exp[f[0]][6], self.node_weights_exp[f[1]][6]))
            self.node_activity_features['sq_6_max'].append(max(self.node_weights_sq[t[0]][6], self.node_weights_sq[t[1]][6]))
            self.node_activity_features['sq_6_max'].append(max(self.node_weights_sq[f[0]][6], self.node_weights_sq[f[1]][6]))

    def get_node_activity_features_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.node_activity_features)
        normalized_df = (df - df.min()) / (df.max() - df.min())
        return normalized_df
