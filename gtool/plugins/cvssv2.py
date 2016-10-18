from gtool.core.types.core import FunctionType
import pyparsing as p
from gtool.core.utils.misc import striptoclassname
from cvsslib import cvss2, calculate_vector

class Cvssv2(FunctionType):
    """
    Calculates a CVSSv2 score given a valid CVSSv2 vector string

    Example strings is :
    'AV:L/AC:M/Au:S/C:N/I:P/A:C/E:U/RL:OF/RC:UR/CDP:N/TD:L/CR:H/IR:H/AR:H'
    """

    def __init__(self, obj, config=str()):

        super(Cvssv2, self).__init__(obj, config=config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Cvssv2 plugin function requires an attribute be specified such as "@vector"')

    def compute(self):

        def getname(obj, name):

            _val = None

            if hasattr(obj, name):
                _val = getattr(obj, name, None)

            if _val is None:
                return _val

            # handling for values from a method
            if isinstance(_val, str):
                return _val

            try:
                if _val.isdynamic:
                    raise ValueError('Cvssv2 plugin cannot process %s because it contains a dynamic class' % name)
            except AttributeError:
                raise TypeError('Expected an attribute but got a %s' % type(_val))

            if _val.issingleton():
                _ret = '%s' % _val[0].raw()
            else:
                raise ValueError('Cvssv2 method plugin specified in user defined class %s '
                                 'only works on singleton attributes' % striptoclassname(type(self.targetobject)))

            return _ret

        attrid = (p.Literal('@') | p.Literal('!')).suppress() + p.Word(p.alphanums)

        attrexpr = attrid.setResultsName('attribute')

        parseresult = attrexpr.parseString(self.config)


        _attrname = parseresult.get('attribute', None)[0]

        if _attrname is None:
            raise ValueError('The configuration string provided to the Cvssv2 method '
                             'plugin in user defined class %s does not contain an '
                             'identifiable attribute. Please provide a configuration '
                             'string in the form of \'@attribute[#:#]\'' % striptoclassname(type(self.targetobject)))

        self.vector = getname(self.targetobject, _attrname)

        if isinstance(self.vector, str):
            self.computable = True

        if self.computable:
            try:
                _score = calculate_vector(self.vector, cvss2)
                _index = len([c for c in _score if c is not None]) - 1
                self.__result__ = _score[_index]
                #self.__result__ = ', '.join(str(i) for i in _score)
            except Exception as err:
                raise Exception('When the Cvssv2 method plugin used in '
                                'the %s class attempted to process the provided '
                                'vector string from %s in %s, the following '
                                'error occured: %s' %
                                (
                                    striptoclassname(type(self.targetobject)),
                                    _attrname,
                                    self.targetobject.__context__['file'],
                                    err
                                ))


def load():
    return Cvssv2
