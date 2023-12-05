# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional

import fire

from llama import Llama, Dialog

import sys
from ast import literal_eval


def tuple2dialog(x):
    systemprompt = {"role": "system", "content": "Always answer with a single word 'True' or 'False'"}
    userprompt = {"role": "user", "content": f"Consider the string '{x[2]}'. True or False: {x[1]}"}
    return [userprompt]

# The system prompt is not needed, the llama assistant already starts with True/False and
# includes an explanation of suitable scope.
# return [systemprompt,userprompt]

def main(
    ckpt_dir: str,
    tokenizer_path: str,
    benchmark_path: str,        
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,

):
    """
    Entry point of the program for generating text using a pretrained model.

    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        benchmark_path (str): The path to the benchmark e.g. benchmark/cl23.txt.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
    """

    # Need to work out how to add this to the arguments
    # benchmark_file = '/share/compling/speech/llama/benchmark/cl23.txt'
    
    # This is iterable
    benchmark_stream =  map(lambda z:literal_eval(z), open(benchmark_path))

    # Bunch into groups of five
    benchmark_by_5 = zip(*(benchmark_stream,) * 5)


    
    # Generator for lists of five dialogs, with 100 elements covering 500 items
    def gen_dialogs():
        for x in zip(range(100),benchmark_by_5):
            dialog = map(tuple2dialog,x[1])
            yield list(dialog)    


    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    for dialogs in gen_dialogs():
        results = generator.chat_completion(
            dialogs,  # type: ignore
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        for dialog, result in zip(dialogs, results):
            for msg in dialog:
                print(f"{msg['role'].capitalize()}: {msg['content']}\n")
                print(
                    f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
                )
                print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)
