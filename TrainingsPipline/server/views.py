from django.shortcuts import render
import mpld3
from .models import *
from django import template
import pandas as pd
import matplotlib.pyplot as plt

# Create your views here.

def monitor(request):
    graphs = []
    server_name = []
    server = ServerManagement.objects.filter(enable=True)
    for var in server:
        result = CpuUsage.objects.filter(server_id=var)
        ls = []
        # time = pd.date_range(end = timezone.now(), periods=10, freq='10S', )
        # time = [60, 50, 40, 30, 20, 10, 0]
        time = [0, 10, 20, 30, 40, 50, 60]
        for a in result:
            ls.append(a.cpu)
        if len(ls) <= 10:
            break
        fig = plt.figure(figsize=(6.5, 2), dpi=180)
        plt.plot(time, ls[-7:], label='CPU Usage')
        plt.legend(loc=3)
        plt.xlim(60, 0)
        plt.ylim(0, 100)
        server_name.append(var)
        graphs.append(mpld3.fig_to_html(fig))
    return render(request, 'monitor_page.html', {'graph': graphs, 'server_name': server_name})

