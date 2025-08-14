import asyncio
import time
 
def blocking_io():
    """Simulated blocking I/O"""
    time.sleep(2)
    return "io-done"
 
def blocking_cpu(n: int = 10_000_00):
    """Simulate CPU-intensive calculations"""
    s = 0
    for i in range(n):
        s += i * i
    return s
 
async def lightweight_task():
    """Simulate a lightweight task"""
    print("[lightweight] start")
    await asyncio.sleep(0.1)
    print("[lightweight] end")
    return "lightweight-done"
 
# ---------- 1) Pitfall: Calling a blocking function in async blocks the event loop ----------

async def bad_blocking_in_async():
    t0 = time.monotonic()
    print("[bad] start: blocking in async ...")
    # ❌ Pitfall: time.sleep blocks the entire thread => the event loop cannot schedule other tasks
    result = blocking_io()  # This will block the event loop for 2 seconds
    print(f"[bad] end: {result}, took {time.monotonic() - t0:.2f}s")
 
# ✅ Fix: Offload blocking function to thread pool (recommended asyncio.to_thread in 3.9+)
async def good_offload_blocking():
    t0 = time.monotonic()
    print("[good] start: offload blocking to thread ...")
    result = await asyncio.to_thread(blocking_io)
    print(f"[good] end: {result}, took {time.monotonic() - t0:.2f}s")
 
# ---------- 2) Pitfall: Forgetting to await a coroutine leads to unexecuted code or warnings ----------

async def coro_returns_value():
    await asyncio.sleep(0.1)
    return 42
 
async def demonstrate_forget_await():
    print("[forget-await] wrong way -> just calling the coroutine")
    c = coro_returns_value()     # Just created the coroutine object, but did not execute it
    print("  got:", c)           # <coroutine object ...>
    # If the function ends without awaiting this c, a runtime warning may occur
    # RuntimeWarning: coroutine '...' was never awaited
    print("[forget-await] right way -> await it or wrap as a Task")
    val = await coro_returns_value()
    print("  awaited value:", val)
 
# ---------- 3) Pitfall: Shared race condition（race condition） ----------

counter = 0
 
async def add_without_lock():
    """Deliberately create a race condition: insert await between read-modify-write"""
    global counter
    tmp = counter
    await asyncio.sleep(0)  # Yield control, easily interrupted by concurrency
    counter = tmp + 1
 
async def add_with_lock(lock: asyncio.Lock):
    global counter
    async with lock:        # ✅ Use async lock to protect critical section
        tmp = counter
        await asyncio.sleep(0)
        counter = tmp + 1
 
async def demonstrate_race_condition():
    global counter
    # ❌ Without lock, the counter result is usually < 1000
    counter = 0
    await asyncio.gather(*[add_without_lock() for _ in range(1000)])
    print(f"[race] without lock -> counter = {counter} (expect 1000)")
    # ✅ With lock, the result should be 1000
    counter = 0
    lock = asyncio.Lock()
    await asyncio.gather(*[add_with_lock(lock) for _ in range(1000)])
    print(f"[race] with lock    -> counter = {counter} (expect 1000)")
 
# ---------- 4) Cancelation and cleanup (timeout control) ----------

async def slow_op():
    try:
        for i in range(5):
            print(f"[cancel] working step {i}")
            await asyncio.sleep(1)
        return "done"
    except asyncio.CancelledError:
        print("[cancel] got CancelledError, cleaning up ...")
        # Do necessary cleanup (close handles/rollback etc.)
        raise
    finally:
        print("[cancel] finally cleanup called")
 
async def demonstrate_cancel_and_timeout():
    task = asyncio.create_task(slow_op())
    try:
        # ❗ Add timeout to trigger cancellation
        await asyncio.wait_for(task, timeout=2)
    except asyncio.TimeoutError:
        print("[cancel] timeout! now cancel the task ...")
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("[cancel] task is cancelled")
 
 
# ---------- 5) Pitfall: CPU intensive causing 'starvation' vs to_thread fix ----------

async def ticker(name: str, seconds: float = 3.0):
    """Be careful: if the event loop is blocked, this ticker will 'stall'"""
    t0 = time.monotonic()
    while time.monotonic() - t0 < seconds:
        print(f"[ticker-{name}] tick")
        await asyncio.sleep(0.2)
 
async def demonstrate_cpu_blocking_and_fix():
    print("[cpu] demo: ticker + CPU heavy (bad)")
    # ❌ Bad example: directly running CPU intensive task in coroutine, ticker will 'stall'
    t_bad = asyncio.create_task(ticker("bad"))
    # This blocks directly (don't do this)
    blocking_cpu(30_000_000)   # Adjust the number to feel the stutter
    await t_bad
    print("[cpu] bad demo done\n")
    # ✅ Good example: offload CPU intensive work to thread, ticker can still run every 0.2s
    print("[cpu] demo: ticker + to_thread (good)")
    t_good = asyncio.create_task(ticker("good"))
    result = await asyncio.to_thread(blocking_cpu, 30_000_000)
    await t_good
    print(f"[cpu] good demo done, cpu result={result}\n")
 
# ---------- Entry Point ----------

async def main():
    # print("\n=== 1) Pitfall: Blocking call in async vs Good: Offload ===")
    # Concurrently start a lightweight task and observe if it gets "stuck"
    # t = asyncio.create_task(lightweight_task())
    # await bad_blocking_in_async()    # Deliberately block
    # await t                          # This await will be noticeably delayed
    # await good_offload_blocking()    # Correct approach
    # await t
    # print("\n=== 2) Pitfall: Forgetting await ===")
    # await demonstrate_forget_await()
    # print("\n=== 3) Pitfall: Race condition ===")
    # await demonstrate_race_condition()
    print("\n=== 4) Pitfall: Cancelation and cleanup (timeout control) ===")
    await demonstrate_cancel_and_timeout()
    # print("\n=== 5) Pitfall: CPU intensive causing 'starvation' vs to_thread fix ===")
    # await demonstrate_cpu_blocking_and_fix()
 
if __name__ == "__main__":
   asyncio.run(main())
 