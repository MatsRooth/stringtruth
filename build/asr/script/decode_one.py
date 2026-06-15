#!/usr/bin/env python3

import argparse
import torch
import torchaudio
import json
import os

from torchaudio.models.decoder import ctc_decoder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wav")
    parser.add_argument("--tokens", required=True)
    parser.add_argument("--lexicon", required=True)
    parser.add_argument("--lm", default=None)
    parser.add_argument(
        "--output-format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )

    
    args = parser.parse_args()

    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model()
    model.eval()

    waveform, sr = torchaudio.load(args.wav)

    if sr != 16000:
        waveform = torchaudio.functional.resample(
            waveform, sr, 16000
        )

    with torch.inference_mode():
        emissions, _ = model(waveform)

    decoder = ctc_decoder(
        lexicon=args.lexicon,
        tokens=args.tokens,
        lm=args.lm,
        nbest=10,
        beam_size=50,
        beam_threshold=50,
    )

    results = decoder(emissions.cpu())

    # Build hyps
    hyps = []
    for rank, hyp in enumerate(results[0], start=1):
        hyps.append({
            "rank": rank,
            "score": float(hyp.score),
            "words": list(hyp.words),
        })

    # Output result embedding hyps as json
    if args.output_format == "json":
        out = {
            "wav": args.wav,
            "utt_id": os.path.splitext(os.path.basename(args.wav))[0],
            "nbest": hyps,
        }
        
        print(json.dumps(out, indent=2))

    #  .. or as text
    else:
        print()
        print("Top hypotheses")
        print("==============")
        
        for hyp in hyps:
            print(
                f"{hyp['rank']:2d}  "
                f"score={hyp['score']:8.3f}  "
                + " ".join(hyp["words"])
            )

            print()
            print("Top hypotheses")
            print("==============")

            for i, hyp in enumerate(results[0]):
                words = hyp.words
                score = hyp.score
                
                print(
                    f"{i+1:2d}  score={score:8.3f}  "
                    + " ".join(words)
                )


if __name__ == "__main__":
    main()
