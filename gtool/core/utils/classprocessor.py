import pyparsing as p
import collections

# Statics
# TODO make this proper object or wrap inside a module
MODE_KEYWORD_MULTIPLE = 'multiple'
MODE_KEYWORD_SINGLE = 'single'


def readClass(configString):

    def caps(string, location, tokens):
        return str.capitalize(tokens[0])

    def isList(string, location, tokens):
        return True

    def classParser():
        # --- class parser ---
        classColon = p.Literal('::').suppress()
        className = p.Word(p.alphas.upper()).setResultsName('classname')
        classDef = className + classColon + p.LineEnd().suppress()
        return classDef

    def _classParser():
        # --- class parser ---
        classColon = p.Literal('::').suppress()
        className = p.Word(p.alphas.upper())
        classDef = className + classColon + p.LineEnd().suppress()
        return classDef

    def metaParser():
        # --- meta parser ---
        metaIndicator = p.LineStart() + p.Suppress(p.Literal('*'))
        metaName = p.Word(p.alphanums).setResultsName('metaname')
        metaSeparator = p.Suppress(p.Literal('='))

        # TODO force case insensitivity in attributeMode keyword match
        # TODO add debug names
        # TODO add a conditional debug flag

        metavalue = p.Combine(p.restOfLine() + p.Suppress(p.LineEnd())).setResultsName('metavalue')

        metaList = p.Dict(p.Group(metaIndicator +
                                metaName +
                                metaSeparator +
                                metavalue
                                ))
        return metaList

    def _metaParser():
        # --- meta parser ---
        metaIndicator = p.LineStart() + p.Suppress(p.Literal('*'))
        metaName = p.Word(p.printables)
        metaSeparator = p.Suppress(p.Literal('='))

        # TODO force case insensitivity in attributeMode keyword match
        # TODO add debug names
        # TODO add a conditional debug flag

        metavalue = p.Combine(p.restOfLine() + p.Suppress(p.LineEnd()))

        metaList = metaIndicator + metaName + metaSeparator + metavalue
        return metaList

    def _funcParser():
        # --- func attribute parser ---

        # TODO add debug names
        # TODO add a conditional debug flag

        bracedString = p.Combine(p.Regex(r"{(?:[^{\n\r\\]|(?:{})|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*") + "}").setName(
            "string enclosed in braces")

        funcIndicator = p.Literal('!')
        funcIndicator.setName('indicator')

        funcName = p.Word(p.alphanums)
        funcName.setName('name')
        funcSeparator = p.Suppress(p.Literal('::'))
        funcSeparator.setName('separator')

        funcModule = p.Word(p.printables, excludeChars='(')
        funcModule.setName('module')
        funcDemarcStart = p.Literal("(")
        funcDemarcStart.setName('demarcstart')

        funcDemarcEnd = p.Literal(")")
        funcDemarcEnd.setName('demarcend')

        funcMiddle = p.nestedExpr() #(p.sglQuotedString() | bracedString()) # | p.dblQuotedString())
        funcMiddle.setName('middle')

        funcPattern = p.LineStart() + p.Suppress(funcIndicator) + funcName + p.Suppress(funcSeparator) + \
                      funcModule + funcMiddle + \
                      p.Suppress(p.Optional(p.LineEnd())) #funcModule + p.Suppress(funcDemarcStart) + p.Optional(funcMiddle) + p.Suppress(funcDemarcEnd) + \

        return funcPattern

    def attributeParser():
        # --- attribute parser ---
        attributeIndicator = p.LineStart() + p.Suppress(p.Literal('@'))
        attributeName = p.Word(p.alphanums).setResultsName('attributename')
        attributeSeparator = p.Suppress(p.Literal('::'))

        # TODO force case insensitivity in attributeMode keyword match
        # TODO add debug names
        # TODO add a conditional debug flag

        attributeMode = (
                            p.Word(MODE_KEYWORD_SINGLE) | p.Word(MODE_KEYWORD_MULTIPLE)
                        ).setResultsName('attributemode') + p.Literal(':').suppress()

        attributeType = (p.Word(p.alphanums).setResultsName('attributetype')).setParseAction(caps)

        attributePosargs = p.ZeroOrMore(
            (
                p.Word(p.alphanums) |
                p.Combine(
                    p.Literal('[') + p.SkipTo(']') + p.Literal(']')
                )
            ) + ~p.FollowedBy(p.Literal('=')) +
            p.Optional(p.Literal(',').suppress())
        ).setResultsName('posargs')

        attributeKwargs = p.ZeroOrMore(
            p.Group(
                p.Word(p.alphanums).setResultsName('keyword') +
                p.Literal('=').suppress() +
                (
                    p.Word(p.alphanums) | p.Combine(
                        p.Literal('[') + p.SkipTo(']') + p.Literal(']')
                    )
                ).setResultsName('value') +
                p.Optional(p.Literal(',').suppress())
            )
        ).setResultsName('kwargs')

        attributeArgs = (
            p.Literal('(').suppress() +
            attributePosargs +
            attributeKwargs +
            p.Literal(')').suppress()
        ).setResultsName('attributeargs')

        attributeList = p.Group(attributeIndicator +
                                attributeName +
                                attributeSeparator +
                                attributeMode +
                                attributeType +
                                p.Optional(attributeArgs)
                                )
        return attributeList

    def _attributeParser():
        # --- attribute parser ---
        attributeIndicator = p.LineStart() + p.Suppress(p.Literal('@'))
        attributeName = p.Word(p.alphanums).setResultsName('attributename')
        attributeSeparator = p.Suppress(p.Literal('::'))


        # TODO force case insensitivity in attributeMode keyword match
        # TODO add debug names
        # TODO add a conditional debug flag

        attributeMode = (
                            p.Word(MODE_KEYWORD_SINGLE) | p.Word(MODE_KEYWORD_MULTIPLE)
                        ).setResultsName('attributemode') + p.Literal(':').suppress()

        attributeType = (p.Word(p.alphanums).setResultsName('attributetype')).setParseAction(caps)

        attributePosargs = p.ZeroOrMore(
            (
                p.Word(p.alphanums) |
                p.Combine(
                    p.Literal('[') + p.SkipTo(']') + p.Literal(']')
                )
            ) + ~p.FollowedBy(p.Literal('=')) +
            p.Optional(p.Literal(',').suppress())
        ).setResultsName('posargs')

        attributeKwargs = p.ZeroOrMore(
            p.Group(
                p.Word(p.alphanums).setResultsName('keyword') +
                p.Literal('=').suppress() +
                (
                    p.Word(p.alphanums) | p.Combine(
                        p.Literal('[') + p.SkipTo(']') + p.Literal(']')
                    )
                ).setResultsName('value') +
                p.Optional(p.Literal(',').suppress())
            )
        ).setResultsName('kwargs')

        attributeArgs = (
            p.Literal('(').suppress() +
            attributePosargs +
            attributeKwargs +
            p.Literal(')').suppress()
        ).setResultsName('attributeargs')

        attributeList = attributeIndicator + attributeName + attributeSeparator + \
                        attributeMode + attributeType + p.Optional(attributeArgs)
        return attributeList

    def _generateAttributes(attributes):

        tempDict = {}
        for attribute in attributes:
            #print(attribute)
            # TODO throw error if attribname matches names in classgen methodsdict to prevent override (move methodsdict to getter method in classgen module)
            args = getattr(attribute, 'attributeargs', None)[0:]
            # TODO figure out why this slicing works and we get weird cruft when we don't use it

            if attribute.attributemode == 'single':
                mode_ = False
            else:
                mode_ = True

            tempDict[attribute.attributename] = {
                'type': attribute.attributetype,  # TODO should type be a string or a ref to the class?
                'list': mode_,
                'args': {
                    'kwargs': attribute.attributeargs.kwargs if 'kwargs' in attribute.attributeargs else [],
                    'posargs': attribute.attributeargs.posargs if 'posargs' in attribute.attributeargs else []
                }
            }

            if args:
                tempDict[attribute.attributename]['arguments'] = args
        #print(tempDict)
        return tempDict

    def parseconfig(configstring):
        # --- full parser ---
        # print('--- parseConfig ---')
        _classblocklist_start = []

        configblocks = []

        for x in _classParser().scanString(configstring):
            _classblocklist_start.append(x[1])

        _classblocklist_start.append(len(configstring)-1)

        for i in range(1,len(_classblocklist_start)):
            start = _classblocklist_start[i-1]
            end = _classblocklist_start[i]
            configblocks.append(configstring[start: end])

        parsedconfigs = {}

        for block in configblocks:

            _parsedconfig = {}
            _classname = None

            #print('\n--- class ---')
            for x in _classParser().scanString(block):
                #print(x[0])
                _classname = x[0][0]
                #_parsedconfig[_classname] = {}

            #print('--- meta ---')
            _metadict = {}
            for x in _metaParser().scanString(block):
                #print(x[0])
                _metadict[x[0][0]] = x[0][1]
            _parsedconfig['metas'] = _metadict

            #print('--- attributes ---')
            _attributedict = {}
            _attribparseresultslist = []
            for x in _attributeParser().scanString(block):
                #print(x)
                _attributedict[x[0][0]] = x[0][1:]
                _attribparseresultslist.append(x[0])
            _parsedconfig['attributes'] = _generateAttributes(_attribparseresultslist)

            #TODO add parser for methods (should inject a property into attrs or list_slots?

            #print('--- methods ---')
            """
            We use an orderedDict to ensure that dependencies in methods that take other methods as input aren't broken.
            A normal dict get's read randomly and will result in attribute errors when you call
            """
            _methodsdict = collections.OrderedDict()
            for x in _funcParser().scanString(block):
                #print(x[0])

                #check if method contains a config string
                if len(x[0]) < 2:
                    _config = None
                elif len(x[0][2]) > 0:

                    if len(x[0][2]) == 1:
                        _match = x[0][2][0][1:-1]
                    else:
                        _match = ' '.join(x[0][2])

                    if _match.startswith("'") and _match.endswith("'"):
                        _match = _match[1:-1]
                    #if _match.endswith("'"):
                    #    _match = _match[:-1]

                    _config = _match
                else:
                    _config = None

                #print(_config)

                _methodsdict[x[0][0]] = {'module': x[0][1],
                                         'config': _config
                                         }

            #print(_methodsdict)

            _parsedconfig['methods'] = _methodsdict  # not being used yet

            #_parsedconfig['processors'] = None,  # not being used yet
            #_parsedconfig['renderengines'] = None  # not being used yet

            parsedconfigs[_classname] =_parsedconfig

        #print(parsedconfigs)
        #print('--- parseConfig --\n\n')
        return parsedconfigs

    # --- full parser ---

    #parseconfig(configString)

    """
    classStructure = p.Group(classParser() +
                             p.ZeroOrMore(metaParser()).setResultsName('metas') +
                             p.OneOrMore(attributeParser()).setResultsName('attributes') +
                             p.ZeroOrMore(funcParser().setResultsName('methods')))

    parser = p.Dict(p.OneOrMore(classStructure))
    """

    #return parser.parseString(configString)
    return parseconfig(configString)

# read https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/


def debugClass(config):
    for classDef in config:
        print(list(classDef.keys()))
        print(classDef.classname)
        if 'metas' in classDef:
            print('metas: ', classDef['metas'])
        for attribute in classDef.attributes:
            print(list(attribute.keys()))
            print(attribute.attributename)
            print(attribute.attributemode)
            if 'attributeargs' in attribute:
                print(list(attribute.attributeargs.keys()))
                if 'posargs' in attribute:
                    print(attribute.posargs)
                if 'kwargs' in attribute:
                    print(attribute.kwargs)
        if 'methods' in classDef:
            print('methods:', classDef['methods'])
    return None


def processClass(config):

    def generateMetas(element):
        _metaDict = {}
        if 'metas' in element:
            _metaDict = {k[0]: k[1] for k in element.metas}
        return _metaDict

    def generateMethods(element):
        """
        We use an orderedDict to ensure that dependencies in methods that take other methods as input aren't broken.
        A normal dict get's read randomly and will result in attribute errors when you call
        """
        _methodDict = collections.OrderedDict()
        if 'methods' in element:
            _methodDict = element.methods
        return _methodDict

    def generateAttributes(attributes):

        tempDict = {}
        for attribute in attributes:
            #print(attribute)
            # TODO throw error is attribname matches names in classgen methodsdict to prevent override (move methodsdict to getter method in classgen module)
            args = getattr(attribute, 'attributeargs', None)[0:]
            # TODO figure out why this slicing works and we get weird cruft when we don't use it

            if attribute.attributemode == 'single':
                mode_ = False
            else:
                mode_ =True

            tempDict[attribute.attributename] = {
                'type': attribute.attributetype,  # TODO should type be a string or a ref to the class?
                'list': mode_,
                'args': {
                    'kwargs': attribute.attributeargs.kwargs if 'kwargs' in attribute.attributeargs else [],
                    'posargs': attribute.attributeargs.posargs if 'posargs' in attribute.attributeargs else []
                }
            }

            if args:
                tempDict[attribute.attributename]['arguments'] = args
        #print(tempDict)
        return tempDict

    classDict = {}
    for element in config:
        classDict[element.classname] = {
            'metas': generateMetas(element),
            'attributes': generateAttributes(element.attributes),
            'methods': generateMethods(element),
            'processors': None, # not being used yet
            'renderengines': None # not being used yet
        }

    # TODO return a list, not a dict otherwise class definitions can overwrite each other (we will catch this latter)
    #print('classdict:', classDict)
    return classDict


