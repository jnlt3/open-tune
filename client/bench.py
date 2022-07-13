import multiprocessing
import re
from subprocess import PIPE, Popen


def run_benchmarks(exe: str, threads: int) -> int:
    print(f"Benching on {threads} threads...")
    queue = multiprocessing.Queue()
    for _ in range(threads):
        proc = multiprocessing.Process(target=bench, args=(queue, exe))
        proc.start()

    nps = sum([queue.get() for _ in range(threads)])
    print(f"Average NPS per thread is {nps}")
    return nps // threads


def bench(queue: multiprocessing.Queue, exe: str) -> int:
    try:
        process = Popen([exe, "bench"], stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        queue.put(parse_bench_output(stdout))
    except Exception:
        queue.put(0)


def parse_bench_output(stream) -> int:
    nps = None
    for line in stream.decode("ascii").strip().split("\n")[::-1]:
        line = re.sub(r"[^a-zA-Z0-9 ]+", " ", line)
        nps_pattern = r"([0-9]+ NPS)|(NPS[ ]+[0-9]+)"
        re_nps = re.search(nps_pattern, line.upper())
        if not nps and re_nps:
            nps = re_nps.group()
    nps = int(re.search(r"[0-9]+", nps).group()) if nps else None
    return nps
