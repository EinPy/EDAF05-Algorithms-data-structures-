#include <bits/stdc++.h>
#include <iomanip>
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


const ld INF = 1e10;
const ld EPS = 1e-9;


bool allInt = true;

int D, N;
ld cross(ld x0, ld y0, ld x1, ld y1){
    return x0 * y1 - y0 *x1;
}
ld len(ld x, ld y){
    return sqrt(x*x + y*y);
}



struct Point {
    ld x, y;
    bool operator<(Point const& other){
        ld w = cross(x, y, other.x, other.y);
        if (w > 0){
            return false;
        }else if (w < 0){
            return true;
        }else if (len(x,y) > len(other.x,other.y)){
            return false;
        }else{
            return true;
        }
    }
    Point operator-(Point const& other){
        Point ret = {x - other.x, y - other.y};
        return ret;
    }
};


void test(vector<Point> points){
    for(auto x: points){
        cout << x.x << " "  << x.y << endl;
    }

}



void solve(vector<Point> points){
    //find bottom point in leftmost corner
    ld minY, minX;
    minY = INF;
    minX = INF; 
    int idx;
    Point p0;
    rep(i, 0, N){
        if (points[i].y < minY ||( points[i].x < minX && points[i].y == minY)){
            p0 = points[i];
            idx = i;
            minY = p0.y;
            minX = p0.x;            
        }
    }
    points[idx] = points[0];
    points[0]=p0;

    rep(i, 0, N){ //Normalize
        points[i].x -= p0.x;
        points[i].y -= p0.y;
    }
    sort(points.begin()+1, points.end());

    vector<Point> CH; //ConvexHull
    //Add first 3 points
    CH.pb(points[0]);
    CH.pb(points[1]);
    CH.pb(points[2]);
    int q = 3;
    points.pb(points[0]);

    //Check colinearity
    if(abs(points[1].x*points[2].y - points[1].y*points[2].x) < EPS){
        CH[1]=points[2];
        CH[2]=points[1];
    }

    //cout << endl << endl; test(CH); cout << "Efter byte" << endl;

    while(q  < N+1){
        //cout << q << endl; test(CH); cout << endl;
        Point p = points[q];
        ld v1x = points[q].x - CH[CH.size()-1].x;
        ld v1y = points[q].y - CH[CH.size()-1].y;
        ld v2x = CH[CH.size()-2].x - CH[CH.size()-1].x;
        ld v2y = CH[CH.size()-2].y - CH[CH.size()-1].y;
        if (cross(v1x, v1y, v2x, v2y) >= 0){
            CH.erase(CH.end()-1);
        }else{
            q++;
            CH.pb(p);
            //cout << "p" << p.x << " " << p.y << endl;
        } 
    }
    CH.erase(CH.end()-1); //Remove the first element which was added at the end to fix edge case
    //preparata hong order
    ld maxX, maxY;
    maxY = -INF;
    maxX = -INF; 
    rep(i, 0, CH.size()){
        if (CH[i].x > maxX || (CH[i].x == maxX && CH[i].y > maxY)){
            idx = i;
            maxX = CH[i].x;
            maxY = CH[i].y;            
        }
    }
    //rotate(CH.begin(), CH.begin()+idx, CH.end()); # caused errors
    //got non available number
    vector<Point> out;
    for (int i = idx; i < CH.size(); i++){
        out.pb(CH[i]);
    }
    for(int i = 0; i < idx; i++){
        out.pb(CH[i]);
    }


    //cout << endl;
    //test(CH);
    cout << CH.size() << endl;
    if (!allInt){
        cout << setprecision(3) << fixed;
        rep(q, 0, out.size()){ //Antinormalize and output
            Point point = out[q];
            cout << point.x+p0.x << " " << point.y+p0.y << endl;
        }

    }else{
        cout << setprecision(0) << fixed;
        rep(q, 0, out.size()){ //Antinormalize and output
            Point point = out[q];
            cout << point.x+p0.x << " " << point.y+p0.y << endl;
        }
    }
}


int main(){
    
    cin >> D >> N;
    ld x;
    ld y;
    string hashtag;

    vector<Point> points(N);
    rep(i, 0, N){
        string xHex, yHex;
        cin >> xHex;
        cin >> yHex; 
        cin >> hashtag;
        cin >> x;
        cin >> y;
        if (x != round(x) || y != round(y)){
            allInt = false;
        }

        Point point = {x, y};
        points[i]=point;
    }

    solve(points);
    return 0;
}
