import pandas as pd
from biothings_client import get_client
import argparse

def convert_list(ens):
    """
    Accepts a list of Ensembl GeneId strings
    Returns a pandas dataframe including the queried data, 
    the symbol and the gene name.
    """

    mg = get_client('gene')
    ginfo = mg.querymany(ens, scopes='ensembl.gene')

    out = {
        "query": [],
        "symbol": [],
        "name": []
    }
    keys = out.keys()
    print(keys)

    for g in ginfo:
        # print("symbol:", g["symbol"], "name:", g["name"])
        for key in keys:

            try:
                out[key].append(g[key])
            except:
                out[key].append("void")

    df_all = pd.DataFrame(out)
    return df_all


def main(fname_in: str, fname_out: str):

    # allow the possibility for excel files.
    # consider first column only
    if fname_in.endswith('.xlsx'):
        ens = pd.read_excel(fname_in,header=0)
        ens = list(ens.iloc[:,0])

    else:    
        # reads the input by line
        with open(fname_in) as f:
            ens_el = f.readlines()

        # trims new line character
        ens = list(map(lambda x: x[:-1], ens_el))

        print(len(ens))
    # ens_l = [el for el in ens]
    # print(ens.columns)
    df_all = convert_list(ens)
    df_all.to_csv(fname_out)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("fname",
                        help="input file name (1 column GeneID data)")
    parser.add_argument("--out",
                        help="output file name (inferred by input file by default)",
                        default=-1)

    args = parser.parse_args()
    print(args.fname)

    if args.out == -1:
        outfname = args.fname + "_names.csv"
    else:
        outfname = args.output

    main(args.fname, outfname)

    

    
