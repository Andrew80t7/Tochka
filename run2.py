import sys
from collections import deque
from functools import lru_cache


def parse_input(lines):
    edges = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        a, sep, b = s.partition('-')
        if sep:
            edges.append((a, b))
    return edges


def make_adj(canon_edges):
    adj = {}
    for u, v in canon_edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    return adj


def bfs(start, adj):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for w in adj.get(u, ()):
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist


def find_target_gateway(adj, virus):
    dist = bfs(virus, adj)
    best = None
    best_dist = None
    for node, dist in dist.items():
        if node.isupper():
            if best is None or dist < best_dist or (dist == best_dist and node < best):
                best = node
                best_dist = dist
    return best, best_dist


def next_virus_node(adj, virus):
    tgt, td = find_target_gateway(adj, virus)
    if tgt is None:
        return None
    dist_from_tgt = bfs(tgt, adj)
    if virus not in dist_from_tgt:
        return None
    curd = dist_from_tgt[virus]
    if curd == 0:
        return tgt
    if curd == 1:
        return tgt
    neigh = sorted(adj.get(virus, []))
    candidates = [n for n in neigh if dist_from_tgt.get(n, 10 ** 9) == curd - 1]
    if not candidates:
        return None
    return candidates[0]


def canonical_edges_from_input(edges):
    return frozenset(tuple(sorted((u, v))) for (u, v) in edges)


def format_cut(g, n):
    return f"{g}-{n}"


def solve(lines):
    edges = parse_input(lines)
    canon_start = canonical_edges_from_input(edges)
    start_virus = 'a'

    @lru_cache(maxsize=None)
    def dfs(canon_edges_frozen, virus):
        canon_edges = set(canon_edges_frozen)
        adj = make_adj(canon_edges)
        tgt, _ = find_target_gateway(adj, virus)
        if tgt is None:
            return []
        cuts = []
        for u, v in sorted(canon_edges):
            if u.isupper() and not v.isupper():
                cuts.append((u, v))
            elif v.isupper() and not u.isupper():
                cuts.append((v, u))
        cuts.sort()

        for g, n in cuts:
            pair = tuple(sorted((g, n)))
            if pair not in canon_edges:
                continue
            new_canon = set(canon_edges)
            new_canon.remove(pair)
            new_adj = make_adj(new_canon)
            new_tgt, _ = find_target_gateway(new_adj, virus)
            if new_tgt is None:
                return [format_cut(g, n)]
            nxt = next_virus_node(new_adj, virus)
            if nxt is None:
                return [format_cut(g, n)]
            if nxt.isupper():
                continue
            sub = dfs(frozenset(new_canon), nxt)
            if sub is not None:
                return [format_cut(g, n)] + sub
        return None

    res = dfs(canon_start, start_virus)
    if res is None:
        return []
    return res


def main():
    lines = []
    for line in sys.stdin:
        s = line.rstrip('\n')
        if not s:
            break
        lines.append(s)
    ans = solve(lines)

    for e in ans:
        print(e)


if __name__ == "__main__":
    main()
