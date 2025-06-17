def appearance(intervals: dict[str, list[int]]) -> int:
    LESSON = tuple(intervals['lesson'])          # L0, L1

    def to_pairs(lst):
        """[a,b,c,d] -> [(a,b), (c,d)]"""
        return list(zip(lst[::2], lst[1::2]))

    def clip_and_merge(raw):
        """обрезаем лессоном и склеиваем пересекающиеся интервалы."""
        segs = []
        L0, L1 = LESSON
        for a, b in to_pairs(raw):
            a, b = max(a, L0), min(b, L1)
            if a < b:                       # остался кусок внутри урока
                segs.append((a, b))
        if not segs:
            return []

        segs.sort()
        merged = [segs[0]]
        for a, b in segs[1:]:
            prev_a, prev_b = merged[-1]
            if a <= prev_b:                 # перекрытие/стык
                merged[-1] = (prev_a, max(prev_b, b))
            else:
                merged.append((a, b))
        return merged

    pupil = clip_and_merge(intervals['pupil'])
    tutor = clip_and_merge(intervals['tutor'])

    # пересечение двух списков отрезков
    i = j = total = 0
    while i < len(pupil) and j < len(tutor):
        a0, a1 = pupil[i]
        b0, b1 = tutor[j]
        start = max(a0, b0)
        end   = min(a1, b1)
        if start < end:
            total += end - start
        # продвигаемся по тому отрезку, что раньше закончился
        if a1 < b1:
            i += 1
        else:
            j += 1
    return total
