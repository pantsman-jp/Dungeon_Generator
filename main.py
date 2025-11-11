from random import choice, randrange


def make_room(x, y, w, h):
    """部屋を表すタプル (x, y, w, h) を作成する"""
    return (x, y, w, h)


def room_center(room):
    """部屋の中心座標 (x, y) を返す"""
    x, y, w, h = room
    return (x + w // 2, y + h // 2)


def is_intersect(a, b):
    """部屋 a と部屋 b が重なっているか判定する"""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (
        (ax + aw <= bx) or (bx + bw <= ax) or (ay + ah <= by) or (by + bh <= ay)
    )


def carve_room(m, room):
    """マップ m に部屋 room を掘る（床を '.' に置換）"""
    x, y, w, h = room
    return [
        [
            ("." if ((x <= ix < x + w) and (y <= iy < y + h)) else m[iy][ix])
            for ix in range(len(m[0]))
        ]
        for iy in range(len(m))
    ]


def carve_tunnel(m, x1, y1, x2, y2):
    """座標 (x1, y1) から (x2, y2) までのL字型通路を掘る"""
    m = [row[:] for row in m]
    if choice([True, False]):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            m[y1][x] = "."
        for y in range(min(y1, y2), max(y1, y2) + 1):
            m[y][x2] = "."
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            m[y][x1] = "."
        for x in range(min(x1, x2), max(x1, x2) + 1):
            m[y2][x] = "."
    return m


def place_rooms(width, height, max_rooms=30, room_min=5, room_max=12, max_tries=1000):
    """マップを初期化し、部屋をランダムに配置し、通路で接続する"""
    m = [["#" for _ in range(width)] for _ in range(height)]
    rooms = []
    tries = 0
    while (len(rooms) < max_rooms) and (tries < max_tries):
        w, h = randrange(room_min, room_max + 1), randrange(room_min, room_max + 1)
        x, y = randrange(1, width - w - 1), randrange(1, height - h - 1)
        new_room = make_room(x, y, w, h)
        if all(not is_intersect(new_room, other) for other in rooms):
            m = carve_room(m, new_room)
            if rooms:
                prev_cx, prev_cy = room_center(rooms[-1])
                new_cx, new_cy = room_center(new_room)
                m = carve_tunnel(m, prev_cx, prev_cy, new_cx, new_cy)
            rooms.append(new_room)
        tries += 1
    return m


def generate_dungeon(width=80, height=45, **kwargs):
    """ダンジョンを生成してマップを返す"""
    return place_rooms(width, height, **kwargs)


def ascii_map(m):
    """マップ m を文字列に変換して返す"""
    return "\n".join("".join(row) for row in m)


if __name__ == "__main__":
    dungeon = generate_dungeon(80, 45, max_rooms=20, room_min=4, room_max=10)
    print(ascii_map(dungeon))
