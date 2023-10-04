#pragma once

#include <vector>
#include <functional>
#include <stack>
#include <queue>
#include <random>
#include <set>
#include <map>
#include <unordered_set>
#include "tools/benchmark.hpp"

namespace Graph
{

    using Vertex = unsigned int;
    using Edge = std::pair<Vertex, Vertex>;
    using Index = size_t;

    struct EdgeTime
    {
        EdgeTime(Vertex v1, Vertex v2, size_t time): vertex1_(v1), vertex2_(v2), time_(time) {}

        Vertex vertex1_, vertex2_;
        size_t time_;
    };

    struct GraphData
    {
        std::vector<EdgeTime> edges_;
        std::vector<Vertex> vertices_;

        void timeSort()
        {
            std::sort(edges_.begin(), edges_.end(), [](EdgeTime& edge1, EdgeTime& edge2)
            {
                if (edge1.time_ == edge2.time_)
                {
                    if (edge1.vertex1_ == edge2.vertex1_)
                    {
                        return edge1.vertex2_ <= edge2.vertex2_;
                    }
                    return edge1.vertex1_ <= edge2.vertex1_;
                }
                return edge1.time_ <= edge2.time_;
            });
        }

        void edgeSort()
        {
            std::sort(edges_.begin(), edges_.end(), [](EdgeTime& edge1, EdgeTime& edge2)
            {
                if (edge1.vertex1_ == edge2.vertex1_)
                {
                    return edge1.vertex2_ <= edge2.vertex2_;
                }
                return edge1.vertex1_ <= edge2.vertex1_;
            });
        }

    };

    class Graph
    {
    public:

        Graph(const GraphData& graph_data): 
            time_(0.), 
            adj_list_(graph_data.vertices_.size()),
            all_edges_(graph_data.edges_),
            accord_v_(graph_data.vertices_),
            accord_m_()
        {
            for (size_t i = 0; i < graph_data.vertices_.size(); ++i)
            {
                accord_m_[graph_data.vertices_[i]] = i;
            }
        }

        Graph(const Graph& graph): 
            time_(graph.time_),
            adj_list_(graph.adj_list_),
            all_edges_(graph.all_edges_),
            accord_v_(graph.accord_v_),
            accord_m_(graph.accord_m_) {}

        Graph(Graph&& graph): 
            time_(std::move(graph.time_)),
            adj_list_(std::move(graph.adj_list_)),
            all_edges_(std::move(graph.all_edges_)),
            accord_v_(std::move(graph.accord_v_)),
            accord_m_(std::move(graph.accord_m_)) {}

        // O(m)
        void setTime(size_t time)
        {
            time_ = time;
            for (auto& adj: adj_list_)
            {
                adj.clear();
            }

            LoopProgress progress(all_edges_.size(), "Set new time");

            for (auto& edge: all_edges_)
            {
                if (edge.time_ <= time)
                {
                    adj_list_[getAccordIndex_(edge.vertex1_)].insert(getAccordIndex_(edge.vertex2_));
                    adj_list_[getAccordIndex_(edge.vertex2_)].insert(getAccordIndex_(edge.vertex1_));
                }
                progress.update();
            }
        }

        // O(1)
        size_t getTime() const
        {
            return time_;
        }

        // O(1)
        size_t getNumVertices() const 
        {
            return adj_list_.size();
        }
        
        // O(n)
        size_t getNumEdges() const 
        {
            size_t ans = 0;
            for (auto& adj: adj_list_)
            {
                ans += adj.size();
            }
            return ans / 2;
        }
        
        // O(1)
        double getDensity() const
        {
            return  (double)getNumEdges() / getMaxNumEdges_();
        }
        
        // O(n + m)
        std::vector<std::vector<Vertex>> getWeakComponents() const
        {
            std::vector<bool> is_visit(adj_list_.size(), false);
            std::vector<size_t> component;
            std::function isVisit = [&is_visit](size_t index){return is_visit[index];};
            std::function check = [&is_visit, &component](size_t index)
            {
                is_visit[index] = true;
                component.emplace_back(index); 
            };
            std::vector<std::vector<Vertex>> ans;
            for (size_t index = 0; index < adj_list_.size(); ++index)
            {
                if (!isVisit(index))
                {
                    dfs_(index, isVisit, check);
                    ans.emplace_back(getAccordVertices_(component));
                    component.clear();
                }
            }
            return ans;
        }

        // O(n^2 + n*m)
        double getPercentile(double val) const
        {
            val /= 100.;
            std::vector<int> count_dists(adj_list_.size());
            int count = 0;
            for (Index index = 0; index < adj_list_.size(); ++index)
            {
                for (int dist: getDistances_(index))
                {
                    if (dist > 0)
                    {
                        ++count_dists[dist];
                        ++count; 
                    }
                }
            }
            double ans = 0;
            int sum = 0;
            for (size_t i = 1; i < adj_list_.size(); ++i)
            {
                if (sum + count_dists[i] - val * count >= 0)
                {
                    ans = i;
                    break;
                }
                ans = i;
                sum += count_dists[i];
            }
            return ans;
        }

        // O(n1(n + m))
        double getPercentile(double val, const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            val /= 100.;
            std::vector<int> count_dists(adj_list_.size());
            int count = 0;
            for (Index index: indices)
            {
                for (int dist: getDistances_(index))
                {
                    if (dist > 0)
                    {
                        ++count_dists[dist];
                        ++count; 
                    }
                }
            }
            double ans = 0;
            int sum = 0;
            for (size_t i = 1; i < adj_list_.size(); ++i)
            {
                if (sum + count_dists[i] - val * count >= 0)
                {
                    ans = i;
                    break;
                }
                ans = i;
                sum += count_dists[i];
            }
            return ans;
        }

        // O(n^2 + n*m)
        size_t getRadius() const
        {
            size_t ans = adj_list_.size();
            for (Index index = 0; index < adj_list_.size(); ++index)
            {
                ans = std::min(ans, (size_t)std::max(0, getEccentricity_(index)));
            }
            return ans;
        }

        // O(n1(n + m))
        size_t getRadius(const std::vector<Vertex>& vertices)
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            LoopProgress progress(vertices.size(), "Radius");
            size_t ans = adj_list_.size();
            for (Index index: indices)
            {
                ans = std::min(ans, (size_t)std::max(0, getEccentricity_(index)));
                progress.update();
            }
            return ans;
        }

        // O(n^2 + n*m)
        size_t getDiameter() const
        {
            size_t ans = 0;
            for (Index index = 0; index < adj_list_.size(); ++index)
            {
                ans = std::max(ans, (size_t)std::max(0, getEccentricity_(index)));
            }
            return ans;
        }

        // O(n1(n + m))
        size_t getDiameter(const std::vector<Vertex>& vertices)
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            size_t ans = 0;
            for (Index index: indices)
            {
                ans = std::max(ans, (size_t)std::max(0, getEccentricity_(index)));
            }
            return ans;
        }

        // O(m)
        std::vector<Vertex> getRandomSubgraph(size_t subgraph_size) const
        {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::vector<Vertex> vertices(adj_list_.size());
            for (Index index = 0; index <= adj_list_.size(); ++index)
            {
                vertices[index] = getAccordVertex_(index);
            }
            if (vertices.size() > subgraph_size)
            {
                std::shuffle(vertices.begin(), vertices.end(), gen);
                vertices.resize(subgraph_size);
            }
            return vertices;
        }

        // O(n + m)
        std::vector<Vertex> getSnowballSubgraph(size_t subgraph_size) const
        {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::vector<Index> indecies(adj_list_.size());
            for (Index index = 0; index < adj_list_.size(); ++index)
            {
                indecies[index] = index;
            }

            std::vector<bool> is_visit(adj_list_.size());
            std::function isVisit = [&is_visit](size_t index){return is_visit[index];};
            std::function fun = [&is_visit](size_t parent, size_t son){is_visit[son] = true;};
            size_t num_indices = 0;

            while(num_indices < subgraph_size && !indecies.empty())
            {
                std::swap(indecies.back(), indecies[std::uniform_int_distribution<size_t>(0, indecies.size() - 1)(gen)]);
                Index index = indecies[indecies.size() - 1];
                indecies.resize(indecies.size() - 1);
                if (!is_visit[index])
                {
                    bfs_(index, isVisit, fun);
                }
            }

            std::vector<Vertex> vertices;
            for (size_t i = 0; i < adj_list_.size(); ++i)
            {
                if (is_visit[i])
                {
                    vertices.emplace_back(getAccordVertex_(i));
                }
            }

            if (vertices.size() > subgraph_size)
            {
                std::shuffle(vertices.begin(), vertices.end(), gen);
                vertices.resize(subgraph_size);
            }

            return vertices;
        }

        // O(m)
        Graph extractSubgraph(const std::vector<Vertex>& vertices) const
        {
            std::set<Vertex> vertices_s;

            for (Vertex vertex: vertices)
            {
                vertices_s.insert(vertex);
            }

            GraphData graph_data;

            for (auto& edge: all_edges_)
            {
                if (vertices_s.find(edge.vertex1_) != vertices_s.end() && vertices_s.find(edge.vertex2_) != vertices_s.end())
                {
                    graph_data.edges_.emplace_back(edge);
                }
            }
            graph_data.vertices_ = vertices;
            Graph graph(graph_data);
            graph.setTime(time_);

            return graph;
        }

        // O(R2)
        double getClusteringCoefficient() const
        {
            double res = 0.;
            for (auto& neighbors: adj_list_)
            {
                if (neighbors.size() <= 1)
                {
                    continue;
                }
                double tmp_res = 0.;
                for (Index index1: neighbors)
                {
                    for (Index index2: neighbors)
                    {
                        if (index1 == index2)
                        {
                            continue;
                        }
                        if (adj_list_[index1].find(index2) != adj_list_[index1].end())
                        {
                            ++tmp_res;
                        }
                    }
                }
                res += tmp_res / (neighbors.size() * (neighbors.size() - 1));
            }
            return res / adj_list_.size();
        }

        double getClusteringCoefficient(const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            double res = 0.;
            for (Index index: indices)
            {
                if (adj_list_[index].size() <= 1)
                {
                    continue;
                }
                double tmp_res = 0.;
                for (Index index1: adj_list_[index])
                {
                    for (Index index2: adj_list_[index])
                    {
                        if (index1 == index2)
                        {
                            continue;
                        }
                        if (adj_list_[index1].find(index2) != adj_list_[index1].end())
                        {
                            ++tmp_res;
                        }
                    }
                }
                res += tmp_res / (adj_list_[index].size() * (adj_list_[index].size() - 1));
            }
            return res / vertices.size();
        }

        // O(n + m)
        double getPearsonsCoefficient() const
        {
            double R1 = getR1(), R2 = getR2(), R3 = getR3(), Re = getRe();
            return (double)(Re * R1 - R2 * R2) / (R3 * R1 - R2 * R2);
        }

        // O(n + m)
        double getPearsonsCoefficient(const std::vector<Vertex>& vertices) const
        {
            double R1 = getR1(vertices), R2 = getR2(vertices), R3 = getR3(vertices), Re = getRe(vertices);
            return (double)(Re * R1 - R2 * R2) / (R3 * R1 - R2 * R2);
        }

        // O(neighbours / log(k))
        const std::vector<Vertex>& getNeighbors(Vertex vertex)
        {
            if (neighbours_buffer_.find(vertex) != neighbours_buffer_.end())
            {
                return neighbours_buffer_.at(vertex);
            }
            std::vector<Vertex> vertices;
            for (Index index: adj_list_[getAccordIndex_(vertex)])
            {
                vertices.emplace_back(getAccordVertex_(index));
            }
            return neighbours_buffer_[vertex] = vertices;
        }

        // O(common neighbours / log(k))
        const std::vector<Vertex>& getCommonNeighbours(Edge edge)
        {
            edge = getKeyEdge_(edge);
            if (common_neighbours_buffer_.find(edge) != common_neighbours_buffer_.end())
            {
                return common_neighbours_buffer_.at(edge);
            }
            Edge edge_index = getKeyEdge_({getAccordIndex_(edge.first), getAccordIndex_(edge.second)});
            std::vector<Vertex> res;
            for (Index index: adj_list_[edge_index.first])
            {
                if (adj_list_[edge_index.second].find(index) != adj_list_[edge_index.second].end())
                {
                    res.emplace_back(getAccordVertex_(index));
                }
            }
            return common_neighbours_buffer_[edge] = res;
        }

        // O(log(neighbours(edge)))
        bool isExist(Edge edge) const
        {
            std::pair<Index, Index> edge_index = {getAccordIndex_(edge.first), getAccordIndex_(edge.second)};
            if (adj_list_[edge_index.first].find(edge_index.second) != adj_list_[edge_index.first].end())
            {
                return true;
            }
            return false;
        }

        // O(log(n))
        size_t getNeighborsSize(Vertex vertex) const
        {
            return adj_list_[getAccordIndex_(vertex)].size();
        }

        // O(n + m)
        int getDistance(Edge edge) const
        {
            return getDistances_(getAccordIndex_(edge.first))[getAccordIndex_(edge.second)];
        }

        // O(n)
        // std::set<unsigned int> getUniqueNeighbours(std::pair<unsigned int, unsigned int> edge) const
        // {
        //     std::pair<size_t, size_t> edge_index = {getAccordIndex_(edge.first), getAccordIndex_(edge.second)};
        //     std::set<size_t> ans_index = getNeighbors(edge_index.first);
        //     for ( vertex: getNeighbors(edge_index.second))
        //     {
        //         ans.insert(vertex);
        //     }
        //     return ans;
        // }

        // O(common neighbours / log(n))
        size_t getUniqueNeighboursSize(Edge edge)
        {
            return getNeighborsSize(edge.first) + getNeighborsSize(edge.second) - getCommonNeighbours(edge).size();
        }

        // O(n + m)
        std::vector<Vertex> getVerticesInDistance2(Vertex vertex) const
        {
            Index index = getAccordIndex_(vertex);
            std::vector<Vertex> res;
            std::queue<Index> que;
            que.push(index);
            std::vector<int> dists(adj_list_.size(), -1);
            dists[index] = 0;

            while(!que.empty())
            {
                Index cur = que.front(); que.pop();
                for (Index neighbor: adj_list_[cur])
                {
                    if (dists[neighbor] == -1)
                    {
                        dists[neighbor] = dists[cur] + 1;
                        if (dists[neighbor] < 2)
                        {
                            que.push(neighbor);
                        }
                        else
                        {
                            res.emplace_back(getAccordVertex_(neighbor));
                        }
                    }
                }
            }
            return res;
        }

        // O(n)
        size_t getR1() const
        {
            size_t ans = 0;
            for (auto& neighbors: adj_list_)
            {
                ans += neighbors.size();
            }  
            return ans;
        }

        // O(n)
        size_t getR1(const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            size_t ans = 0;
            for (Index index: indices)
            {
                ans += adj_list_[index].size();
            }
            return ans;
        }

        // O(n)
        size_t getR2() const
        {
            size_t ans = 0;
            for (auto& neighbors: adj_list_)
            {
                ans += neighbors.size() * neighbors.size();
            }
            return ans;
        }

        // O(n)
        size_t getR2(const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            size_t ans = 0;
            for (Index index: indices)
            {
                ans += adj_list_[index].size() * adj_list_[index].size();
            }
            return ans;
        }

        // O(n)
        size_t getR3() const
        {
            size_t ans = 0;
            for (auto& neighbors: adj_list_)
            {
                ans += neighbors.size() * neighbors.size() * neighbors.size();
            }
            return ans;
        }

        // O(n)
        size_t getR3(const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            size_t ans = 0;
            for (Index index: indices)
            {
                ans += adj_list_[index].size() * adj_list_[index].size() * adj_list_[index].size();
            }
            return ans;
        }

        // O(m)
        size_t getRe() const
        {
            size_t ans = 0;
            for (auto& neighbors: adj_list_)
            {
                size_t temp_sum = 0;
                for (auto neighbor: neighbors)
                {
                    temp_sum += adj_list_[neighbor].size();
                }
                ans += temp_sum * neighbors.size();
            }
            return ans;
        }

        // O(n1^2)
        size_t getRe(const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices = getAccordIndices_(vertices);
            size_t ans = 0;
            for (Index index1: indices)
            {
                for (Index index2: indices)
                {
                    if (index1 == index2)
                    {
                        continue;
                    }
                    if (adj_list_[index1].find(index2) != adj_list_[index1].end())
                    {
                        ans += adj_list_[index1].size() * adj_list_[index2].size();
                    }
                }
            }
            return ans;
        }

        std::vector<size_t> getStaticData(const std::vector<Vertex>& vertices = {})
        {
            std::vector<Index> indices;
            if (vertices.empty())
            {
                for (Index index = 0; index <= adj_list_.size(); ++index)
                {
                    indices.emplace_back(index);
                }
            }
            else
            {
                for (Vertex vertix: vertices)
                {
                    indices.emplace_back(getAccordIndex_(vertix));
                }
            }

            size_t radius = adj_list_.size(), diameter = 0;
            std::vector<size_t> count_dists(adj_list_.size());        
            size_t count = 0;

            LoopProgress progress(indices.size(), "Radius / Diameter / 90 Percentile");

            for (Index index: indices)
            {
                size_t exc = 0;
                for (int dist: getDistances_(index))
                {
                    if (dist > 0)
                    {
                        exc = std::max(exc, (size_t)dist);
                        ++count_dists[dist];
                        ++count;
                    }
                }
                radius = std::min(radius, exc);
                diameter = std::max(diameter, exc);
                progress.update();
            }

            size_t perc = 0;
            int sum = 0;
            for (size_t i = 1; i < adj_list_.size(); ++i)
            {
                if (sum + count_dists[i] - 0.9 * count >= 0)
                {
                    perc = i;
                    break;
                }
                perc = i;
                sum += count_dists[i];
            }
            return {radius, diameter, perc};
        }

    private:

        Edge getKeyEdge_(Edge edge) const
        {
            return {std::min(edge.first, edge.second), std::max(edge.first, edge.second)};
        }

        Index getAccordIndex_(Vertex vertex) const
        {
            return accord_m_.at(vertex);
        }

        std::vector<Index> getAccordIndices_(const std::vector<Vertex>& vertices) const
        {
            std::vector<Index> indices(vertices.size());
            for (size_t i = 0; i < vertices.size(); ++i)
            {
                indices[i] = getAccordIndex_(vertices[i]);
            }
            return indices;
        }

        std::set<Index> getAccordIndices_(const std::set<Vertex>& vertices) const
        {
            std::set<Index> indices;
            for (Vertex vertex: vertices)
            {
                indices.insert(getAccordIndex_(vertex));
            }
            return indices;
        }

        Vertex getAccordVertex_(Index index) const
        {
            return accord_v_[index];
        }

        std::vector<Vertex> getAccordVertices_(const std::vector<Index>& indices) const
        {
            std::vector<Vertex> vertices(indices.size());
            for (size_t i = 0; i < indices.size(); ++i)
            {
                vertices[i] = getAccordVertex_(indices[i]);
            }
            return vertices;
        }

        std::set<Vertex> getAccordVertices_(const std::set<Index>& indices) const
        {
            std::set<Vertex> vertices;
            for (Index index: indices)
            {
                vertices.insert(getAccordVertex_(index));
            }
            return vertices;
        }

        // O(1)
        size_t getMaxNumEdges_() const  
        {
            return (adj_list_.size()) * (adj_list_.size() - 1) / 2.;
        }

        // O(n + m)
        void dfs_(
            Index start,
            std::function<bool(Index)> isVisit,
            std::function<void(Index)> fun = [](Index){}) const
        {
            std::stack<Index> st;
            if (!isVisit(start))
            {
                st.push(start);
                fun(start);
            }
            while(!st.empty())
            {
                Index cur = st.top();
                st.pop();
                for (Index index: adj_list_[cur])
                {
                    if (!isVisit(index))
                    {
                        st.push(index);
                        fun(index);
                    }
                }
            }
        }
        
        // O(n + m)
        void dfs_(
            Index start,
            std::function<void(Index)> fun = [](Index){}) const
        {
            std::vector<bool> is_visit;
            std::function isVisit = [&is_visit](Index index){return is_visit[index];};
            std::function funWrapper = [&fun, &is_visit](Index index)
            {
                is_visit[index] = true; 
                fun(index);
            };
            dfs_(start, isVisit, funWrapper);
        }

        // O(n + m)
        void bfs_(
            Index start,
            std::function<bool(Index)> isVisit,
            std::function<void(Index, Index)> fun = [](Index, Index){}) const
        {
            std::queue<Index> que;
            if (!isVisit(start))
            {
                que.push(start);
                fun(start, start);
            }
            while(!que.empty())
            {
                Index cur = que.front();
                que.pop();

                for (Index index: adj_list_[cur])
                {
                    if (!isVisit(index))
                    {
                        que.push(index);
                        fun(cur, index);
                    }
                }
            }
        }

        // O(n + m)
        std::vector<int> getDistances_(Index index) const
        {
            std::vector<int> dists(adj_list_.size(), -1);
            std::function isVisit = [&dists](Index index){return dists[index] != -1;};
            std::function fun = [&dists](Index parent, Index son)
            {
                if (son == parent) {dists[parent] = 0;}
                else {dists[son] = dists[parent] + 1;}
            };
            bfs_(index, isVisit, fun);
            return dists;
        }

        // O(n + m)
        int getEccentricity_(Index index) const
        {
            std::vector<int> dists = getDistances_(index);
            int ans = -1;
            for (int dist: dists)
            {
                if (dist == 0)
                {
                    continue;
                }
                ans = std::max(ans, dist);
            }
            
            return ans;
        }

        size_t time_;
        std::vector<std::unordered_set<Index>> adj_list_;
        std::vector<EdgeTime> all_edges_;
        std::vector<Vertex> accord_v_;
        std::unordered_map<Vertex, Index> accord_m_;
        std::map<Edge, std::vector<Vertex>> common_neighbours_buffer_;
        std::map<Vertex, std::vector<Vertex>> neighbours_buffer_;
    };

}