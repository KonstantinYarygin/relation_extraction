import re

from subprocess import call, Popen, PIPE

def parse_dependencies(sentence):
    with open('temp.sent', 'w') as f:
        f.write(sentence)
    cmd = './stanford_parser/lexparser_typed_only.sh temp.sent'
    # call(cmd, shell=True)
    p, e = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    p = p.decode("utf-8")
    e = e.decode("utf-8")

    e = e.split('\n')
    sent_line = [line for line in e if re.match('^Parsing\s\[sent.*\]:\s(.*)', line)][0]
    sent = re.match('Parsing \[sent.*\]:\s(.*)', sent_line).group(1)
    tokenized_sent = sent.split(' ')

    graph_raw = p.split('\n')
    graph_raw = [line for line in graph_raw if re.match('^.*\(.*\)$', line)]

    return({'graph_raw': graph_raw,
            'tokenized_sent': tokenized_sent})
