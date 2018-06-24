from pyparsing import *
import pprint


def make_keyword(kwd_str, kwd_value):
    return Keyword(kwd_str).setParseAction(replaceWith(kwd_value))

def makeJSONObject():

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

def makeEdgeDOTObject():

    # define grammar for edges
    node_name = Word(alphas)
    node_id = Word(alphanums)
    nodeElem = (Combine(node_name + "_" + node_id))

    #node = nodeElem
    jsonObject = makeJSONObject()
    node = Group(nodeElem + ZeroOrMore(jsonObject))

    RANGLE = Literal('>')
    REMOVE = Literal('!')
    PIPE = Literal('|')

    edgeExpr = Forward()
    edgeExpr <<  Group(node  + (RANGLE ^ REMOVE ^ PIPE)) + ( node ^ OneOrMore(edgeExpr))
    return edgeExpr

test_str = """x_01 > x_02 {"1":0,"2":1} > x_03 A_01 | B_01
y_01 > y_02 {"x1":"val1"} > y_03
z_01 > z_02 {"x1":"val1"} > z_03
x_01 | x_02 {"1":0,"2":1} ! x_03
"""
#edgeLists = (' ').splitlines()
edgeExpr = makeEdgeDOTObject() 
edgeLists = test_str.splitlines()
for edges in edgeLists:
    print("***\n"+edges)
    result = edgeExpr.parseString(edges)
    #result = edgeListExpr.parseString(edges)
    for num, token in enumerate(result):
        print('token: #'+str(num))
        pprint.pprint(token)
    print("")

def makeEdgeCypherObject():

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
    nodeObject = node ^ Group((LBRACK + nodeList + RBRACK))
    
    
    jsonObject = makeJSONObject()
    portMapObject = Group(LBRACE + node + RBRACE)
    edge = (RANGLE ^ REMOVE ^ PIPE) + (Optional(jsonObject) ^ Optional(portMapObject) )

    
    edgeExpr = Forward()
    edgeExpr <<  Group(nodeObject  + edge ) + ( nodeObject ^ OneOrMore(edgeExpr))

    edgeObject = Forward()
    edgeObject << edgeExpr + ZeroOrMore(edgeObject)
    return edgeObject

print("\n\n\n **** \n\n\n")
test_str_02 = """x_01 > x_02 > x_03 A_01 !{"key":"val"} B_01
[y_01,y_02] > y_03 z_01 | z_02
[y_01,y_02] >{"key":1} [y_03,y_04] | y_05 >{"key":"val"} y_06 |{ola_01} y_07 | y_08
"""
edgeExpr = makeEdgeCypherObject() 
edgeLists = test_str_02.splitlines()
for edges in edgeLists:
    print("***\n"+edges)
    result = edgeExpr.parseString(edges)
    for num, token in enumerate(result):
        print('token: #'+str(num))
        pprint.pprint(token)
    print("")
