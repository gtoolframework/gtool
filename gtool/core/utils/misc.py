def striptoclassname(fullclassstring):
    return '{0}'.format(fullclassstring)[7:-2].split('.')[-1]