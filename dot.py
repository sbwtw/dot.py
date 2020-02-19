#!/usr/bin/python3

#
#   Author:     sbw <sbw@sbw.so>
#   License:    MIT
#

import os
import csv
import enum
import argparse

TEST = False
ENVS = { 
    'HOME' : os.getenv('HOME'),
}

class Operation(enum.Enum):
    Deploy = 'deploy'
    Collect = 'collect'
    Push = 'push'
    Pop = 'pop'

    def __str__(self):
        return self.value

def link(src, dst):
    cmd = 'ln -sf {} {}'.format(src, dst)
    if TEST:
        os.system('echo {}'.format(cmd))
    else:
        print(cmd, os.system(cmd))

def copy(src, dst):
    if os.path.islink(src):
        print('WARN: {} is a link'.format(src))
        return False

    cmd = 'cp -f {} {}'.format(src, dst)
    if TEST:
        os.system('echo {}'.format(cmd))
    else:
        print(cmd, os.system(cmd))
    return True

def deploy(backup, real, symbolic):
    backup = os.path.abspath(backup)
    if symbolic == True:
        link(backup, real)
    else:
        copy(backup, real)

def collect(backup, real):
    backup = os.path.abspath(backup)
    copy(real, backup)

def main(conf, operation):
    with open(conf, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            backup = row[0]
            real = row[1]
            symbolic = row[2] == 'True'

            if operation == Operation.Deploy:
                deploy(backup, real, symbolic)
            if operation == Operation.Collect and symbolic == False:
                collect(backup, real)

def env_path(path):
    for env, val in ENVS.items():
        if val and path.startswith(val):
            return '${}{}'.format(env, path[len(val):])
    return path

def pop(conf, file):
    list = []
    found = False
    with open(conf, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != file:
                list.append(row)
            else:
                found = True
                break

    if not found:
        print('WARN: {} not found'.format(file))
        return

    if TEST:
        print(list)
        return

    with open(conf, 'w+') as f:
        writer = csv.writer(f)
        for row in list:
            writer.writerow(row)

def push(conf, file, rename, symbol):
    if not rename:
        rename = os.path.basename(file.name)

    if not symbol and os.path.islink(file.name):
        print('WARN: save {} as symbol'.format(rename))
        symbol = True

    list = []
    try:
        with open(conf, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == rename:
                    print('WARN: {} already collected from {} !'.format(rename, row[1]))
                    return
                list.append(row)
    except FileNotFoundError:
        pass

    path = env_path(file.name)
    print('Collect', path, 'as', rename, ', symbol link:', symbol)
    list.append([rename, path, symbol])

    if collect(rename, file.name) and symbol:
        deploy(rename, file.name, True)

    if TEST:
        print(list)
        return

    with open(conf, 'w+') as f:
        writer = csv.writer(f)
        for row in list:
            writer.writerow(row)

argparser = argparse.ArgumentParser()
subparsers = argparser.add_subparsers(dest='command')
pushparser = subparsers.add_parser('push')
pushparser.add_argument('file', type=argparse.FileType('r'))
pushparser.add_argument('--name', type=str)
pushparser.add_argument('--symbol', action='store_true')

popparser = subparsers.add_parser('pop')
popparser.add_argument('name', type=str)

deployparser = subparsers.add_parser('deploy');
collectparser = subparsers.add_parser('collect');

argparser.add_argument('-t', help='print command but not really do this', action='store_true');

args = argparser.parse_args()
TEST = args.t

if args.command == 'deploy':
    main('dot.conf', Operation.Deploy)
elif args.command == 'collect':
    main('dot.conf', Operation.Collect)
elif args.command == 'push':
    push('dot.conf', args.file, args.name, args.symbol)
elif args.command == 'pop':
    pop('dot.conf', args.name)
