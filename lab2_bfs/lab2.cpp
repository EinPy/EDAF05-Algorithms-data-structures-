#include <vector>
#include <algorithm>
#include <string>
#include <sstream>
#include <math.h>
#include <iostream>
#include <queue>
#include <stack>
#include <map>

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

bool checkpath(string s1, string s2){ //Kolla om kant från s1 till s2.
    //for safety
    string ss1 = s1.copy();
    string ss2 = s2.copy();
    for (int i = 1; i < 5; i++){
        size_t  plats = s2.find_first_of(s1.substr(i, 1));
        if (plats == string::npos){
            return false;
        }
        else{
            s2.erase(plats, 1);
        }
        return true;
    }
    return false;
}

vii graph; //Global

int BFS(int orig, int dest, int len){
    if (orig == dest){
        return 0;
    }
    vector<int> q;
    int dist[len];
    q.pb(orig);
    for (int i = 0; i < len; i ++){
        dist[i] = -1;
    }
    dist[orig] = 0;
    while (q.size() != 0){
        vector<int> q2;
        for (auto u : q){
            for (auto node : graph[u]){
                if (dist[node] == -1){
                    dist[node] = dist[u] + 1;
                    q2.push_back(node);
                    if (node == dest){
                        return dist[node];
                    }
                }
            }
        }
        q = q2;
    }

    return -1;
}



int main (){
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    
    int N, M; // Number of words and queries
    cin >> N, M;
    vector<string> words;
    map<string, int> ind; //Kanske användbart
    string word;
    rep(q, 0, N){
        cin >> word;
        words.pb(word);
        ind.insert({word, q});
    }

    cout << words[2];

    //Skapa graf
    rep(q, 0, N){
        vi emptyvec;
        graph.pb(emptyvec);
        rep(p, 0, N){
            if (q != p){
                if (checkpath(words[q], words[p])){
                    graph[q].pb(p);
                } 
            }
        }
    }

    //cout << graph[0][0]; Testa detta.


    //Ta in queries, sök, och skicka ut svar
    string w1, w2;
    rep(q, 0, M){
        cin >> w1, w2;
        int dist = BFS(ind.find(w1) -> second, ind.find(w2) -> second, 0);
        if (dist == -1){
            cout << "Impossible" << endl; //Om omöjligt
        }
        else{
            cout << dist << endl;
        }
    }
}
