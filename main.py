import asyncio
import time

class AsyncTaskBatchingSystem:
    def __init__(self, batch_size=10):
        self.batch_size = batch_size
        self.tasks = []
        self.lock = asyncio.Lock()

    async def add_task(self, task):
        async with self.lock:
            self.tasks.append(task)
            if len(self.tasks) >= self.batch_size:
                await self.process_tasks()

    async def process_tasks(self):
        async with self.lock:
            tasks_to_process = self.tasks[:self.batch_size]
            self.tasks = self.tasks[self.batch_size:]
            await asyncio.gather(*tasks_to_process)

    async def task1(self):
        await asyncio.sleep(1)
        print("Task 1 completed")

    async def task2(self):
        await asyncio.sleep(2)
        print("Task 2 completed")

    async def task3(self):
        await asyncio.sleep(3)
        print("Task 3 completed")

async def main():
    batching_system = AsyncTaskBatchingSystem(batch_size=5)
    tasks = [batching_system.task1, batching_system.task2, batching_system.task3]
    for task in tasks * 10:
        await batching_system.add_task(task())
    await asyncio.sleep(10)

asyncio.run(main())