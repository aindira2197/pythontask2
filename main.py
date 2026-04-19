import asyncio
from typing import Callable, List

class AsyncTaskBatcher:
    def __init__(self, max_batch_size: int = 10):
        self.max_batch_size = max_batch_size
        self.tasks = []

    async def add_task(self, task: Callable):
        self.tasks.append(task)
        if len(self.tasks) >= self.max_batch_size:
            await self.run_tasks()

    async def run_tasks(self):
        tasks_to_run = self.tasks[:]
        self.tasks = []
        await asyncio.gather(*[task() for task in tasks_to_run])

    async def run_remaining_tasks(self):
        if self.tasks:
            await self.run_tasks()

async def example_task(task_id: int):
    await asyncio.sleep(1)
    print(f"Task {task_id} completed")

async def main():
    batcher = AsyncTaskBatcher(max_batch_size=5)
    for i in range(20):
        await batcher.add_task(lambda task_id=i: example_task(task_id))
    await batcher.run_remaining_tasks()

asyncio.run(main())

class AsyncTaskBatcherWithQueue:
    def __init__(self, max_batch_size: int = 10):
        self.max_batch_size = max_batch_size
        self.tasks = asyncio.Queue()

    async def add_task(self, task: Callable):
        await self.tasks.put(task)
        if self.tasks.qsize() >= self.max_batch_size:
            await self.run_tasks()

    async def run_tasks(self):
        tasks_to_run = []
        for _ in range(self.max_batch_size):
            if not self.tasks.empty():
                task = await self.tasks.get()
                tasks_to_run.append(task)
        await asyncio.gather(*[task() for task in tasks_to_run])

    async def run_remaining_tasks(self):
        while not self.tasks.empty():
            tasks_to_run = []
            for _ in range(self.max_batch_size):
                if not self.tasks.empty():
                    task = await self.tasks.get()
                    tasks_to_run.append(task)
            await asyncio.gather(*[task() for task in tasks_to_run])

async def example_task_with_queue(task_id: int):
    await asyncio.sleep(1)
    print(f"Task {task_id} completed")

async def main_with_queue():
    batcher = AsyncTaskBatcherWithQueue(max_batch_size=5)
    for i in range(20):
        await batcher.add_task(lambda task_id=i: example_task_with_queue(task_id))
    await batcher.run_remaining_tasks()

asyncio.run(main_with_queue())