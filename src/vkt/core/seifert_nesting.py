def seifert_nesting(diagram):
    components = diagram.seifert_components()
    intervals = []

    for i, circle in enumerate(components):
        all_segments = []
        for idx, ref in enumerate(circle):
            if idx % 2 != 0:  # odd indices are incoming, skip
                continue
            if ref not in diagram.arc_routes:
                continue
            all_segments.extend(diagram.arc_routes[ref])

        crossings = []
        seen_pts = set()

        for seg in all_segments:
            for pt in [seg.start, seg.end]:
                if pt in seen_pts:
                    continue
                seen_pts.add(pt)
                for seg in all_segments:
                    for pt in [seg.start, seg.end]:
                        x, y = pt
                        print(f"  Component {i} corner: ({x}, {y}), y - x = {y - x}")
                x, y = pt
                if y != x + 1:
                    continue

                h_other = None
                v_other = None

                for s in all_segments:
                    if s.start == s.end:
                        continue
                    is_horizontal = s.start[1] == s.end[1]
                    if is_horizontal:
                        if s.start == pt:
                            h_other = s.end
                        elif s.end == pt:
                            h_other = s.start
                    else:
                        if s.start == pt:
                            v_other = s.end
                        elif s.end == pt:
                            v_other = s.start

                if h_other is None or v_other is None:
                    continue

                h_above = h_other[1] > h_other[0] + 1
                v_above = v_other[1] > v_other[0] + 1

                if h_above != v_above:
                    crossings.append(x)
        print(f"Component {i}: {len(all_segments)} segments, crossings found: {crossings}")
        if len(crossings) == 2:
            intervals.append((min(crossings), max(crossings), i))

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