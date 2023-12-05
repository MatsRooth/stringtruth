# stringtruth
This is a benchmark for sentences about strings. The file `benchmark/cl23.txt` has tuples like

```
('gavi_b_7_yahoo', 'every nasal that precedes letter two is capitalized', 'yahoo', 'f')
('cyz_a_5_oeieouo', 'no vowel is capitalized and is adjacent to a vowel', 'oeieouo', 't')
('cyz_a_5_OEUE', 'no vowel is capitalized and is adjacent to a vowel', 'OEUE', 'f')
```

consisting of an ID, a sentence, a string, and the truth value of the sentence as a description of the string.
`data_clean/pooled_text` has just the sentences in a capitalized format, and shorter IDs. 

```
lyra_b_3 THERE IS A CONSONANT THAT IS FINAL AND IS CAPITALIZED
yumi_a_1 THERE ARE EXACTLY TWO VOWELS THAT PRECEDE LETTER THREE
```

`data_clean/pooled_truth` has the truth values in another format, with a sentence ID and
strings alternating with truth values.

```
apple_b_10 apple t hello t friday f think f letter t yes f well t see f
ava_a_1 aTqF f aaer t aban f sAioa t tttt u
```

There are 533 sentences, and 3477 truth value judgments, about 6.5 truth value judgments for different strings per sentence.
Authors of the sentences were students in Computational Linguistics I at Cornell in Spring 2023, and the author of the sentence also
gave the truth value judgments. The data were created in connection with a final project consisting of an end-to-end
speech to truth system.  While there are audio recordings of the 533 sentences, this repository emphasizes the textual part.

## Llama2 truth values
`strings_chat.out` has llama2 truth values for 500 items, obtained with the `llama-2-7b-chat` model. The Assistant responses
begin with True or False, usually followed by a brief justification.


```
==================================

User: Consider the string 'BANANA'. True or False: no vowel is capitalized and is adjacent to a vowel

> Assistant:  True.

In the string 'BANANA', no vowel is capitalized and is adjacent to another vowel. The vowels in the string are 'A' and 'A', which are adjacent to each other.

==================================
```

This command runs `strings_chat.py` to produce `strings_chat.out`.
```
torchrun --nproc_per_node 1 strings_chat.py --ckpt_dir llama-2-7b-chat/ --tokenizer_path tokenizer.model --benchmark_path benchmark/cl23.txt --max_seq_len 512 --max_batch_size 6
```

The following was used to launch the compute node in a Slurm environment.  

```
srun --partition=gpu-interactive --gpus=a5000:1 --mem=16000 --pty /bin/bash
```

Specifying the gpu type helped with avoiding out of memory errors.  Llama-2-7b requires this much GPU memory, according to premai.io.

```
Memory requirements: 15.01 GB (14318 MiB).
```
