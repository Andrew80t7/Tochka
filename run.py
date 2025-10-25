from heapq import heappush, heappop
import sys

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_POS = [2, 4, 6, 8]
HALL_STOPS = [0, 1, 3, 5, 7, 9, 10]


def parse_input(lines):
    lines = [line for line in lines if line.strip()]
    hallway_line = None
    room_lines = []
    for line in lines:
        if line.startswith('#') and '.' in line and line.count('.') >= 11:
            start = line.find('#') + 1
            end = line.rfind('#')
            hallway_str = line[start:end]
            if len(hallway_str) == 11:
                hallway_line = tuple(hallway_str)
        elif any(c in 'ABCD' for c in line):
            room_lines.append(line)
    if not hallway_line:
        hallway_line = tuple(lines[1][1:12]) if len(lines) > 1 else tuple('.' * 11)
    rooms_data = []
    for line in room_lines:
        chars = []
        for pos in [3, 5, 7, 9]:
            if len(line) > pos and line[pos] in 'ABCD':
                chars.append(line[pos])
            else:
                chars.append('.')
        rooms_data.append(chars)
    if not rooms_data:
        if len(lines) >= 3:
            room_line1 = lines[2]
            room_line2 = lines[3] if len(lines) > 3 else "  #.#.#.#.#"
            rooms_data = [
                [room_line1[3] if len(room_line1) > 3 else '.',
                 room_line2[3] if len(room_line2) > 3 else '.'],
                [room_line1[5] if len(room_line1) > 5 else '.',
                 room_line2[5] if len(room_line2) > 5 else '.'],
                [room_line1[7] if len(room_line1) > 7 else '.',
                 room_line2[7] if len(room_line2) > 7 else '.'],
                [room_line1[9] if len(room_line1) > 9 else '.',
                 room_line2[9] if len(room_line2) > 9 else '.']
            ]
        else:
            rooms_data = [['.', '.'], ['.', '.'], ['.', '.'], ['.', '.']]
    depth = len(rooms_data)
    rooms = []
    for room_idx in range(4):
        room_chars = []
        for depth_idx in range(depth):
            if depth_idx < len(rooms_data) and room_idx < len(rooms_data[depth_idx]):
                room_chars.append(rooms_data[depth_idx][room_idx])
            else:
                room_chars.append('.')
        rooms.append(tuple(room_chars))
    return hallway_line, tuple(rooms)


def is_final(state):
    hall, rooms = state
    if any(c != '.' for c in hall):
        return False
    for i, room in enumerate(rooms):
        target = chr(ord('A') + i)
        if any(c != target for c in room):
            return False
    return True


def corridor_clear(hall, start, end):
    if start == end:
        return True
    step = 1 if end > start else -1
    for p in range(start + step, end, step):
        if hall[p] != '.':
            return False
    return True


def possible_moves(state):
    hall, rooms = state
    depth = len(rooms[0])
    moves = []
    for pos, obj in enumerate(hall):
        if obj == '.':
            continue
        target_room_idx = ord(obj) - ord('A')
        room = rooms[target_room_idx]
        if any(c != '.' and c != obj for c in room):
            continue
        if all(c == obj for c in room):
            continue
        room_pos = ROOM_POS[target_room_idx]
        if not corridor_clear(hall, pos, room_pos):
            continue
        target_depth = -1
        for depth_idx in range(depth - 1, -1, -1):
            if room[depth_idx] == '.':
                target_depth = depth_idx
                break
        if target_depth == -1:
            continue
        steps = abs(pos - room_pos) + (target_depth + 1)
        cost = steps * ENERGY[obj]
        new_hall = list(hall)
        new_hall[pos] = '.'
        new_rooms = [list(r) for r in rooms]
        new_rooms[target_room_idx][target_depth] = obj
        moves.append(((tuple(new_hall), tuple(tuple(r) for r in new_rooms)), cost))
    for r_idx, room in enumerate(rooms):
        top_idx = -1
        for i in range(depth):
            if room[i] != '.':
                top_idx = i
                break
        if top_idx == -1:
            continue
        obj = room[top_idx]
        room_pos = ROOM_POS[r_idx]
        target_room_idx = ord(obj) - ord('A')
        if r_idx == target_room_idx:
            all_correct = True
            for i in range(top_idx, depth):
                if room[i] != obj:
                    all_correct = False
                    break
            if all_correct:
                continue
        for pos in HALL_STOPS:
            if not corridor_clear(hall, room_pos, pos):
                continue
            if hall[pos] != '.':
                continue
            steps = (top_idx + 1) + abs(pos - room_pos)
            cost = steps * ENERGY[obj]
            new_hall = list(hall)
            new_hall[pos] = obj
            new_rooms = [list(r) for r in rooms]
            new_rooms[r_idx][top_idx] = '.'
            moves.append(((tuple(new_hall), tuple(tuple(r) for r in new_rooms)), cost))
    return moves


def solve(lines):
    try:
        start = parse_input(lines)
        heap = [(0, start)]
        best = {start: 0}
        while heap:
            cost, state = heappop(heap)
            if cost != best.get(state, float('inf')):
                continue
            if is_final(state):
                return cost
            for ns, move_cost in possible_moves(state):
                new_cost = cost + move_cost
                if new_cost < best.get(ns, float('inf')):
                    best[ns] = new_cost
                    heappush(heap, (new_cost, ns))
    except:
        pass
    return None


def main():
    lines = []
    for line in sys.stdin:
        stripped_line = line.rstrip('\n')
        if not stripped_line:
            break
        lines.append(stripped_line)

    result = solve(lines)
    print(result if result is not None else 0)


if __name__ == "__main__":
    main()
