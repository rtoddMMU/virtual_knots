def seifert_nesting(diagram):
    components = diagram.seifert_components()
    intervals = []

    for i, circle in enumerate(components):
        all_segments = []
        for idx, ref in enumerate(circle):
            if idx % 2 != 0:          # odd = arriving, skip
                continue
            if ref not in diagram.arc_routes:
                continue
            all_segments.extend(diagram.arc_routes[ref])

        xs_on_line = []
        seen = set()

        for seg in all_segments:
            for pt in [seg.start, seg.end]:
                if pt in seen:
                    continue
                seen.add(pt)
                x, y = pt
                if y == x + 1:
                    xs_on_line.append(x)

        if len(xs_on_line) >= 2:
            intervals.append((min(xs_on_line), max(xs_on_line), i))

    intervals.sort(key=lambda iv: iv[0])
    parent = [-1] * len(intervals)
    stack = []

    for j, (left, right, _) in enumerate(intervals):
        while stack and intervals[stack[-1]][1] < left:
            stack.pop()
        if stack:
            parent[j] = stack[-1]
        stack.append(j)

    return intervals, parent