import yaml
admin = [2544704967]
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
        if sender in admin:
            add(f'{msg[5:]}\n')
            return 'Add Successful'
        else:
            return 'You Are Not Bot Admin'
    else:
        return get_respons(msg)
