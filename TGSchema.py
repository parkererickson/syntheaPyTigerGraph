class TGSchema(object):
    def __init__(self, conn, graphname, schemaPath):
        self.conn = conn
        self.graphname = graphname
        self.schemaPath = schemaPath
    def createSchema(self):
        with open(self.schemaPath, 'r') as fp:
            schemaDef = fp.read()
        schemaDef = schemaDef.replace('@graphname@', self.graphname)
        res = self.conn.gsql(schemaDef, options=[])
        return res