#!/usr/bin/python3
import agent.config.parameter as parameter


def create_script(config, sample):
    output = sample.replace('{{REPLACE_TO_ACCOUNT}}', config['account'])
    output = output.replace('{{REPLACE_TO_PASSWORD}}', config['password'])
    output = output.replace('{{REPLACE_TO_URI}}', config['uri'])
    output = output.replace('{{REPLACE_TO_DEV1}}', config['dev1'])
    output = output.replace('{{REPLACE_TO_DEV2}}', config['dev2'])
    output = output.replace('{{REPLACE_TO_SITE}}', config['site'])

    script_name = config['site'] + '_testcase.py'
    with open('./routine_script/' + script_name, 'w') as f:
        f.write(output)


def main():
    with open('./jenkins_deploy_script/testsample.py', 'U') as f:
        template = f.read()

    site_cfg = parameter.SITE_CFG()
    for cfg in site_cfg:
        create_script(cfg, template)

    with open('./routine_script/exeApiScanAll.sh', 'w') as f:
        f.write('#!/bin/sh\n')
        for cfg in site_cfg:
            cmd = 'docker run --rm -v ' + parameter.LOG_DIR() \
                  + ':/log -d python_apiscan routine_script/' \
                  + cfg['site'] + '_testcase.py\n'
            f.write(cmd)


if __name__ == '__main__':
    main()
