#!/usr/bin/python
import click
import time
import redis
import random
import socket
from multiprocessing import Pool
RECORD_KEY = 'SPEED_DATA:'

def sendRedisRequest(param):
    hostname = socket.gethostname()
    fail = 0
    firstRound = True
    hsetKeyForRecord = '{}{}.{}'.format(RECORD_KEY, hostname, param['start'])
    while True:
        startTime = time.time()
        r = None
        r = redis.Redis(host=param['site'], port=param['port'], decode_responses=True)
        for i in range(param['count']):
            index = str(i+param['start'])
            if param['cliType'] == 'hset':
                r.hset("OPENAPI.TOKEN:" + index, "key", index)
            elif param['cliType'] == 'hget':
                res = r.hget("OPENAPI.TOKEN:" + index, 'key')
                if res != index:
                    fail += 1
            elif param['cliType'] == 'hgetall':
                r.hgetall("OPENAPI.TOKEN:" + index)
            elif param['cliType'] == 'hdel':
                r.hdel("OPENAPI.TOKEN:" + index, "key")
            elif param['cliType'] == 'stress':
                strRandom = str(random.random())
                r.hset("OPENAPI.TOKEN:" + index, "key", strRandom)
                res = r.hget("OPENAPI.TOKEN:" + index, "key")
                if res != strRandom:
                    print('Set:{} Get:{}'.format(strRandom, res))
                    print("OPENAPI.TOKEN:{} didn't write correctly".format(index))
                    fail += 1

        
        endTime = time.time()

        spendTime = endTime-startTime
        if firstRound:
            firstRound = False
            r.hset(hsetKeyForRecord, 'count', param['count'])
            r.hset(hsetKeyForRecord, 'loop', 1)
            r.hset(hsetKeyForRecord, 'secs', spendTime)
            r.hset(hsetKeyForRecord, 'fail', fail)
        else:
            r.hincrby(hsetKeyForRecord, 'loop', 1)
            r.hincrby(hsetKeyForRecord, 'fail', fail)
            r.hincrbyfloat(hsetKeyForRecord, 'secs', spendTime)

        remainTime = param['time_period'] - spendTime
        if param['cliType'] == 'stress':
            print('startIdx {}  spend {} seconds send {} pair of hset/hget cmd, Has {} fail of hset.'.format(param['start'], spendTime, param['count'], fail))
        elif param['cliType'] == 'hget':
            print('startIdx {}  spend {} seconds send {} of hget cmd, Has {} fail of hset.'.format(param['start'], spendTime, param['count'], fail))
        else:
            print('startIdx {}  spend {} seconds send {} of {} cmd.'.format(param['start'], spendTime, param['count'], param['cliType']))

        if param['onlyonce']:
            break

        if remainTime > 0:
            time.sleep(remainTime)

def rmOldSpeedLog(site, port):
    r = redis.Redis(host=site, port=port, decode_responses=True)
    keyList = r.keys(RECORD_KEY + '*')
    for key in keyList:
        r.delete(key)


@click.command()
@click.option('-t', '--type', 'cliType', type=click.Choice(['hset', 'hgetall', 'hdel', 'stress', 'hget', 'getSpeed', 'clearSpeed']), help='Which redis-cli to send', required=True)
@click.option('-c', '--count', 'count', help='Send n times in a period', type=int, required=True)
@click.option('-d', '--period', 'time_period', help='How long a time period is(in seconds)', type=int, default=300, show_default=True)
@click.option('-s', '--site', 'site', help='Site of redis', type=str, default='10.205.91.11', show_default=True)
@click.option('-p', '--port', 'port', help='Port of redis', type=int, default=6379, show_default=True)
@click.option('-n', '--number', 'dbNumber', help='Database number', type=int, default=0, show_default=True)
@click.option('-o', '--onlyonce', 'onlyonce', help='Only execute once 1: True, 0: False', type=int, default=0, show_default=True)
@click.option('-m', '--multiple', 'multiple', help='Send multiple request at the same time', type=int, default=1, show_default=True)
def sendRedisCli(cliType, count, time_period, site, port, dbNumber, onlyonce, multiple):
    if cliType == 'clearSpeed':
        rmOldSpeedLog(site, port)
        print('Old speed logs are removed.') 
        exit()
    elif cliType == 'getSpeed':
        r = redis.Redis(host=site, port=port, decode_responses=True)
        keyList = r.keys(RECORD_KEY + '*')
        total = 0.0
        totalFail = 0
        if len(keyList) is 0:
             print('Please run any test first')
             exit()

        for key in keyList:
            data = r.hgetall(key)
            print(data)
            total += float(data['secs']) / (int(data['loop']) * int(data['count']))
            totalFail += int(data['fail'])
        print('Total value setting fail: {}, Avg time of each redis command: {} secs'.format(totalFail, total/len(keyList)))
        exit()

    if onlyonce:
        print('This tool will send {} times of {} cli once'.format(count, cliType))
    else:
        print('This tool will send {} times of {} cli in every {} secs'.format(count, cliType, time_period))
    print('Send to redis url[{}:{}] db{}'.format(site, port, dbNumber))
    if multiple > count:
        print('count need to bigger than multiple')
        exit()

    rmOldSpeedLog(site, port)
    #pool = redis.ConnectionPool(host=site, port=port, decode_responses=True)
    #r = redis.Redis(connection_pool=pool)
    distance = 0
    if cliType == 'stress':
        count = int(round( float(count) / 2))

    distance =  int(round( float(count) / multiple))
    count = distance

    pool = Pool(multiple)
    listTask = []
    paramDict = {}   
    startTime = time.time()
    for j in range(int(multiple)):
        paramDict[j] = {}
        paramDict[j]['cliType'] = cliType
        paramDict[j]['count'] = count
        paramDict[j]['time_period'] = time_period
        paramDict[j]['site'] = site
        paramDict[j]['port'] = port
        paramDict[j]['onlyonce'] = onlyonce
        paramDict[j]['start'] = int(j * distance)

        listTask.append(paramDict[j])
        
    pool.map(sendRedisRequest, listTask)
    pool.close()
    pool.join()
    endTime = time.time()
    spendTime = endTime-startTime
    print('Total spend time {} seconds'.format(spendTime))


if __name__ == '__main__':
    sendRedisCli()

