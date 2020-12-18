import agent.agent as agent
import agent.config.parameter as parameter



def subs_dev(mydlink_id):
    uap = agent.Uap(
        'qa-us-openapi.auto.mydlink.com',
        parameter.APP_ID(),
        parameter.APP_SECRET()
    )
    uap.get_user_token(f'testqaid+{mydlink_id}@sqadt1.mydlink.com', 'mydlink')
    uap.cnvr_query_subscription()
    try:
        subs_uid = uap.res.json()['data'][0]['subs_uid']
        if uap.res.json()['data']:
            print('Add dev to exist plan.')
            uap.cnvr_enable_device_subscription(subs_uid, [mydlink_id])
        else:
            print('Create free trial and add dev to it.')
            uap.cnvr_subscribe_freetrial([mydlink_id])
    except (IndexError):
        print('Create free trial and add dev to it.')
        uap.cnvr_subscribe_freetrial([mydlink_id])

    uap.cnvr_query_subscription()


for i in range(88000031, 88000061):
    subs_dev(str(i))

