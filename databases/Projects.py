import sys
import os
import csv
import warnings
from pybtex.database.input import bibtex
import pandas as pd
import codecs

month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

def parse_bibtex(path, type):
    #open a bibtex file
    parser = bibtex.Parser()
    bibdata = parser.parse_file(path)

    data = []

    #loop through the individual references
    for bib_id in bibdata.entries:
        row = {}
        fields = bibdata.entries[bib_id].fields
        try:
            row["Key"] = bibdata.entries[bib_id].key
            row["Year"] = fields["year"]
            row["Month"] = month_dict[fields["month"]]
            row["Type"] = type
            for idx, author in enumerate(bibdata.entries[bib_id].persons["author"]):
                name = author.bibtex_first_names
                surename = author.last_names
                if idx == 0:
                    row["PAuthors"] = surename[0] + ", " + name[0]
                    row["Authors"] = surename[0] + ", " + name[0]
                elif idx == 1:
                    row["SAuthors"] = surename[0] + ", " + name[0]
                    row["Authors"] = row["Authors"] + "; " + surename[0] + ", " + name[0]
                else:
                    row["SAuthors"] = row["SAuthors"] + "; " + surename[0] + ", " + name[0]
                    row["Authors"] = row["Authors"] + "; " + surename[0] + ", " + name[0]
            row["Title"] = fields["title"]

        except KeyError as ex:
            warnings.warn("Key "+str(bibdata.entries[bib_id].key)+" is missing filed "+ex.args[0])
            continue

        try:
            y_data = fields["date"][:4]
            if y_data != row["Year"]:
                warnings.warn("Starting year do not match in fields Date and Year, keeping minimum as valid")
                row["Year"] = min(y_data, row["Year"])
            row["EndYear"] = fields["date"][5:9]
        except KeyError:
            pass

        try:
            row["Url"] = fields["url"]

        except KeyError:
            pass

        data.append(row)

    return data


def merge_form_information(d_bib, path):
    d_form = pd.read_csv(path, index_col=0)
    final_data = []
    for p_bib in d_bib:

        # print("Loading project", p_bib["Key"], "...")

        #Initialize fields
        final_proj = dict()
        final_proj["Id"] = ""
        final_proj["Year"] = ""
        final_proj["Month"] = ""
        final_proj["Type"] = ""
        final_proj["PAuthors"] = ""
        final_proj["SAuthors"] = ""
        final_proj["Authors"] = ""
        final_proj["Title"] = ""
        final_proj["PArea"] = ""
        final_proj["SAreas"] = ""
        final_proj["Collaborators"] = ""
        final_proj["Url"] = ""
        final_proj["Summary"] = ""
        final_proj["Key"] = ""
        final_proj["EndYear"] = ""


        try:
            final_proj["Key"] = p_bib["Key"]
            final_proj["Year"] = p_bib["Year"]
            final_proj["Month"] = p_bib["Month"]
            final_proj["Type"] = p_bib["Type"]
        except KeyError as ex:
            warnings.warn("Missing basic field: " + ex.args[0]+" --> "+str(p_bib["Key"]))
            continue

        try:
            final_proj["EndYear"] = p_bib["EndYear"]
        except KeyError:
            pass

        try:
            final_proj["Id"] = d_form.at[int(p_bib["Key"]), "Id"]
        except KeyError as ex:
            final_proj["Id"] = ""
            print("Ignore", ex.args[0])
            continue

        print("Merging "+ str(p_bib["Key"]))

        PAuthors = ""
        Authors = ""
        Title = ""
        PArea = ""

        try:
            PAuthors = str(d_form.at[int(p_bib["Key"]), "PAuthors"])
            Authors = str(d_form.at[int(p_bib["Key"]), "Authors"])
            Title = str(d_form.at[int(p_bib["Key"]), "Title"])
            PArea = str(d_form.at[int(p_bib["Key"]), "PArea"])

        except KeyError as ex:
            warnings.warn("Missing basic additional form field: " + ex.args[0] + " --> " + str(p_bib["Key"]))
            pass

        if PAuthors != "":
            try:
                if str(p_bib["PAuthors"]).replace(" ", "") != PAuthors.replace(" ", ""):
                    final_proj["PAuthors"] = PAuthors
                else:
                    final_proj["PAuthors"] = p_bib["PAuthors"]
                if str(p_bib["Authors"]).replace(" ", "") != Authors.replace(" ", ""):
                    final_proj["Authors"] = Authors
                    warnings.warn("Different Authors --> "+str(p_bib["Key"]))
                else:
                    final_proj["Authors"] = p_bib["Authors"]
            except KeyError as ex:
                warnings.warn("Missing basic field: " + ex.args[0]+" --> "+str(p_bib["Key"]))
                continue

        try:
            final_proj["SAuthors"] = p_bib["SAuthors"]
        except KeyError:
            pass

        try:
            final_proj["SAuthors"] = str(d_form.at[int(p_bib["Key"]), "SAuthors"])
        except KeyError:
            pass

        if Title != "":
            try:
                if str(p_bib["Title"]).replace(" ", "") != Title.replace(" ", ""):
                    final_proj["Title"] = Title
                else:
                    final_proj["Title"] = p_bib["Title"]
            except KeyError as ex:
                warnings.warn("Missing basic field: " + ex.args[0]+" --> "+str(p_bib["Key"]))
                continue

        if PArea != "":
            final_proj["PArea"] = PArea
        else:
            try:
                final_proj["PArea"] = p_bib["PArea"]
            except KeyError:
                pass

        try:
            final_proj["SAreas"] = p_bib["SAreas"]
        except KeyError:
            pass

        try:
            if "SAreas" in final_proj:
                final_proj["SAreas"] = str(d_form.at[int(p_bib["Key"]), "SAreas"])
        except KeyError:
            pass

        try:
            final_proj["Collaborators"] = p_bib["Collaborators"]
        except KeyError:
            pass

        try:
            final_proj["Collaborators"] = str(d_form.at[int(p_bib["Key"]), "Collaborators"])
        except KeyError:
            pass

        try:
            final_proj["Url"] = p_bib["Url"]
        except KeyError:
            pass

        try:
            final_proj["Url"] = str(d_form.at[int(p_bib["Key"]), "Url"])
        except KeyError:
            pass

        try:
            final_proj["Summary"] = p_bib["Summary"]
        except KeyError:
            pass

        try:
            final_proj["Summary"] = str(d_form.at[int(p_bib["Key"]), "Summary"])
        except KeyError:
            pass

        final_data.append(final_proj)

    return final_data

def export_data_csv(final_data, out_path):
    with codecs.open(out_path, "w", encoding="utf-8") as outfile:
        fp = csv.DictWriter(outfile, final_data[0].keys())
        fp.writeheader()
        fp.writerows(final_data)

if __name__ == "__main__":

    path_non_competitive = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v2/originals/2019-06-07_NoCompetitius.bib"
    path_competitive = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v2/originals/2019-06-07_Competitius.bib"
    path_form = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v2/form.csv"
    path_out = "C:/Users/Ivan/OneDrive/1-Work/2-ideai/databases/Projects_v2/PAP.csv"

    data_nc = parse_bibtex(path_non_competitive, "non-competitive")
    data_c  = parse_bibtex(path_competitive, "competitive")

    data = data_nc + data_c
    data = sorted(data, key=lambda k: k['Year'], reverse=True)

    data = merge_form_information(data, path_form)
    data = sorted(data, key=lambda k: int(k['Year'])*100+k['Month'], reverse=True)

    # df = pd.DataFrame(data)
    # df.to_csv(path_out)

    export_data_csv(data, path_out)



