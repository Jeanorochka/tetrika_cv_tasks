def appearance(intervals: dict[str, list[int]]) -> int:
    LESSON = tuple(intervals['lesson'])  # L0, L1

    def to_pairs(lst):
        return list(zip(lst[::2], lst[1::2]))

    def clip_and_merge(raw):
        segs = []
        L0, L1 = LESSON
        for a, b in to_pairs(raw):
            a, b = max(a, L0), min(b, L1)
            if a < b:
                segs.append((a, b))
        if not segs:
            return []

        segs.sort()
        merged = [segs[0]]
        for a, b in segs[1:]:
            prev_a, prev_b = merged[-1]
            if a <= prev_b:
                merged[-1] = (prev_a, max(prev_b, b))
            else:
                merged.append((a, b))
        return merged

    pupil = clip_and_merge(intervals['pupil'])
    tutor = clip_and_merge(intervals['tutor'])

    i = j = total = 0
    while i < len(pupil) and j < len(tutor):
        a0, a1 = pupil[i]
        b0, b1 = tutor[j]
        start = max(a0, b0)
        end = min(a1, b1)
        if start < end:
            total += end - start
        if a1 < b1:
            i += 1
        else:
            j += 1
    return total

if __name__ == '__main__':
    tests = [
        {
            'intervals': {
                'lesson': [1594663200, 1594666800],
                'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                'tutor': [1594663290, 1594663430, 1594663443, 1594666473],
            },
            'expected': 3117
        },
        {
            'intervals': {
                'lesson': [100, 200],
                'pupil': [],
                'tutor': [],
            },
            'expected': 0
        },
        {
            'intervals': {
                'lesson': [100, 200],
                'pupil': [90, 150],
                'tutor': [140, 210],
            },
            'expected': 10
        },
        {
            'intervals': {
                'lesson': [100, 200],
                'pupil': [90, 210],
                'tutor': [80, 250],
            },
            'expected': 100
        },
        {
            'intervals': {
                'lesson': [100, 200],
                'pupil': [100, 150],
                'tutor': [150, 200],
            },
            'expected': 0
        },
    ]

    for i, test in enumerate(tests):
        result = appearance(test['intervals'])
        assert result == test['expected'], f'Test {i+1} failed: got {result}, expected {test["expected"]}'
    print('тесты прошли успешно')