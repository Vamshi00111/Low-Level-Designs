"""
Question To Ask:
Purpose of the system?
Multiple Jobs ?
Job Types ?
Job Priority ?
Job Duration ?
Job Deadline ?
Job Dependencies ?
Job Resources ?

Assumptions:
Cluster Configuration -  Each cluster has fixed CPU and memory capacities.
Job Submission - Jobs specify required CPU, memory, execution time, and priority.
Concurrency - Multiple jobs can execute on a cluster if resources suffice.
Job Scheduling - Jobs are assigned to the first available cluster satisfying resource requirements.
Priority Handling - Higher priority jobs preempt lower-priority jobs waiting in the queue.
Thread Safety - All resource allocations and deallocations are thread-safe.

LLD:

Job
 ├── defines job requirements
 └── supports priority-based comparison

Cluster
 ├── tracks available CPU/RAM
 └── executes jobs concurrently

ClusterManager
├── manages available clusters
├── checks resource availability
└── allocates/deallocates resources

JobScheduler
 ├── submits jobs to Priority Queue
 ├── retrieves jobs for execution
 └── dispatches jobs to ClusterManager


Pre-Requisites:
Process
- A process is an instance of a program that is being executed
Thread
- A thread is a lightweight process that is a subset of a process
Concurrency
-  Concurrency is the ability of different parts or units of a program, algorithm, or problem to be executed
Race Condition
- race condition is a situation in which two or more threads or processes are reading or writing shared data
- and the final result depends on the timing of how the threads are scheduled
- We can prevent race conditions by using locks or other synchronization mechanisms
Lock
- A lock is a synchronization primitive that is used to manage access to shared resources
- A lock is used to prevent multiple threads from accessing shared resources simultaneously

"""



# Solution:

import time
from threading import Lock

class Job:
    def __init__(self, job_id, cpu_req, ram_req, exec_time, priority):
        self.job_id = job_id
        self.cpu_req = cpu_req
        self.ram_req = ram_req
        self.exec_time = exec_time
        self.priority = priority  # Higher priority has precedence
    
    def __lt__(self, other):
        return self.priority > other.priority  # Priority Queue: Higher priority first

class Cluster:
    def __init__(self, cluster_id, total_cpu, total_ram):
        self.cluster_id = cluster_id
        self.total_cpu = total_cpu
        self.total_ram = total_ram
        self.available_cpu = total_cpu
        self.available_ram = total_ram
        self.lock = Lock()

    def allocate_resources(self, cpu_req, ram_req):
        with self.lock: # Lock to ensure thread safety - Only one thread can access the resource at a time
            # No other thread can access available_cpu until the current thread releases the lock
            if self.available_cpu >= cpu_req and self.available_ram >= ram_req:
                self.available_cpu -= cpu_req
                self.available_ram -= ram_req
                return True
        return False

    def release_resources(self, cpu_req, ram_req):
        with self.lock:
            self.available_cpu += cpu_req
            self.available_ram += ram_req

class ClusterManager:
    def __init__(self):
        self.clusters = []

    def add_cluster(self, cluster):
        self.clusters.append(cluster)

    def find_available_cluster(self, cpu_req, ram_req):
        for cluster in self.clusters:
            if cluster.allocate_resources(cpu_req, ram_req):
                return cluster
        return None


import heapq
import threading

class JobScheduler:
    def __init__(self, cluster_manager):
        self.cluster_manager = cluster_manager
        self.job_queue = []
        self.lock = Lock()

    def submit_job(self, job):
        with self.lock:
            heapq.heappush(self.job_queue, job)

    def schedule_jobs(self):
        while self.job_queue:
            with self.lock:
                job = heapq.heappop(self.job_queue)
            cluster = self.cluster_manager.find_available_cluster(job.cpu_req, job.ram_req)
            if cluster:
                threading.Thread(target=self.execute_job, args=(cluster, job)).start()
            else:
                print(f"No available cluster for job {job.job_id}. Retrying...")
                with self.lock:
                    heapq.heappush(self.job_queue, job)  # Requeue the job

    def execute_job(self, cluster, job):
        print(f"Job {job.job_id} started on Cluster {cluster.cluster_id}")
        time.sleep(job.exec_time)  # Simulate job execution
        print(f"Job {job.job_id} completed on Cluster {cluster.cluster_id}")
        cluster.release_resources(job.cpu_req, job.ram_req)


if __name__ == "__main__":
    cluster_manager = ClusterManager()
    cluster_manager.add_cluster(Cluster("A", 8, 32))
    cluster_manager.add_cluster(Cluster("B", 16, 64))

    # Job()
    jobs = [
        Job("1", 4, 16, 5, 1),
        Job("2", 2, 8, 3, 2),
        Job("3", 16, 64, 7, 1),
    ]

    scheduler = JobScheduler(cluster_manager)
    for job in jobs:
        scheduler.submit_job(job)

    scheduler.schedule_jobs()