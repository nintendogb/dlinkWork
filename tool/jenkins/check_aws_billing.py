import subprocess
import json
import redis
import datetime
import send_msg

check_metric_cmd = "aws --region us-east-1 cloudwatch list-metrics --namespace AWS/Billing --metric-name EstimatedCharges --dimensions Name=Currency,Value=USD --output text | grep ServiceName | awk '{ print $3 }'"
p = subprocess.run(check_metric_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
metric_list = p.stdout.decode().strip().split('\n')
has_error = False

service_bill = {}
for metric in metric_list:
    billing_cmd = f'aws --region us-east-1 cloudwatch get-metric-statistics \
    --namespace "AWS/Billing" \
    --metric-name "EstimatedCharges" \
    --dimensions Name=Currency,Value=USD \
        Name=ServiceName,Value={metric} \
    --start-time $(date +"%Y-%m-%dT%H:%M:00" --date="-15 hours") \
    --end-time $(date +"%Y-%m-%dT%H:%M:00") \
    --statistic Maximum \
    --period 57600'
    # --output text | sort -r -k 3 | head -n 1 | cut -f 2'
    p = subprocess.run(billing_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    tmp_json = json.loads(p.stdout.decode())
    # print(metric, tmp_json)
    try:
        service_bill[metric] = {'cost': tmp_json['Datapoints'][0]['Maximum'], 'timestamp': tmp_json['Datapoints'][0]['Timestamp']}
    except (IndexError):
        has_error = True
        service_bill[metric] = {'error': 'No data', 'cost': 0, 'res_json': tmp_json}


redis_url = '54.67.52.204'
redis_port = 6379

r = redis.Redis(
    host=redis_url,
    port=redis_port,
    decode_responses=True
)


curr_date = datetime.datetime.now()
r.lpush(f'day_list', curr_date.strftime("%m/%d"))
r.ltrim(f'day_list', 0, 6)
total = 0.0
for service in service_bill:
    if 'error' in service_bill[service]:
        continue

    cur_cost = service_bill[service]['cost']
    if r.hexists('lastest_cost', service):
        service_bill[service]['cost'] -= float(r.hget('lastest_cost', service))
    if r.hexists('lastest_cost', f'{service}_update'):
        service_bill[service]['pre_timestamp'] = r.hget('lastest_cost', f'{service}_update')
    if service_bill[service]['cost'] < 0:
        service_bill[service]['cost'] = cur_cost
    r.hset('lastest_cost', service, cur_cost)
    r.hset('lastest_cost', f'{service}_update', service_bill[service]['timestamp'])
    total += service_bill[service]['cost']
r.lpush('total_list', f'{total:.2f}')
r.ltrim('total_list', 0, 6)







sorted_service = sorted(
    metric_list, 
    key = lambda k : service_bill[k]['cost'],
    reverse=True
)

if has_error:
    error_res = ''
    for service in sorted_service:
        if 'error' in service_bill[service]:
            error_res = f'{error_res}\n[{service}] Err:[{service_bill[service]["error"]}] Res:[{service_bill[service]["res_json"]}]'
    send_msg.send_slack_msg(error_res, ['#team-siqad-usqa-usage'])

cost_res = '自從上次檢查後 前五大消耗的服務為\n'
count = 0
for service in sorted_service:
    if 'error' in service_bill[service]:
        continue

    count += 1
    cost_res += f'{count}. *{service_bill[service]["cost"]:.2f}* USD @  *{service}*\n    [{service_bill[service]["pre_timestamp"]}] > [{service_bill[service]["timestamp"]}]\n'
    if count >= 5:
        break

days_num = r.llen('day_list')
history_res = f'如下為{r.llen("day_list")}天內的每日消耗費用\n'
for cnt in range(days_num):
    cost = r.lindex(f'total_list', cnt)
    history_res += f'    {r.lindex("day_list", cnt)}: *{cost}*\n'

send_msg.send_slack_msg(cost_res, ['#team-siqad-usqa-usage'])
send_msg.send_slack_msg(history_res, ['#team-siqad-usqa-usage'])
#send_msg.send_slack_msg(cost_res, ['@Ted.Kao'])
#send_msg.send_slack_msg(history_res, ['@Ted.Kao'])
