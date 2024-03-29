from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time
from execption import MiniSQLError, MiniSQLSyntaxError
from enum import Enum
from utilis import *


class MiniSQLType(Enum):
    CREATE_TABLE = 0
    INSERT = 1
    DROP_TABLE = 2
    CREATE_INDEX = 3
    DROP_INDEX = 4
    SELECT = 5
    DELETE = 6
    QUIT = 7
    EXECFILE = 8
    RECOVER = 9


def execfile(file):
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            query = line
            line = line.strip()
            if line and line[-1] == ';':
                try:
                    
                    status = interpret(query)
                    if status == 1:
                        break
                except MiniSQLError as e:
                    print('In line {}: {}'.format(i + 1, e))
                    break


def judge_type(query):
    query = query.lower().strip(';\n ').split()
    if query[0] == 'insert':
        return MiniSQLType.INSERT
    elif query[0] == 'select':
        return MiniSQLType.SELECT
    elif query[0] == 'delete':
        return MiniSQLType.DELETE
    elif query[0] in ['quit', 'exit']:
        return MiniSQLType.QUIT
    elif query[0] == 'execfile':
        return MiniSQLType.EXECFILE
    elif query[0] == 'create':
        if query[1] == 'table':
            return MiniSQLType.CREATE_TABLE
        elif query[1] == 'index':
            return MiniSQLType.CREATE_INDEX
    elif query[0] == 'drop':
        if query[1] == 'table':
            return MiniSQLType.DROP_TABLE
        elif query[1] == 'index':
            return MiniSQLType.DROP_INDEX

    raise MiniSQLSyntaxError('Error Type')


def interpret(query):
    type = judge_type(query)
    queryarr = query.split()
    res = None
    if type == MiniSQLType.CREATE_TABLE:
        name = queryarr[2]
        name = name[:name.index("(")]
        if existsTable(name):
            print("There is a table "+name+" already")
        else:
            ip = createTable(name)
            if ip == "No more region server!":
                res = "No more region server!"
            else:
                res = command(ip, query)
    elif type == MiniSQLType.CREATE_INDEX:
        name = queryarr[4]
        name = name[:name.index("(")]
        ip = whereTable(name)
        res = command(ip, query)
    elif type == MiniSQLType.INSERT:
        name = queryarr[2]
        ip = whereTable(name)
        res = command(ip, query)
    elif type == MiniSQLType.SELECT:
        name = queryarr[3]
        if name[-1] == ';':
            name = name[:name.index(";")]
        ip = whereTable(name)
        res = command(ip, query)
    elif type == MiniSQLType.DELETE:
        name = queryarr[2]
        if name[-1] == ';':
            name = name[:name.index(";")]
        ip = whereTable(name)
        res = command(ip, query)
    elif type == MiniSQLType.DROP_INDEX:
        name = queryarr[2]
        name = name[:name.index(";")]
        ip = whereTable(name)
        res = command(ip, query)
    elif type == MiniSQLType.DROP_TABLE:
        name = queryarr[2]
        name = name[:name.index(";")]
        ip = dropTable(name)
        if ip == "error":
            res = "error"
        else:
            res = command(ip, query)
    elif type == MiniSQLType.QUIT:
        return 1
    elif type == MiniSQLType.EXECFILE:
        name = queryarr[1]
        name = name[:name.index(";")]
        execfile(name)
    if res != None:
        print(res)
    return 0


if __name__ == "__main__":
    query = ''
    fileread = 0
    filerecovery = 0
    status = 0
    while True:
        print('minisql>>', end=' ')
        cmd = input()
        query += cmd + ' '
        cmd = cmd.strip()
        if cmd and cmd[-1] == ';':
            # print(query)
            try:
                status = interpret(query)
                if status == 1:
                    break
            except MiniSQLError as e:
                print(e)
            query = ''

