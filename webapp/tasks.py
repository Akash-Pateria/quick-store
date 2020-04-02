from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.decorators import task
from .models import Counter
from .models import AffinityGroupView
from .models import Filetuple
from django.db.models import Min
from .serializers import AffinityGroupViewSerializer
import requests
import yaml
import time
from math import log2
import json

with open('webapp/gossip.yaml', 'r') as file:
    configs = yaml.load(file, Loader=yaml.FullLoader)

my_ip = requests.get('https://api.ipify.org').text


def node_with_min_rtt(visited):
    nodes = AffinityGroupView.objects.order_by('rtt')
    for node in nodes:
        if node.IP not in visited and node.IP != my_ip:
            return node
    return None

def update_heartbeat():
    my_mem_list = AffinityGroupView.objects.get(IP=my_ip)
    my_mem_list.heartbeatCount = Counter.objects.get(name='heartbeat').count
    my_mem_list.timestamp = Counter.objects.get(name='heartbeat').count
    my_mem_list.save()
    my_filetuples = Filetuple.objects.filter(IP=my_ip)
    for filetuple in my_filetuples:
        filetuple.heartbeatCount = Counter.objects.get(name='heartbeat').count
        filetuple.timestamp = Counter.objects.get(name='heartbeat').count
        filetuple.save()


@periodic_task(run_every=configs['GOSSIP_PERIOD'], name="disseminate_heartbeat", ignore_result=True)
def disseminate_heartbeat(TTL=log2(AffinityGroupView.objects.all().count()), data={}):
    if int(TTL) > 0:
        fan_out = configs['FAN_OUT']
        visited = []
        payload = {}
        # import pdb; pdb.set_trace()
        update_heartbeat()
        payload = data               
        payload['TTL'] = TTL
        if 'nodes' not in payload or not payload['nodes']:
            payload['nodes'] = [entry for entry in AffinityGroupView.objects.all().values()]
        if 'filetuples' not in payload or not payload['filetuples']:
            payload['filetuples'] = [entry for entry in Filetuple.objects.all().values()]
        _iter = 0
        while _iter < fan_out:
            node = node_with_min_rtt(visited)
            if node == None:
                break            
            t1 = time.time()
            try:
                res = requests.post('http://' + node.IP + ':' + node.port + '/heartbeat', json.dumps(payload))
            # TODO: catch requests.exceptions.OSError,Timeout,ConnectionError
            except Exception as e:
                print(e)
                visited.append(node.IP)
                continue               
            t2 = time.time()
            node.rtt = max(node.rtt, t2 - t1)
            node.save()
            visited.append(node.IP)
            _iter = _iter + 1
        

""" @periodic_task(run_every=configs['GOSSIP_PERIOD'], name="detect_failure", ignore_result=True)
def detect_failure():
    pass """


@periodic_task(run_every=1.0, name="increment_heartbeat", ignore_result=True)
def increment_heartbeat():
    counter = Counter.objects.select_for_update().get_or_create(name='heartbeat')[0]
    counter.count += 1
    counter.save()
