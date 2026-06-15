import kenlm
import random
import math

model = kenlm.Model("stringtruth.binary")

vocab = [w.strip() for w in open("vocab.txt")]

def generate(max_len=30):
    sent = []
    state = kenlm.State()
    model.BeginSentenceWrite(state)

    for _ in range(max_len):
        candidates = []

        for w in vocab:
            out_state = kenlm.State()
            log10prob = model.BaseScore(state, w, out_state)

            candidates.append((w, out_state, log10prob))

        # convert log10 probs to weights
        mx = max(lp for _, _, lp in candidates)
        weights = [10 ** (lp - mx) for _, _, lp in candidates]

        i = random.choices(range(len(candidates)), weights=weights)[0]
        word, state, _ = candidates[i]

        sent.append(word)

        end_state = kenlm.State()
        if model.BaseScore(state, "</s>", end_state) > -0.5:
            break

    return " ".join(sent)

for _ in range(10):
    print(generate())
