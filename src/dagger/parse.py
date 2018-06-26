from pyparsing import *
from pprint import pprint
import yaml


def make_keyword(kwd_str, kwd_value):
    return Keyword(kwd_str).setParseAction(replaceWith(kwd_value))

def make_JSON_parser_object():

    TRUE  = make_keyword("true", True)
    FALSE = make_keyword("false", False)
    NULL  = make_keyword("null", None)

    LBRACK, RBRACK, LBRACE, RBRACE, COLON = map(Suppress, "[]{}:")

    word = Word(alphas)
    
    jsonString = dblQuotedString().setParseAction(removeQuotes)
    jsonNumber = pyparsing_common.number()

    jsonObject = Forward()
    jsonValue = Forward()
    jsonElements = delimitedList( jsonValue )
    jsonArray = Group(LBRACK + Optional(jsonElements, []) + RBRACK)
    jsonValue << (jsonString | jsonNumber | Group(jsonObject)  | jsonArray | TRUE | FALSE | NULL)
    memberDef = Group(jsonString + COLON + jsonValue)
    jsonMembers = delimitedList(memberDef)
    jsonObject << Dict(LBRACE + Optional(jsonMembers) + RBRACE)
    

    jsonComment = cppStyleComment 
    jsonObject.ignore(jsonComment)
    return jsonObject

def make_edge_DOT_parser_object():

    # define grammar for edges
    node_name = Word(alphas)
    node_id = Word(alphanums)
    nodeElem = (Combine(node_name + "_" + node_id))

    jsonObject = make_JSON_parser_object()
    node = Group(nodeElem + ZeroOrMore(jsonObject))

    RANGLE = Literal('>')
    REMOVE = Literal('!')
    PIPE = Literal('|')

    edgeExpr = Forward()
    edgeExpr <<  Group(node  + (RANGLE ^ REMOVE ^ PIPE)) + ( node ^ OneOrMore(edgeExpr))
    return edgeExpr


def make_edge_Cypher_parser_object():

    # define grammar for edges
    RANGLE = Literal('>')
    REMOVE = Literal('!')
    PIPE = Literal('|')

    LBRACK = Literal('[').suppress()
    RBRACK = Literal(']').suppress()
    COMMA = Literal(',').suppress()

    LBRACE = Literal('{')
    RBRACE = Literal('}')

    node_name = Word(alphas)
    node_id = Word(alphanums)
    node = (Combine(node_name + "_" + node_id))

    nodeList = Forward()
    nodeList << node + ZeroOrMore(COMMA + nodeList)
    nodeObject = node ^ Group((LBRACK + nodeList + RBRACK))
    
    
    jsonObject = make_JSON_parser_object()
    portMapObject = Group(LBRACE + node + RBRACE)
    edge = (RANGLE ^ REMOVE ^ PIPE) + (Optional(jsonObject) ^ Optional(portMapObject) )

    
    edgeExpr = Forward()
    edgeExpr <<  Group(nodeObject  + edge ) + ( nodeObject ^ OneOrMore(edgeExpr))

    edgeObject = Forward()
    edgeObject << edgeExpr + ZeroOrMore(edgeObject)
    return edgeObject


def make_edge_Cypher_parser_exp():

    # define grammar for edges
    RANGLE = Literal('>')
    REMOVE = Literal('!')
    PIPE = Literal('|')

    LBRACK = Literal('[').suppress()
    RBRACK = Literal(']').suppress()
    COMMA = Literal(',').suppress()

    LBRACE = Literal('{').suppress()
    RBRACE = Literal('}').suppress()

    node_name = Word(alphas)
    node_id = Word(alphanums)
    node = (Combine(node_name + "_" + node_id))

    nodeList = Forward()
    nodeList << node + ZeroOrMore(COMMA + nodeList)
    nodeObject = (node ^ Group((LBRACK + nodeList + RBRACK)))
    
    
    jsonObject = make_JSON_parser_object()
    portMapObject = Group(LBRACE + node + RBRACE)
    edgeSymbol = (RANGLE ^ REMOVE ^ PIPE)
    edge = (edgeSymbol + (Optional(jsonObject) ^ Optional(portMapObject) ))
    

    
    edgeExpr = Forward()
    edgeExpr <<  Group(nodeObject  + edge ) + ( nodeObject ^ OneOrMore(edgeExpr))

    edgeObject = Forward()
    edgeObject << edgeExpr + ZeroOrMore(edgeObject)
    return edgeObject


class EdgeListReader:

    keys = ['left','op','prop','right']
    empty_buffer = dict.fromkeys(keys)

    def __init__(self):

        self.buffer = self.empty_buffer
        self.edge_list = []
    
    def _fill_buffer(self,token):
        
        buffer = {}
        vals = [None,None,None,None]

        if isinstance(token,str):
            vals[0] = token        
        else:
            vals[0] = token.asList()[0]
            vals[1] = token.asList()[1]
            vals[2] = token.asDict()
            vals[3] = None

        buffer = dict(zip(self.keys,vals))
        return buffer
    

    def push(self,token):
        
        edge = self.buffer

        if isinstance(token,str):
            # reached end-of-path
            edge['right'] = token
            buffer = self.empty_buffer
        
        if not self.buffer:
            buffer = self._fill_buffer(token)
        else:
            buffer = self._fill_buffer(token)
            edge['right'] = buffer['left']
        
        
        if  edge['op'] and edge['left'] and edge['right']:
            self.edge_list.append(edge)
        
        self.buffer = buffer




import pdb
test_str = """[xx_01, xy_01] >{"1":{"2":3}} [xy_02, xy_02] > x_03 > x_04 y_01 > y_05
z_01 ! z_02 a_01 |{"a":12} a_02
"""

test_str_01 = """x_01 >{"1":0} x_02 >{} x_03 y_01 > y_02
"""

edgeList = EdgeListReader()
edgeExpr = make_edge_Cypher_parser_exp() 
edgeLists = test_str.splitlines()

for edges in edgeLists:
    #pprint("***\n"+edges)
    result = edgeExpr.parseString(edges)

    #result = edgeListExpr.parseString(edges)
    for num, token in enumerate(result):
        #print('token: #'+str(num))
        edgeList.push(token)
        #pdb.set_trace()
    #print("")

pprint(edgeList.edge_list)


KEY_ACTIONS = ['ConfigDAG','ImportDAGs','CreateNodes','UpdateNodes','RemoveNodes','MakeDAG']
KEY_NODE_ATTRIBUTES = ['name','','CreateNodes','UpdateNodes','RemoveNodes','MakeDAG']


# first pass checks are done
def load_dag_spec(file = "./examples/Eg2.yaml"):

    dag_stream = {}
    
    with open(file, 'r') as stream:
        try:
            for doc in yaml.load_all(stream):
                print('***')

                for key, val in doc.items():
                    
                    if key not in KEY_ACTIONS:
                        msg = '{} is not a legal action'.format(key)
                        raise ValueError(msg)

                    if key in dag_stream.keys():
                        msg = '{} can not appear more than once in the spec'.format(key)
                        raise ValueError(msg)

                    dag_stream[key] = val
        
        except yaml.YAMLError as exc:
            pprint(exc)
    return dag_stream

dag_stream = load_dag_spec()
pprint(dag_stream)