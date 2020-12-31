import pyTigerGraph as tg

import argparse

import TGSchema as tgs
import loaders

def main(args):
    conn = tg.TigerGraphConnection(host=args.hostname,
                                   gsqlVersion=args.gsqlVersion,
                                   username=args.username,
                                   password=args.password,
                                   restppPort=args.restppPort,
                                   gsPort=args.gsqlPort,
                                   apiToken=args.apiToken,
                                   useCert=args.useCert,
                                   certPath=args.certPath
                                   )
    if args.drop or args.all:
        print("======== DROPPING ALL DATA ========")
        confirm = input("Confirm Dropping Data [Y/n]: ")
        if confirm == "Y":
            print(conn.gsql('''DROP ALL''', options=[]))
        else:
            print("Not dropping data, aborting.")
            exit()
    if args.createSchema or args.all:
        print("======== CREATING SCHEMA ========")
        if isinstance(args.createSchema, str):
            sch = tgs.TGSchema(conn, args.graphname, args.createSchema)
        else:
            sch = tgs.TGSchema(conn, args.graphname, "./gsql/schema.gsql")
        out = sch.createSchema()
        print(out)
    print("======== LOADING DATA ========")
    ldrs = [x for x in dir(loaders) if "__" not in x]
    for ldr in ldrs:
        obj = getattr(args, ldr)
        if obj != None and obj[0] != []:
            print("Running "+ldr)
            params = {}
            for i in range(len(obj[0])):
                params["file"+str(i+1)] = obj[0][i]
            try:
                getattr(loaders, ldr).load(**params)
            except:
                print("FAIL: Invalid arguments for "+ldr)
        elif args.loadAllData or args.all or obj == [[]]: # if loading job is specified but no filename is given, the object is nested empty lists.
            print("Running "+ldr)
            getattr(loaders, ldr).load()
        else:
            pass

if __name__ == "__main__":
    # host="http://localhost", graphname="MyGraph", username="tigergraph", password="tigergraph", restppPort="9000", gsPort="14240", apiToken="", gsqlVersion="", useCert=False, certPath=None
    
    ldrs = [x for x in dir(loaders) if "__" not in x]

    parser = argparse.ArgumentParser(description="Synthea TigerGraph Loader")
    tgConfig = parser.add_argument_group("TigerGraph Configuration")
    tArgs = parser.add_argument_group("Available Tasks")

    tgConfig.add_argument("--hostname", "-hn", type=str, default="http://localhost", help="Where is your TigerGraph Instance Hosted?")
    tgConfig.add_argument("--gsqlVersion", "-gsv", type=str, default="3.0.0", help="What version of GSQL are you running?")
    tgConfig.add_argument("--username", "-u", type=str, default="tigergraph", help="What is your TigerGraph username?")
    tgConfig.add_argument("--password", "-p", type=str, default="tigergraph", help="What is your TigerGraph password?")
    tgConfig.add_argument("--restppPort", "-rp", type=str, default="9000", help="What port is the REST++ interface available?")
    tgConfig.add_argument("--gsqlPort", "-gp", type=str, default="14240", help="What port is the GSQL interface available?")
    tgConfig.add_argument("--apiToken", "-t", type=str, default="", help="Do you have an API Token?")
    tgConfig.add_argument("--useCert", "-uc", type=bool, default=False, help="Do you need to use a SSL certificate (True for TG Cloud users)")
    tgConfig.add_argument("--certPath", "-cp", type=str, default="", help="Path to SSL certificate")
    tgConfig.add_argument("--graphname", "-gn", type=str, default="MyGraph", help="What do you want to name your graph?")

    tArgs.add_argument("--all", "-a", nargs="?", type=bool, const=True, help="Runs all tasks")
    tArgs.add_argument("--createSchema", "-cs", nargs="?", const=True, help="Creates Schema, optionally takes path to schema file")
    tArgs.add_argument("--drop", "-d", nargs="?", const=True, help="Drops all data from graph")
    tArgs.add_argument("--loadAllData", "-ld", nargs="?", const=True, help="Loads All Data")
    
    for ldr in ldrs:
        tArgs.add_argument("--"+ldr, nargs="*", action="append", help="Specify file paths [file1, file2, ...]")

    args = parser.parse_args()

    main(args)