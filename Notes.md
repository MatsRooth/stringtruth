## Srun
Running llama-2-7b requires this much GPU memory, according to https://registry.premai.io/detail.html?service=llama-2-7b.
Memory requirements: 15.01 GB (14318 MiB).


To get it specify the GPU as follows.

```
srun --partition=gpu-interactive --gpus=a5000:1 --mem=16000 --pty /bin/bash
gave me ju-compute-01
```

Then source env/llama/bin/activate, and cd to /share/compling/speech/llama.

## Run the demo

torchrun --nproc_per_node 1 example_chat_completion.py --ckpt_dir llama-2-7b-chat/ --tokenizer_path tokenizer.model --max_seq_len 512 --max_batch_size 6 > example_chat_completion.out

## Sinfo
```
sinfo -a -o '|%20N | %10c | %10m | %25f | %10G|'
```
shows the gpu types.

srun --gres gpu:1 --mem=16000 --pty /bin/bash

The above gave us nikola-compute-01.

torchrun --nproc_per_node 1 example_chat_completion.py --ckpt_dir llama-2-7b-chat/ --tokenizer_path tokenizer.model --max_seq_len 512 --max_batch_size 6

It gave this error

torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 86.00 MiB. GPU 0 has a total capacty of 11.92 GiB of which 65.44 MiB is free. Including non-PyTorch memory, this process has 11.85 GiB memory in use. Of the allocated memory 11.44 GiB is allocated by PyTorch, and 1.59 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF

Try 64000 in srun. It has no effect.
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 86.00 MiB. GPU 0 has a total capacty of 11.92 GiB of which 65.44 MiB is free. Including non-PyTorch memory, this process has 11.85 GiB memory in use. Of the allocated memory 11.44 GiB is allocated by PyTorch, and 1.59 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF


https://registry.premai.io/detail.html?service=llama-2-7b
How much memory is needed for Llama 2 7B?
Memory requirements: 15.01 GB (14318 MiB).

If you are using AWS:

    Instance Type: p3.2xlarge or higher
    GPU: NVIDIA A100, NVIDIA V100


badjak                20          192050      compling,2080ti,gpu,gpu-l  gpu:2080ti 
compling-compute-02   32          515635      compling,a5000,gpu,nvlink  gpu:a5000:



sinfo -o "%20N  %10c  %10m  %25f  %10G "

You can see the options of sinfo by doing sinfo --help. In particular sinfo -o specifies the format of the output, and the options above are short for

    N = node name
    c = number of cores
    m = memory
    f = features, often it will be the architecture or type of associated gpu
    G = gres type and number, e.g. gpu:2

The %20 means 20 characters for this field. For example, for easy import to a Confluence page, you would want to separate fields with |, and so your command would be
sinfo -o “|%20N | %10c | %10m | %25f | %10G|”




====

When trying 13b
AssertionError: Loading a checkpoint for MP=2 but world size is 1
[2023-11-05 09:46:27,135] torch.distributed.elastic.multiprocessing.api: [ERROR] failed (exitcode: 1) local_rank: 0 (pid: 3867377) of binary: /home/mr249/env/llama/bin/python

Tried this
srun --partition=gpu-interactive --gpus=a5000:2 --mem=16000 --pty /bin/bash
torchrun --nproc_per_node 2 string1.py --ckpt_dir llama-2-13b-chat --tokenizer_path tokenizer.model --max_seq_len 512 --max_batch_size 6

The above gave this comment, and there was an error.
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed.

Try
export OMP_NUM_THREADS=2

==== error ====
torchrun --nproc_per_node 2 string1.py --ckpt_dir llama-2-13b-chat --tokenizer_path tokenizer.model --max_seq_len 512 --max_batch_size 6 
[2023-11-05 09:54:49,546] torch.distributed.run: [WARNING] 
[2023-11-05 09:54:49,546] torch.distributed.run: [WARNING] *****************************************
[2023-11-05 09:54:49,546] torch.distributed.run: [WARNING] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
[2023-11-05 09:54:49,546] torch.distributed.run: [WARNING] *****************************************
> initializing model parallel with size 2
> initializing ddp with size 1
> initializing pipeline with size 1
[2023-11-05 09:57:59,729] torch.distributed.elastic.multiprocessing.api: [WARNING] Sending process 3867813 closing signal SIGTERM
[2023-11-05 09:58:00,044] torch.distributed.elastic.multiprocessing.api: [ERROR] failed (exitcode: -9) local_rank: 1 (pid: 3867814) of binary: /home/mr249/env/llama/bin/python
Traceback (most recent call last):
  File "/home/mr249/env/llama/bin/torchrun", line 8, in <module>
    sys.exit(main())
  File "/home/mr249/env/llama/lib/python3.10/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 346, in wrapper
    return f(*args, **kwargs)
  File "/home/mr249/env/llama/lib/python3.10/site-packages/torch/distributed/run.py", line 806, in main
    run(args)
  File "/home/mr249/env/llama/lib/python3.10/site-packages/torch/distributed/run.py", line 797, in run
    elastic_launch(
  File "/home/mr249/env/llama/lib/python3.10/site-packages/torch/distributed/launcher/api.py", line 134, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
  File "/home/mr249/env/llama/lib/python3.10/site-packages/torch/distributed/launcher/api.py", line 264, in launch_agent
  



====

See this discussion
https://github.com/facebookresearch/llama/issues/415


@kechan I switched to the hugging face 13B and was able to run it on a single 4090 at 8bit quantization. It worked fine.
