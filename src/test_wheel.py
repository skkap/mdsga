import random


def construct_roulette_wheel_score_array(scores):
    s_min = min(scores)
    norm_scores = [x - s_min for x in scores]
    s_norm_max = max(norm_scores)
    inv_norm_scores = [s_norm_max - x for x in norm_scores]
    s_inv_norm_min = min([x for x in inv_norm_scores if x != 0])
    inv_norm_scores_inc = [x + s_inv_norm_min for x in inv_norm_scores]
    return inv_norm_scores_inc


def roulette_wheel_selector(scores, total):
    r = random.uniform(0, total)
    current = 0
    for i, s in enumerate(scores):
        current += s
        if current > r:
            return i


p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
scores = [18.93688419, 18.60434526, 19.05940513, 20.16958732, 17.84362292, 19.45954986,
                                 20.31292709, 20.68667404, 20.75534264, 20.24598291]

rw_scores = construct_roulette_wheel_score_array(scores)
total = sum(rw_scores)

C = 1000

for c in range(C):
    i = roulette_wheel_selector(rw_scores, total)
    p[i] += 1
p = [x / C for x in p]
print(p)

print(sum(p))