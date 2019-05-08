import re
import csv
import codecs
import time
from hawkular import metrics, HawkularMetricsClient

class PerfmonCSVParser:

    def __init__(self):
        self.c = HawkularMetricsClient(tenant_id='perfmon')

    def parse_file(self, filename):        
        with codecs.open(filename, encoding='utf16') as f:
            i = 0
            for line in f:
                parsed_line = re.split('"?,\D"?', line)        
                if i == 0:        
                    self.parse_header(parsed_line)
                else:
                    self.parse_stats(parsed_line)
                i += 1

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def parse_header(self, parsed_line):
        metrics = ["timestamp"]
        i = 0
        for l in parsed_line:
            if i > 0:
                metrics.append(l)
            i += 1
        
        self.metrics = metrics

    def parse_stats(self, parsed_line):
        i = 0
        data = []
        for event in parsed_line:
            if i == 0:
                # Parse the timestamp
                # 10/20/2016 10:50:08.992
                epoch = time.mktime(time.strptime(event[1:], "%m/%d/%Y %H:%M:%S.%f"))
                ts = int(round(epoch * 1000))
            else:
                if self.is_float(event):
                    dp = metrics.create_datapoint(event, ts)
                    metric = metrics.create_metric(metrics.MetricType.Gauge, self.metrics[i], dp)
                    data.append(metric)
            i += 1
        
        self.c.put(data)

if __name__ == '__main__':
    p = PerfmonCSVParser()
    p.parse_file('perfmon.csv')
