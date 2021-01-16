import yaml
admin = [2544704967,1627998372]
def get_respons(msg):
    f  = open('./resource/talker.yml')
    yml = yaml.load(f,Loader=yaml.SafeLoader)
    try:
        reply = yml[msg]
        return reply
    except:
        pass
def add(msg):
    f = open('./resource/talker.yml',mode='a+')
    f.write(msg)
def msger(msg,sender):
    if msg[:5] == 'add: ':
        check = yaml.load(msg[5:],Loader=yaml.SafeLoader)
        if type(check)  == dict: 
            if sender in admin:
                add(f'\n{msg[5:]}')
                return 'Add Successful'
            else:
                return 'You Are Not Bot Admin'
        else:
            return 'Please using right yaml'
    else:
        return get_respons(msg)
