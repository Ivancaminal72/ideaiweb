import sys
import os
import csv
import warnings
from pybtex.database.input import bibtex
import pandas as pd
from Projects import parse_bibtex
from collections import Counter

month_dict2 = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

def merge_id_key(data, path):
    dataForm = pd.read_csv(path)
    dataForm.insert(0, 'Key', '00000000')
    for i, pForm in dataForm.iterrows():
        found=False
        patent=False
        print("New project (year:",pForm["Year"],") searching for Key...")
        cur_key = ""
        for pBib in data:
            cur_key = str(pBib["Key"])
            try:
                if str(pBib["Year"]) == str(pForm["Year"]):
                    # print("Id:", pForm["Id"])
                    # print("Key:", pBib["Key"])
                    # print("Form:", pForm["Month"])
                    # print("Bib:", pBib["Month"])
                    # print("Form2:", month_dict2[pForm["Month"]])
                    if str(pBib["Month"]) == str(month_dict2[pForm["Month"].replace(" ", "")]):
                        if str(pBib["Title"]).replace(" ", "") == str(pForm["Title"]).replace(" ", ""):
                            aForm = Counter(str(pForm["Authors"]).replace(" ", ""))
                            aBib = Counter(str(pBib["Authors"]).replace(" ", ""))
                            if aForm == aBib:
                                dataForm.at[i, 'Key'] = pBib["Key"]
                                found = True
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

            except KeyError as ex:
                if ex.args[0] == '0':
                    warnings.warn("Ignoring patent")
                    patent=True
                    break
                else:
                    warnings.warn("Key " + str(pBib["Key"]) + " is missing field " + ex.args[0])
                continue

        if found:
            continue
        elif patent:
            continue
        else: #not found
            print("Not found "+ cur_key + ", trying to match ignoring Title...")

            for pBib in data:
                try:
                    if str(pBib["Year"]) == str(pForm["Year"]):
                        if str(pBib["Month"]) == str(month_dict2[pForm["Month"].replace(" ", "")]):
                            aForm = Counter(str(pForm["Authors"]).replace(" ", ""))
                            aBib = Counter(str(pBib["Authors"]).replace(" ", ""))
                            if aForm == aBib:
                                dataForm.at[i, 'Key'] = pBib["Key"]
                                found = True
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue

                except KeyError as ex:
                    if ex.args[0] == '0':
                        break
                    else:
                        warnings.warn("Key " + str(pBib["Key"]) + " is missing field " + ex.args[0])
                    continue

            if found:
                print("    OK! Found ignoring Title")
                continue
            else:
                print("Not found " + cur_key + ", trying to match ignoring Authors...")

                for pBib in data:
                    try:
                        if str(pBib["Year"]) == str(pForm["Year"]):
                            if str(pBib["Month"]) == str(month_dict2[pForm["Month"].replace(" ", "")]):
                                if str(pBib["Title"]).replace(" ", "") == str(pForm["Title"]).replace(" ", ""):
                                    dataForm.at[i, 'Key'] = pBib["Key"]
                                    found = True
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue

                    except KeyError as ex:
                        if ex.args[0] == '0':
                            break
                        else:
                            warnings.warn("Key " + str(pBib["Key"]) + " is missing field " + ex.args[0])
                        continue

                if found:
                    print("\n    ## WARNING ##    OK! Found ignoring Authors\n")
                    continue
                else:
                    warnings.warn("Not found ID: " + str(pForm["Id"]))
                    continue

    return dataForm

if __name__ == "__main__":

    path_non_competitive = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v1/originals/NoCompetitius.bib"
    path_competitive = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v1/originals/Competitius.bib"
    path_form_original = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v2/form_original.csv"
    path_form = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v2/form.csv"

    data_nc = parse_bibtex(path_non_competitive, "non-competitive")
    data_c  = parse_bibtex(path_competitive, "competitive")

    data = data_nc + data_c
    data = sorted(data, key=lambda k: k['Year'], reverse=True)

    df = merge_id_key(data, path_form_original)

    df.to_csv(path_form, index=False)



