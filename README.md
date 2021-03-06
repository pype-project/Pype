<p align="center">
  <img src="https://github.com/pype-project/Pype/blob/master/docs/assets/pype_logo.png?raw=true" alt="Pype logo"/>
</p>

# Pype
## ***Python Data Pipes for Mulitprocessing Systems***

#### ***Warning, Pype is pre-release and unpublished, there will be bugs, keep updated for the first release of Pype***

### What is Pype?
Pype is a simple-to-use framework designed for data communication between multiple Ray processes.
With Pype, developers can quickly test and create new multiprocessing systems without having to
spend much effort with making parameter servers, streaming protocols, or complicated data handling.

To put it simply, Pype is an easy way to create communication structures between Python processes.

### What can Pype be used for?
- Sending data from one process to another specific process
- Speeding up deep learning or other heavy-compute workloads
- Spliting a video stream to multiple remote worker processes
- Utilizing an entire data center on a single dataset without complicated data communication frameworks

### Coming Soon: Installation
Just pip, no messy compilers or installing from source necessary. Distributed systems can be hard enough without extra headaches.
```bash
pip install pype
```

Or if you want to develop using Pype:
```bash
git clone https://github.com/gndctrl2mjrtm/pype
cd pype
pip install -e .
```

### Pype Architecture

The basic concept behind how Pype works is a central server that can be shared among all remote worker
processes that connects to a collection of FIFO queues. These queues can be easily modifiable to include
a wide variety of communication structures such as batch pulls, stacks, and many more with the simplicity
that Python developers have to come to expect.

This system can work from anywhere from a laptop to large data centers by connecting to an existing Ray cluster
or generating a new one with interfaces for PBS/Torque and Kubernetes (coming soon).

<p align="center">
  <img src="https://github.com/pype-project/Pype/blob/master/docs/assets/pype_diagram.png?raw=true" alt="Pype logo"/>
</p>

### The Basics

#### Start Server
```python
import pype
server = pype.Server.remote()
```

#### Push
```python
server.push.remote(42, 'meaning_of_life')
```

#### Pull
```python
answer = ray.get(server.pull.remote('meaning_of_life'))
```

#### Locking Mechanisms
```python
import pype
import time
import ray


@ray.remote
def f(server):
    while True:
        pype.pull_wait(server, 'data')
        data = ray.get(server.pull.remote('data'))

ray.init()
server = pype.Server.remote()
server.add.remote('data', use_locking=True)
f.remote(server)

for i in range(20):
    pype.push_wait(server, 'data')
    server.push.remote(i, 'data')
    server.print_queue.remote('data')

time.sleep(3)
ray.shutdown()
```

#### Data Communication Chains
```python
import pype
import time
import ray


@ray.remote
def start(server, output_name):
    for i in range(100):
        pype.push_wait(server, output_name)
        server.push.remote(i, output_name)


@ray.remote
def f(server, input_name, output_name):
    while True:
        pype.pull_wait(server, input_name)
        data = ray.get(server.pull.remote(input_name))
        server.push.remote(data, output_name)

def main():
    ray.init()
    server = pype.Server.remote()
    server.add.remote('data_0', use_locking=True)
    server.add.remote('data_1', use_locking=True)
    server.add.remote('data_2', use_locking=True)
    server.add.remote('data_3', use_locking=True)
    server.add.remote('data_4', use_locking=True)
    server.add.remote('data_5', use_locking=True)
    server.add.remote('data_6', use_locking=True)

    start.remote(server, 'data_0')
    f.remote(server, 'data_0', 'data_1')
    f.remote(server, 'data_1', 'data_2')
    f.remote(server, 'data_2', 'data_3')
    f.remote(server, 'data_3', 'data_4')
    f.remote(server, 'data_4', 'data_5')
    f.remote(server, 'data_5', 'data_6')

    for i in range(100):
        pype.pull_wait(server, 'data_6')
        data = ray.get(server.pull.remote('data_6'))
        print("Received ", data)
        server.print_queue.remote('data_6')

    time.sleep(3)
    ray.shutdown()

if __name__ == "__main__":
    main()
```