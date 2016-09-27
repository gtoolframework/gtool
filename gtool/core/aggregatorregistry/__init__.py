# --- statics ---

def aggregatorindex():
    __AGGREGATOR_INDEX = '__aggregatorindex'  # TODO singleton pattern for multiple global directories --> dynamicClasses, URN, instancenames (type aware), plugins
    return __AGGREGATOR_INDEX

# a shared globals ala...
# http://stackoverflow.com/questions/15959534/python-visibility-of-global-variables-in-imported-modules

def registerAggregator(aggregatorId, aggregatorobj, verbose=False):

    if aggregatorId in aggregatornamespace(): # globals()[objectindex()]:
        # this error will occur for a misconfig or a security event
        raise KeyError('One aggregator tried to overwrite an existing one. Aggregator name: %s' % aggregatorId)
    else:
        aggregatornamespace()[aggregatorId] = aggregatorobj
        if verbose:
            print('[VERBOSE] loading aggregator: %s' % aggregatorId)
        return True

def aggregatornamespace():
    return globals()[aggregatorindex()]


#--- initialize namespace
globals()[aggregatorindex()] = dict()