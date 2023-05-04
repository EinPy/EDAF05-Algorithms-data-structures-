#include <bits/stdc++.h>

using namespace std;


typedef long long ll;
typedef long double ld;

#define rep(q, i, a) for (int q = i; q < a; q++)
#define dwnrep(q, i) for (int q = i-1; q >= 0; q--)
#define vi vector<ll>
#define vii vector<vector<ll>>
#define pb(q) push_back(q)
#define vpq vector<priority_queue<ll>>
#define pq priority_queue<ll>
#define pii pair<ll, ll>
#define vp vector<pii>
#define vvp vector<vp>
#define vd vector<ld>
#define vvd vector<vd>
#define all(a) (a).begin(), (a).end()

const int MAX_N = 2e5 + 5;
const ll MOD = 1e9 + 7;
const ll INF = 1e10;
const ld EPS = 1e-9;




struct Edge {
    int u, v, weight;
    bool operator<(Edge const& other){
        return weight < other.weight;
    }
};

int N, M;
vector<Edge> edges;
vector<int> parent;
vector<int> cnt;


void make_set(int v) {
    parent[v] = v;
    cnt[v] = 1;
}

int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}


void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (cnt[a] < cnt[b])
            swap(a, b);
        parent[b] = a;
        cnt[a] += cnt[b];
    }
}


void solve(){
    vi group(N);
    rep(q, 0, N){
        make_set(q);
    }
    
    sort(all(edges));
    
    int cost = 0;
    for (Edge edge : edges){
        if (find_set(edge.u) != find_set(edge.v)){
            cost += edge.weight;
            union_sets(edge.u, edge.v);
        }
        
    }
    cout << cost;
}


int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    cin >> N >> M;
    parent.resize(N);
    cnt.resize(N);
    
    for (int t = 0; t <M; t++) {
        Edge e;
        int a, b, w;
        cin >> a >> b >> w; //from, to, weight
        a--;
        b--;
        e.u = a;
        e.v = b;
        e.weight = w;
        edges.pb(e);
    }
    solve();
}
