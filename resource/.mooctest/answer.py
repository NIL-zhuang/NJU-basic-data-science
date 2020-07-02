#include <bits/stdc++.h>
#define inc(i, a, b) for (register int i = a; i <= b; i++)
#define dec(i, a, b) for (register int i = a; i >= b; i--)
using namespace std;
char s[1000010], t[1000010];
int n, m;
class node2 {
public:
    class node1 {
    public:
        int link, len;
        int ch[27];
    } sam[1000010];
    int last = 1, size = 1;
    long long siz[1000010];
    void add(int to) {
        int cur = ++size;
        siz[cur] = 1;
        sam[cur].len = sam[last].len + 1;
        int u = last;
        while (u && !sam[u].ch[to]) sam[u].ch[to] = cur, u = sam[u].link;
        if (!u)
            sam[cur].link = 1;
        else {
            int q = sam[u].ch[to];
            if (sam[q].len == sam[u].len + 1)
                sam[cur].link = q;
            else {
                int neww = ++size;
                sam[neww] = sam[q];
                sam[neww].len = sam[u].len + 1;
                while (u && sam[u].ch[to] == q) sam[u].ch[to] = neww, u = sam[u].link;
                sam[q].link = neww;
                sam[cur].link = neww;
            }
        }
        last = cur;
    }
} SAM1, SAM2;
long long ans = 0;
void dfs(int x, int y) {
    for (int i = 0; i <= 25; i++) {
        if (SAM1.sam[x].ch[i] && SAM2.sam[y].ch[i]) {
            dfs(SAM1.sam[x].ch[i], SAM2.sam[y].ch[i]);
        }
    }
    if (x != 1 && y != 1)
        ans += SAM1.siz[x] * SAM2.siz[y];
}
int c1[1000010], t1[1000010], c2[1000010], t2[1000010];
int main() {
    scanf("%s%s", s + 1, t + 1);
    n = strlen(s + 1), m = strlen(t + 1);
    inc(i, 1, n) SAM1.add(s[i] - 'a');
    inc(i, 1, m) SAM2.add(t[i] - 'a');
    inc(i, 1, SAM1.size) c1[SAM1.sam[i].len]++;
    inc(i, 1, n) c1[i] += c1[i - 1];
    inc(i, 1, SAM1.size) t1[c1[SAM1.sam[i].len]--] = i;
    dec(i, SAM1.size, 1) SAM1.siz[SAM1.sam[t1[i]].link] += SAM1.siz[t1[i]];
    inc(i, 1, SAM2.size) c2[SAM2.sam[i].len]++;
    inc(i, 1, m) c2[i] += c2[i - 1];
    inc(i, 1, SAM2.size) t2[c2[SAM2.sam[i].len]--] = i;
    dec(i, SAM2.size, 1) SAM2.siz[SAM2.sam[t2[i]].link] += SAM2.siz[t2[i]];
    dfs(1, 1);
    cout << ans;
}