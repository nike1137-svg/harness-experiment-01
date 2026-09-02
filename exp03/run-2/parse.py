import re

LOG_PATTERN = re.compile(
    r'^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'
    r'\s+(?P<level>\w+)\s+\[(?P<module>\w+)\]\s+(?P<msg>.*)$'
)


def parse_errors(path):
    errors = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            m = LOG_PATTERN.match(line)
            if not m:
                continue
            if m.group('level') != 'ERROR':
                continue
            errors.append((m.group('ts'), m.group('module'), m.group('msg')))
    return errors


def print_table(errors):
    headers = ('TIMESTAMP', 'MODULE', 'MESSAGE')
    ts_w = max(len(headers[0]), max((len(e[0]) for e in errors), default=0))
    mod_w = max(len(headers[1]), max((len(e[1]) for e in errors), default=0))
    msg_w = max(len(headers[2]), max((len(e[2]) for e in errors), default=0))

    row_fmt = f'{{:<{ts_w}}}  {{:<{mod_w}}}  {{:<{msg_w}}}'
    print(row_fmt.format(*headers))
    print('-' * (ts_w + mod_w + msg_w + 4))
    for ts, module, msg in errors:
        print(row_fmt.format(ts, module, msg))
    print(f'\n총 {len(errors)}건')


if __name__ == '__main__':
    errors = parse_errors('sample.log')
    print_table(errors)
