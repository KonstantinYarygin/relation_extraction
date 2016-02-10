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
    is_multilpe_sent = [True if re.match('^Parsing\s\[sent\.\s2', line) else False for line in e]
    is_multilpe_sent = any(is_multilpe_sent)
    if is_multilpe_sent:
        return(None)

    sent_line = [line for line in e if re.match('^Parsing\s\[sent.*\]:\s(.*)', line)][0]
    sent = re.match('Parsing \[sent.*\]:\s(.*)', sent_line).group(1)
    tokenized_sent = sent.split(' ')

    graph_raw = p.split('\n')
    graph_raw = [line for line in graph_raw if re.match('^.*\(.*\)$', line)]
    if not graph_raw:
        return(None)

    return({'graph_raw': graph_raw,
            'tokenized_sent': tokenized_sent})