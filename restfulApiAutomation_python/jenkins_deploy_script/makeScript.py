#!/usr/bin/python3
import agent.config.parameter as parameter


def create_script(config, sample):
    output = sample.replace('{{REPLACE_TO_ACCOUNT}}', "'{}'".format(config['account']))
    output = output.replace('{{REPLACE_TO_PASSWORD}}', "'{}'".format(config['password']))
    output = output.replace('{{REPLACE_TO_URI}}', "'{}'".format(config['uri']))
    output = output.replace('{{REPLACE_TO_DEV1}}', "'{}'".format(config['dev1']))
    output = output.replace('{{REPLACE_TO_SITE}}', "'{}'".format(config['site']))
    output = output.replace('{{REPLACE_TO_THRESHOLD}}', config['thres'])
    output = output.replace('{{REPLACE_TO_FW_THRESHOLD}}', config['fw_thres'])

    script_name = config['site'] + '_testcase.py'
    with open('./routine_script/' + script_name, 'w') as f:
        f.write(output)

def create_openapi_test(config, sample):
    output = sample.replace('{{REPLACE_TO_ACCOUNT}}', "os.environ['AUTO_TEST_ACCOUNT']")
    output = output.replace('{{REPLACE_TO_PASSWORD}}', "os.environ['AUTO_TEST_PASSWORD']")
    output = output.replace('{{REPLACE_TO_URI}}', "'{}-openapi.auto.mydlink.com'.format(SITE)")
    output = output.replace('{{REPLACE_TO_DEV1}}', "os.environ['AUTO_TEST_DEV']")
    output = output.replace('{{REPLACE_TO_SITE}}', "os.environ['AUTO_TEST_SITE']")
    output = output.replace('{{REPLACE_TO_THRESHOLD}}', config['thres'])
    output = output.replace('{{REPLACE_TO_FW_THRESHOLD}}', config['fw_thres'])

    with open('./test/openapi_test.py', 'w') as f:
        f.write(output)


def main():
    with open('./jenkins_deploy_script/testsample.py', 'U') as f:
        template = f.read()

    site_cfg = parameter.SITE_CFG()
    for cfg in site_cfg:
        create_script(cfg, template)

    create_openapi_test(cfg, template)

    with open('./routine_script/exeApiScanAll.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(
            'docker run --rm -d --name binding_dev python_apiscan python3 /test/bind_test_dev.py' \
            + '|| echo "There has some error at binding step"\n'
        )
        f.write('sleep 180\n')
        for cfg in site_cfg:
            cmd = f'docker run --name routine_{cfg["site"]} --net=host --rm -v ' + parameter.LOG_DIR() \
                  + ':/log -d python_apiscan python3 routine_script/' \
                  + cfg['site'] + '_testcase.py\n'
            f.write(cmd)


if __name__ == '__main__':
    main()
