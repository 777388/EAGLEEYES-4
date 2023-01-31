import subprocess
import requests
import multiprocessing
import time
import sys
print("python3 eagleeyes4.0.py domain") 
def traceroute(root_server):
    subprocess.call(["traceroute", root_server])

def get_wayback_urls(roots_server):
    response = requests.get(f'http://web.archive.org/cdx/search/cdx?url={roots_server}/*&output=json&fl=original&collapse=urlkey')
    urls = [url for url in response.json()]
    return urls

def compare_responses(responses):
    unique_urls = set(responses[0])
    for url_list in responses[1:]:
        unique_urls.intersection_update(url_list)
    for url_list in responses:
        difference = set(url_list) - unique_urls
        print(f"URLs not found in every response: {difference}")

def worker1(mem):
    while True:
        mem.put('string1')

def worker2(mem):
    while True:
    mem.put('string2')

def root_server_process(root_server, mem):
    traceroute(root_server)
    urls = get_wayback_urls(sys.argv[1])
    mem.put(urls)

if name == 'main':
    mem = multiprocessing.Manager().Queue()
    process1 = multiprocessing.Process(target=worker1, args=(mem,))
    process2 = multiprocessing.Process(target=worker2, args=(mem,))
    process1.start()
    process2.start()
    root_servers = ['a.root-servers.net', 'b.root-servers.net', 'c.root-servers.net', 'd.root-servers.net', 'e.root-servers.net', 'f.root-servers.net', 'g.root-servers.net', 'h.root-servers.net', 'i.root-servers.net', 'j.root-servers.net', 'k.root-servers.net', 'l.root-servers.net', 'm.root-servers.net']
    processes = [multiprocessing.Process(target=root_server_process, args=(root_server, mem)) for root_server in root_servers]
    for process in processes:
        process.start()
    responses = []
    while len(responses) < len(root_servers):
        response = mem.get()
        responses.append(response)
    compare_responses(responses)
    process1.join()
    process2.join()
    for process in processes:
        process.join()
