#!/usr/bin/python3
import click


@click.command()
@click.option('-w', '--work', 'work', help='work dir', required=True)
@click.option('-l', '--log', 'log', help='log dir', required=True)
@click.option(
    '-p',
    '--log_period',
    'log_period',
    help='log checking period',
    required=True
)
@click.option(
    '-a',
    '--alert_period',
    'alert_period',
    help='alert trigger period',
    required=True
)
def change_config(work, log, log_period, alert_period):
    print('work dir: {}'.format(work))
    print('log dir: {}'.format(log))

    with open('./agent/config/parameter.py', 'U') as f:
        template = f.read()
    output = template.replace('{{WORK_DIR}}', work)
    output = output.replace('{{LOG_DIR}}', log)
    output = output.replace('{{LOGGING_PERIOD}}', log_period)
    output = output.replace('{{ALERT_PERIOD}}', alert_period)
    with open('./agent/config/parameter.py', 'w') as f:
        f.write(output)


if __name__ == '__main__':
    change_config()
