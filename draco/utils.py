import json
import re
import pandas as pd

REGEX = r"(\w+)\(([\w\.\-\_\/]+)(,([\w\.]+))?\)"

def asp_to_vl(facts):
    """given a list of asp facts, generate a VL spec """
    mark = ""
    encodings = {}

    for value in facts:
        cleanded_value = value.replace("\"", "")
        neg_symbol = value.strip().startswith(":-")
        matches = re.search(REGEX, cleanded_value)

        predicate, first, _, second = list(matches.groups())

        if predicate == "mark":
            mark = first
        elif predicate == "data":
            url = first
        elif predicate != "soft":
            if first not in encodings:
                encodings[first] = {}
            encodings[first][predicate] = second or (not neg_symbol)

    encoding = {}
    for e in encodings:
        enc = encodings[e]

        # if quantitative encoding and zero is not set, set zero to false
        if (enc["type"] == 'quantitative') and ("zero" not in enc) and ("bin" not in enc):
            enc["zero"] = False

        scale = {}
        if "log" in enc and enc["log"]:
            scale["type"] = "log"

        ## Do not process zero, just left them for vl engine
        # if "zero" in enc:
        #     scale["zero"] = True if enc["zero"] else False
        if "zero" in enc and enc["zero"] is False:
            scale["zero"] = False

        encoding[enc["channel"]] = { "type": enc["type"]}

        if "aggregate" in enc:
            encoding[enc["channel"]]["aggregate"] = enc["aggregate"]
        if "field" in enc:
            encoding[enc["channel"]]["field"] = enc["field"]
        if "stack" in enc:
            encoding[enc["channel"]]["stack"] = enc["stack"]
        if "bin" in enc:
            encoding[enc["channel"]]["bin"] = True if int(enc["bin"]) == 10 else {"maxbins": int(enc["bin"])}
        if scale and enc["channel"] not in ["row", "column"]:
            encoding[enc["channel"]]["scale"] = scale

    spec = {
        "$schema": 'https://vega.github.io/schema/vega-lite/v4.json',
        "data": { "url": url },
        "mark": mark,
        "encoding": encoding
    }

    if mark == "arc" and "theta" in encoding:
        spec["title"] = encoding["theta"]["field"]

    return spec

def cql_to_asp(spec):
    """given a compass query,
       return an ASP program to describe its property """

    facts = []

    if "mark" in spec:
        facts.append("mark({}).".format(spec["mark"]))

    if 'data' in spec and 'url' in spec["data"]:
        facts.append('data("{}").'.format(spec["data"]["url"]))

    for i, enc in enumerate(spec["encodings"]):
        eid = f"e{i}"
        facts.append(f"encoding({eid}).")

        enc_field_type = None
        enc_zero = None
        enc_binned = None

        for f in enc:
            content = enc[f]
            if not content: continue

            if f == "type":
                enc_field_type = content
            if f == "bin":
                enc_binned = content
            
            # start adding facts to the asp program
            if f == 'scale': 
                # translate two boolean fields
                if 'zero' in content:
                    enc_zero = content["zero"]
                    if content["zero"]:
                        facts.append("zero({}).".format(eid))
                    else:
                        facts.append(":- zero({}).".format(eid))
                if 'log' in content:
                    if content["log"]:
                        facts.append("log({}).".format(eid))
                    else:
                        facts.append(":-log({}).".format(eid))
            elif f == 'bin':
                if isinstance(content, dict) and "maxbins" in content:
                    facts.append("{}({},{}).".format(f, eid, content["maxbins"]))
                elif content:
                    facts.append(":- not bin({},_).".format(eid))
                else:
                    facts.append(":- bin({},_).".format(eid))
            elif f == 'field':
                # fields can have spaces and start with capital letters
                facts.append("{}({},\"{}\").".format(f, eid, content))
            else:
                # translate normal fields
                if f != 'bin':
                  facts.append("{}({},{}).".format(f, eid, content))
        
        #if enc_field_type == 'quantitative' and not enc_zero and not enc_binned:
        #  facts.append("zero({}).".format(eid))

    return facts


def data_to_asp(json_data, fine_types=None):
    """Given json_data, return an ASP program to describe its property """

    def dtype_to_field_type(ty):
        if ty in ["float64", "int64"]: 
            return "number"
        elif ty in ["bool"]:
            return "boolean"
        elif ty in ["object"]: 
            return "string"
        else:
            print("ERROR :: {}".format(ty))
            import sys
            sys.exit(-1)

    df = pd.DataFrame(json_data)

    facts = []
    facts.append("num_rows({}).".format(df.shape[0]))
    
    for i, col in enumerate(df.columns):
        cardinality = pd.Series.nunique(df[col])
        data_type = dtype_to_field_type(df[col].dtype)

        # update datetime field with fine_type information
        if fine_types is not None and fine_types[i].startswith("TEMPORAL"):
            data_type = "datetime"

        field_name = '"{}"'.format(col)
        facts.append("fieldtype({},{}).".format(field_name, data_type))
        facts.append("cardinality({},{}).".format(field_name, cardinality))

    return facts


if __name__ == '__main__':
    asp_props = ['data("data/cars.csv").', 'zero(e0).', 'field(e0,"yield").', 
                'field(e1,"variety").', 'type(e0,quantitative).', 'type(e1,nominal).', 
                'bin(e0,10).', 'aggregate(4,count).', 'aggregate(5,median).', 'field(5,"year").', 
                'channel(e0,row).', 'channel(e1,y).', 'channel(4,x).', 'channel(5,color).', 
                'type(4,quantitative).', 'type(5,quantitative).', 'zero(4).', 'zero(5).', 'mark(point).']
    print(json.dumps(asp_to_vl(asp_props)))

    cql_object = {'data': {'url': 'data/cars.csv'}, 'encodings': [{'field': 'yield', 'type': 'quantitative'}, {'field': 'variety', 'type': 'nominal'}]}
    print(cql_to_asp(cql_object))

    data = [{'yield': 27.0, 'variety': 'Manchuria', 'year': 1931, 'site': 'University Farm'}, {'yield': 48.86667, 'variety': 'Manchuria', 'year': 1931, 'site': 'Waseca'}, {'yield': 27.43334, 'variety': 'Manchuria', 'year': 1931, 'site': 'Morris'}, {'yield': 39.93333, 'variety': 'Manchuria', 'year': 1931, 'site': 'Crookston'}, {'yield': 32.96667, 'variety': 'Manchuria', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 28.96667, 'variety': 'Manchuria', 'year': 1931, 'site': 'Duluth'}, {'yield': 43.06666, 'variety': 'Glabron', 'year': 1931, 'site': 'University Farm'}, {'yield': 55.2, 'variety': 'Glabron', 'year': 1931, 'site': 'Waseca'}, {'yield': 28.76667, 'variety': 'Glabron', 'year': 1931, 'site': 'Morris'}, {'yield': 38.13333, 'variety': 'Glabron', 'year': 1931, 'site': 'Crookston'}, {'yield': 29.13333, 'variety': 'Glabron', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 29.66667, 'variety': 'Glabron', 'year': 1931, 'site': 'Duluth'}, {'yield': 35.13333, 'variety': 'Svansota', 'year': 1931, 'site': 'University Farm'}, {'yield': 47.33333, 'variety': 'Svansota', 'year': 1931, 'site': 'Waseca'}, {'yield': 25.76667, 'variety': 'Svansota', 'year': 1931, 'site': 'Morris'}, {'yield': 40.46667, 'variety': 'Svansota', 'year': 1931, 'site': 'Crookston'}, {'yield': 29.66667, 'variety': 'Svansota', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 25.7, 'variety': 'Svansota', 'year': 1931, 'site': 'Duluth'}, {'yield': 39.9, 'variety': 'Velvet', 'year': 1931, 'site': 'University Farm'}, {'yield': 50.23333, 'variety': 'Velvet', 'year': 1931, 'site': 'Waseca'}, {'yield': 26.13333, 'variety': 'Velvet', 'year': 1931, 'site': 'Morris'}, {'yield': 41.33333, 'variety': 'Velvet', 'year': 1931, 'site': 'Crookston'}, {'yield': 23.03333, 'variety': 'Velvet', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 26.3, 'variety': 'Velvet', 'year': 1931, 'site': 'Duluth'}, {'yield': 36.56666, 'variety': 'Trebi', 'year': 1931, 'site': 'University Farm'}, {'yield': 63.8333, 'variety': 'Trebi', 'year': 1931, 'site': 'Waseca'}, {'yield': 43.76667, 'variety': 'Trebi', 'year': 1931, 'site': 'Morris'}, {'yield': 46.93333, 'variety': 'Trebi', 'year': 1931, 'site': 'Crookston'}, {'yield': 29.76667, 'variety': 'Trebi', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 33.93333, 'variety': 'Trebi', 'year': 1931, 'site': 'Duluth'}, {'yield': 43.26667, 'variety': 'No. 457', 'year': 1931, 'site': 'University Farm'}, {'yield': 58.1, 'variety': 'No. 457', 'year': 1931, 'site': 'Waseca'}, {'yield': 28.7, 'variety': 'No. 457', 'year': 1931, 'site': 'Morris'}, {'yield': 45.66667, 'variety': 'No. 457', 'year': 1931, 'site': 'Crookston'}, {'yield': 32.16667, 'variety': 'No. 457', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 33.6, 'variety': 'No. 457', 'year': 1931, 'site': 'Duluth'}, {'yield': 36.6, 'variety': 'No. 462', 'year': 1931, 'site': 'University Farm'}, {'yield': 65.7667, 'variety': 'No. 462', 'year': 1931, 'site': 'Waseca'}, {'yield': 30.36667, 'variety': 'No. 462', 'year': 1931, 'site': 'Morris'}, {'yield': 48.56666, 'variety': 'No. 462', 'year': 1931, 'site': 'Crookston'}, {'yield': 24.93334, 'variety': 'No. 462', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 28.1, 'variety': 'No. 462', 'year': 1931, 'site': 'Duluth'}, {'yield': 32.76667, 'variety': 'Peatland', 'year': 1931, 'site': 'University Farm'}, {'yield': 48.56666, 'variety': 'Peatland', 'year': 1931, 'site': 'Waseca'}, {'yield': 29.86667, 'variety': 'Peatland', 'year': 1931, 'site': 'Morris'}, {'yield': 41.6, 'variety': 'Peatland', 'year': 1931, 'site': 'Crookston'}, {'yield': 34.7, 'variety': 'Peatland', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 32.0, 'variety': 'Peatland', 'year': 1931, 'site': 'Duluth'}, {'yield': 24.66667, 'variety': 'No. 475', 'year': 1931, 'site': 'University Farm'}, {'yield': 46.76667, 'variety': 'No. 475', 'year': 1931, 'site': 'Waseca'}, {'yield': 22.6, 'variety': 'No. 475', 'year': 1931, 'site': 'Morris'}, {'yield': 44.1, 'variety': 'No. 475', 'year': 1931, 'site': 'Crookston'}, {'yield': 19.7, 'variety': 'No. 475', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 33.06666, 'variety': 'No. 475', 'year': 1931, 'site': 'Duluth'}, {'yield': 39.3, 'variety': 'Wisconsin No. 38', 'year': 1931, 'site': 'University Farm'}, {'yield': 58.8, 'variety': 'Wisconsin No. 38', 'year': 1931, 'site': 'Waseca'}, {'yield': 29.46667, 'variety': 'Wisconsin No. 38', 'year': 1931, 'site': 'Morris'}, {'yield': 49.86667, 'variety': 'Wisconsin No. 38', 'year': 1931, 'site': 'Crookston'}, {'yield': 34.46667, 'variety': 'Wisconsin No. 38', 'year': 1931, 'site': 'Grand Rapids'}, {'yield': 31.6, 'variety': 'Wisconsin No. 38', 'year': 1931, 'site': 'Duluth'}, {'yield': 26.9, 'variety': 'Manchuria', 'year': 1932, 'site': 'University Farm'}, {'yield': 33.46667, 'variety': 'Manchuria', 'year': 1932, 'site': 'Waseca'}, {'yield': 34.36666, 'variety': 'Manchuria', 'year': 1932, 'site': 'Morris'}, {'yield': 32.96667, 'variety': 'Manchuria', 'year': 1932, 'site': 'Crookston'}, {'yield': 22.13333, 'variety': 'Manchuria', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 22.56667, 'variety': 'Manchuria', 'year': 1932, 'site': 'Duluth'}, {'yield': 36.8, 'variety': 'Glabron', 'year': 1932, 'site': 'University Farm'}, {'yield': 37.73333, 'variety': 'Glabron', 'year': 1932, 'site': 'Waseca'}, {'yield': 35.13333, 'variety': 'Glabron', 'year': 1932, 'site': 'Morris'}, {'yield': 26.16667, 'variety': 'Glabron', 'year': 1932, 'site': 'Crookston'}, {'yield': 14.43333, 'variety': 'Glabron', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 25.86667, 'variety': 'Glabron', 'year': 1932, 'site': 'Duluth'}, {'yield': 27.43334, 'variety': 'Svansota', 'year': 1932, 'site': 'University Farm'}, {'yield': 38.5, 'variety': 'Svansota', 'year': 1932, 'site': 'Waseca'}, {'yield': 35.03333, 'variety': 'Svansota', 'year': 1932, 'site': 'Morris'}, {'yield': 20.63333, 'variety': 'Svansota', 'year': 1932, 'site': 'Crookston'}, {'yield': 16.63333, 'variety': 'Svansota', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 22.23333, 'variety': 'Svansota', 'year': 1932, 'site': 'Duluth'}, {'yield': 26.8, 'variety': 'Velvet', 'year': 1932, 'site': 'University Farm'}, {'yield': 37.4, 'variety': 'Velvet', 'year': 1932, 'site': 'Waseca'}, {'yield': 38.83333, 'variety': 'Velvet', 'year': 1932, 'site': 'Morris'}, {'yield': 32.06666, 'variety': 'Velvet', 'year': 1932, 'site': 'Crookston'}, {'yield': 32.23333, 'variety': 'Velvet', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 22.46667, 'variety': 'Velvet', 'year': 1932, 'site': 'Duluth'}, {'yield': 29.06667, 'variety': 'Trebi', 'year': 1932, 'site': 'University Farm'}, {'yield': 49.2333, 'variety': 'Trebi', 'year': 1932, 'site': 'Waseca'}, {'yield': 46.63333, 'variety': 'Trebi', 'year': 1932, 'site': 'Morris'}, {'yield': 41.83333, 'variety': 'Trebi', 'year': 1932, 'site': 'Crookston'}, {'yield': 20.63333, 'variety': 'Trebi', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 30.6, 'variety': 'Trebi', 'year': 1932, 'site': 'Duluth'}, {'yield': 26.43334, 'variety': 'No. 457', 'year': 1932, 'site': 'University Farm'}, {'yield': 42.2, 'variety': 'No. 457', 'year': 1932, 'site': 'Waseca'}, {'yield': 43.53334, 'variety': 'No. 457', 'year': 1932, 'site': 'Morris'}, {'yield': 34.33333, 'variety': 'No. 457', 'year': 1932, 'site': 'Crookston'}, {'yield': 19.46667, 'variety': 'No. 457', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 22.7, 'variety': 'No. 457', 'year': 1932, 'site': 'Duluth'}, {'yield': 25.56667, 'variety': 'No. 462', 'year': 1932, 'site': 'University Farm'}, {'yield': 44.7, 'variety': 'No. 462', 'year': 1932, 'site': 'Waseca'}, {'yield': 47.0, 'variety': 'No. 462', 'year': 1932, 'site': 'Morris'}, {'yield': 30.53333, 'variety': 'No. 462', 'year': 1932, 'site': 'Crookston'}, {'yield': 19.9, 'variety': 'No. 462', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 22.5, 'variety': 'No. 462', 'year': 1932, 'site': 'Duluth'}, {'yield': 28.06667, 'variety': 'Peatland', 'year': 1932, 'site': 'University Farm'}, {'yield': 36.03333, 'variety': 'Peatland', 'year': 1932, 'site': 'Waseca'}, {'yield': 43.2, 'variety': 'Peatland', 'year': 1932, 'site': 'Morris'}, {'yield': 25.23333, 'variety': 'Peatland', 'year': 1932, 'site': 'Crookston'}, {'yield': 26.76667, 'variety': 'Peatland', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 31.36667, 'variety': 'Peatland', 'year': 1932, 'site': 'Duluth'}, {'yield': 30.0, 'variety': 'No. 475', 'year': 1932, 'site': 'University Farm'}, {'yield': 41.26667, 'variety': 'No. 475', 'year': 1932, 'site': 'Waseca'}, {'yield': 44.23333, 'variety': 'No. 475', 'year': 1932, 'site': 'Morris'}, {'yield': 32.13333, 'variety': 'No. 475', 'year': 1932, 'site': 'Crookston'}, {'yield': 15.23333, 'variety': 'No. 475', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 27.36667, 'variety': 'No. 475', 'year': 1932, 'site': 'Duluth'}, {'yield': 38.0, 'variety': 'Wisconsin No. 38', 'year': 1932, 'site': 'University Farm'}, {'yield': 58.16667, 'variety': 'Wisconsin No. 38', 'year': 1932, 'site': 'Waseca'}, {'yield': 47.16667, 'variety': 'Wisconsin No. 38', 'year': 1932, 'site': 'Morris'}, {'yield': 35.9, 'variety': 'Wisconsin No. 38', 'year': 1932, 'site': 'Crookston'}, {'yield': 20.66667, 'variety': 'Wisconsin No. 38', 'year': 1932, 'site': 'Grand Rapids'}, {'yield': 29.33333, 'variety': 'Wisconsin No. 38', 'year': 1932, 'site': 'Duluth'}]
    print(data_to_asp(data))