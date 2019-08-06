<p align="center">
  <img src="https://github.com/pype-project/Pype/blob/master/docs/assets/pype_logo.png?raw=true" alt="Pype logo"/>
</p>

# Pype
## ***Python Data Pipes for Mulitprocessing Systems***

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
answer = server.pull.remote('meaning_of_life')
```

#### Remote Video Server in 5 lines of Python
```python
import pype
server = pype.Server.remote()
video_server = pype.VideoServer.remote(server, camera=0, output_queues=('frames'))
while True:
    data = ray.get(server.pull.remote('frames'))
```