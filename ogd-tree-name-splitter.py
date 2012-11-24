# -*- coding: utf-8 -*-

# Processing of the shapefile was not possible due to
# problems with the pyshp-module and also OGR. Therefore
# the CSV-file is used.

# This script takes the OGD-CSV BAUMOGD.csv file as input
# and transforms it to an OSM-compatible shapefile
#    !! The original CSV-file has to be edited -> there are some
#       values that belong togeter, but are separated by a comma (",").
#       The script will detect these as separate values, which is wrong.

import csv
import re
import datetime

infile = "csv/BAUMOGD_edited.csv"
outfile = "csv/out2.csv"

def extractGeometry(row):
    '''convert the geometry from the CSV to an geometry-array'''
    geo = str(row[1])
    splitGeo = geo.split()
    x = splitGeo[1][1:]
    y = splitGeo[2]
    y = y[:len(y)-1]
    return [float(x),float(y)]

def setTtype(genus):
    '''setze den TYPE abhängig vom genus'''
    ttype = ""
    if genus == "": ttype = ""
    if genus == "abies": ttype = "conifer"
    if genus == "acer": ttype = "broad_leaved"
    if genus == "aesculus": ttype = "broad_leaved"
    if genus == "ailanthus": ttype = "broad_leaved"
    if genus == "albizia": ttype = "broad_leaved"
    if genus == "alnus": ttype = "broad_leaved"
    if genus == "amelanchier": ttype = "broad_leaved"
    if genus == "araucaria": ttype = "conifer"
    if genus == "baumgruppe": ttype = ""
    if genus == "betula": ttype = "broad_leaved"
    if genus == "broussonetia": ttype = "broad_leaved"
    if genus == "buxus": ttype = "broad_leaved"
    if genus == "calocedrus": ttype = "conifer"
    if genus == "caragana": ttype = "broad_leaved"
    if genus == "carpinus": ttype = "broad_leaved"
    if genus == "castanea": ttype = "broad_leaved"
    if genus == "catalpa": ttype = "broad_leaved"
    if genus == "cedrus": ttype = "conifer"
    if genus == "celtis": ttype = "broad_leaved"
    if genus == "cercidiphyllum": ttype = "broad_leaved"
    if genus == "cercis": ttype = "broad_leaved"
    if genus == "chamaecyparis": ttype = "conifer"
    if genus == "cladrastis": ttype = "broad_leaved"
    if genus == "cornus": ttype = "broad_leaved"
    if genus == "corylus": ttype = "broad_leaved"
    if genus == "cotinus": ttype = "broad_leaved"
    if genus == "cotoneaster": ttype = "broad_leaved"
    if genus == "crataegus": ttype = "broad_leaved"
    if genus == "cryptomeria": ttype = "conifer"
    if genus == "cupressocyparis": ttype = "conifer"
    if genus == "cupressus": ttype = "conifer"
    if genus == "cydonia": ttype = "broad_leaved"
    if genus == "davidia": ttype = "broad_leaved"
    if genus == "elaeagnus": ttype = "broad_leaved"
    if genus == "eucommia": ttype = "broad_leaved"
    if genus == "exochorda": ttype = "broad_leaved"
    if genus == "fagus": ttype = "broad_leaved"
    if genus == "fontanesia": ttype = "broad_leaved"
    if genus == "frangula": ttype = "broad_leaved"
    if genus == "fraxinus": ttype = "broad_leaved"
    if genus == "ginkgo": ttype = "broad_leaved"
    if genus == "gleditsia": ttype = "broad_leaved"
    if genus == "gymnocladus": ttype = "broad_leaved"
    if genus == "hibiscus": ttype = "broad_leaved"
    if genus == "ilex": ttype = "broad_leaved"
    if genus == "juglans": ttype = "broad_leaved"
    if genus == "juniperus": ttype = "conifer"
    if genus == "koelreuteria": ttype = "broad_leaved"
    if genus == "laburnum": ttype = "broad_leaved"
    if genus == "larix": ttype = "broad_leaved"
    if genus == "liquidambar": ttype = "broad_leaved"
    if genus == "liriodendron": ttype = "broad_leaved"
    if genus == "maclura": ttype = "broad_leaved"
    if genus == "magnolia": ttype = "broad_leaved"
    if genus == "malus": ttype = "broad_leaved"
    if genus == "metasequoia": ttype = "conifer"
    if genus == "morus": ttype = "broad_leaved"
    if genus == "nadelbaum": ttype = "conifer"
    if genus == "ostrya": ttype = "broad_leaved"
    if genus == "parrotia": ttype = "broad_leaved"
    if genus == "paulownia": ttype = "broad_leaved"
    if genus == "phellodendron": ttype = "broad_leaved"
    if genus == "photinia": ttype = "broad_leaved"
    if genus == "picea": ttype = "conifer"
    if genus == "pinus": ttype = "conifer"
    if genus == "platanus": ttype = "broad_leaved"
    if genus == "platycladus": ttype = "conifer"
    if genus == "populus": ttype = "broad_leaved"
    if genus == "prunus": ttype = "broad_leaved"
    if genus == "pseudotsuga": ttype = "conifer"
    if genus == "pterocarya": ttype = "broad_leaved"
    if genus == "pyrus": ttype = "broad_leaved"
    if genus == "quercus": ttype = "broad_leaved"
    if genus == "rhamnus": ttype = "broad_leaved"
    if genus == "rhus": ttype = "broad_leaved"
    if genus == "robinia": ttype = "broad_leaved"
    if genus == "salix": ttype = "broad_leaved"
    if genus == "sambucus": ttype = "broad_leaved"
    if genus == "sequoiadendron": ttype = "conifer"
    if genus == "sophora": ttype = "broad_leaved"
    if genus == "sorbus": ttype = "broad_leaved"
    if genus == "tamarix": ttype = "broad_leaved"
    if genus == "taxus": ttype = "conifer"
    if genus == "tetradium": ttype = "broad_leaved"
    if genus == "thuja": ttype = "conifer"
    if genus == "thujopsis": ttype = "conifer"
    if genus == "tilia": ttype = "broad_leaved"
    if genus == "toona": ttype = "broad_leaved"
    if genus == "tsuga": ttype = "conifer"
    if genus == "ulmus": ttype = "broad_leaved"
    if genus == "zelkova": ttype = "broad_leaved"
    
    return ttype
    
def uniq(inlist): 
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques

def detectGenus(species):
    '''finde GENUS'''
    if species == "":
        genus = ""
    elif species == " ":
        genus = ""
    else:
        genus = species.split()[0]
        
    genus = genus.strip()
    if genus == "unbekannt": genus = ""
    if genus.lower() == "nadelbaum": genus = ""
    if genus.lower() == "eucommina": genus = "Eucommia"
    if genus.lower() == "eleagnus": genus = "Elaeagnus"
    
    return genus

def detectSpecies(stri):
    '''finde die SPECIES'''
    firstindex = stri.find("'")
    secondindex = stri.find("(")
    if firstindex > 0:
        species = stri[0:firstindex]
    else:
        if secondindex > 0:
            species = stri[0:secondindex]
        else:
            species = str(stri)
    
    species = species.strip()
    if species.lower() == "eleagnus angustifolia": species = "elaeagnus angustifolia"
    if species.lower() == "unbekannt": species = ""
    if species.lower() == "nadelbaum": species = ""
    return species

def detectHeight(row):
    height = str(row[9])
    
    if height != "":
            if float(height) > 50:
                height = ""
                
    if height == "0" : height = ""
    return height
    
def detectSorte(stri):
    sorte = re.findall('\'([^"]*)\'', stri) # Findet nur single-quotes!
    if sorte:
        sorte = str(sorte[0])
    else:
        sorte = ""
    
    sorte = sorte.strip()
    return sorte
    
def detectDeutsch(stri):
    deutsch = re.findall('\(([^"]*)\)', stri)
    if deutsch:
        deutsch = str(deutsch[0])
    else:
        deutsch = ""
    
    return deutsch
    
def detectCircumference(row):
    circumference = str(row[7])
    if circumference == " ":
        circumference = ""
    elif circumference == "":
        pass
    else:
        circumference = str( float(circumference) / 100.0 ) 
    
    if circumference == "0.0": circumference = ""
    return circumference
    
def detectYear(row):
    year = str(row[6]).strip()
    if year != "":
        if int(year) < 1500:
            year = ""
        elif int(year) > 2012:
            year = ""
    return year

def detectTreeId(row):
    treeid = str(row[2]).strip()
    return treeid
    
def detectWidth(row):
    diameter_crown = str(row[8])
    
    if diameter_crown != "":
        if float(diameter_crown) > 40:
            diameter_crown = ""
            
    if diameter_crown == "0": diameter_crown = ""
    return diameter_crown
    
def setTaxon(species,sorte):
    if sorte:
        taxon = species + " " + sorte
    else:
        taxon = species
            
def makeReplacements(stri):
    stri = stri.replace("kiefer","föhre")
    stri = stri.replace("Kiefer","Föhre")
    return stri
    
def isBaum(genus,height,circumference,width,species,year):
    genus = genus.lower()
    species = species.lower()
    if height == "": height = 20
    height = float(height)
    if circumference == "": circumference = 0.5
    circumference = float(circumference)
    if width == "": width = 7
    width = float(width)
    if year == "": year = 0
    year = int(year)

    if height <= 2 and (int(datetime.datetime.now().year) - year) >= 3 :
        # print "height: " + str(height) + "  " + "age: " + str(int(datetime.datetime.now().year) - year)
        return False
    if genus == "": return True
    if genus == "abies": return True
    if genus == "acer": return True
    if genus == "aesculus": return True
    if genus == "ailanthus": return True
    if genus == "albizia": return True
    if genus == "alnus": return True
    if genus == "amelanchier": return True
    if genus == "araucaria": return True
    if genus == "betula": return True
    if genus == "broussonetia": return True
    if genus == "buxus": return True
    if genus == "calocedrus": return True
    if genus == "caragana": return True
    if genus == "carpinus": return True
    if genus == "castanea": return True
    if genus == "catalpa": return True
    if genus == "cedrus": return True
    if genus == "celtis": return True
    if genus == "cercidiphyllum": return True
    if genus == "cercis": return True
    if genus == "chamaecyparis": return True
    if genus == "cladrastis": return True
    if genus == "cornus": return True
    if genus == "corylus": return True
    if genus == "cotinus": return True
    if genus == "cotoneaster": return True
    if genus == "crataegus": return True
    if genus == "cryptomeria": return True
    if genus == "cupressocyparis": return True
    if genus == "cupressus": return True
    if genus == "cydonia": return True
    if genus == "davidia": return True
    if genus == "elaeagnus": return True
    if genus == "eucommia": return True
    if genus == "exochorda": return True
    if genus == "fagus": return True
    if genus == "fontanesia": return True
    if genus == "frangula": return True
    if genus == "fraxinus": return True
    if genus == "ginkgo": return True
    if genus == "gleditsia": return True
    if genus == "gymnocladus": return True
    if genus == "hibiscus": return True
    if genus == "ilex": return True
    if genus == "juglans": return True
    if genus == "juniperus" and species != "juniperus virginiana" and height <= 3: return False
    if genus == "koelreuteria": return True
    if genus == "laburnum": return True
    if genus == "larix": return True
    if genus == "liquidambar": return True
    if genus == "liriodendron": return True
    if genus == "maclura": return True
    if genus == "magnolia": return True
    if genus == "malus": return True
    if genus == "metasequoia": return True
    if genus == "morus": return True
    if genus == "nadelbaum": return True
    if genus == "ostrya": return True
    if genus == "parrotia": return True
    if genus == "paulownia": return True
    if genus == "phellodendron": return True
    if genus == "photinia": return True
    if genus == "picea": return True
    if genus == "pinus": return True
    if genus == "platanus": return True
    if genus == "platycladus": return True
    if genus == "populus": return True
    if genus == "prunus": return True
    if genus == "pseudotsuga": return True
    if genus == "pterocarya": return True
    if genus == "pyrus": return True
    if genus == "quercus": return True
    if genus == "rhamnus": return True
    if genus == "rhus": return True
    if genus == "robinia": return True
    if genus == "salix": return True
    if genus == "sambucus" and height >= 4: return True
    if genus == "sequoiadendron": return True
    if genus == "sophora": return True
    if genus == "sorbus": return True
    if genus == "tamarix": return True
    if genus == "taxus": return True
    if genus == "tetradium": return True
    if genus == "thuja": return True
    if genus == "thujopsis": return True
    if genus == "tilia": return True
    if genus == "toona": return True
    if genus == "tsuga": return True
    if genus == "ulmus": return True
    if genus == "zelkova": return True
    
    # print "     NO " + str(genus)
    return False

wfile = csv.writer(open(outfile, "wb"))
wfile.writerow(["x","y","natural","tree:ref", "species","species:de","circumference","height","diameter_crown","type","taxon:cultivar","taxon","start_date","fixme","source"])

ifile = open(infile, "r")
reader = csv.reader(ifile, delimiter=',', quotechar='"')

print "Calculate total amount of entries"
rowcount = len(list(csv.reader(open(infile)))) 
rownum = 0
added = 0
baumgrleer = 0
nobaum = 0

print "Start processing"
for row in reader:
    if rownum % 10000 == 0: print "     Calculate " + str(rownum/1000) + " of " + str(rowcount/1000) + " thousand"
    if rownum == 0:
        header = row
    else:
        stri = str(row[5])

        '''überspringe "Leerer Pflanzstandort" oder andere unerwünschte Punkte'''
        if stri == "Leerer Pflanzstandort" or stri == "Leerer Baumstandort" or stri == "Baumgruppe":
            # if stri == "baumgruppe": print "leerer Pflanzstandort - überspringe " + str(stri)
            baumgrleer += 1
            rownum += 1
            continue
            
        stri = makeReplacements(stri)

        species = detectSpecies(stri)
        genus = detectGenus(species)
        height = detectHeight(row)
        sorte = detectSorte(stri)
        deutsch = detectDeutsch(stri)
        geo = extractGeometry(row)
        year = detectYear(row)
        circumference = detectCircumference(row)
        treeid = detectTreeId(row)
        diameter_crown = detectWidth(row)
        ttype = setTtype(genus.lower())
        taxon = setTaxon(species,sorte)
        
        if isBaum(genus,height,circumference, diameter_crown,species,year):
            added += 1
            wfile.writerow([geo[0],geo[1], "tree", treeid, species, deutsch, circumference, height, diameter_crown, ttype, sorte, taxon, year,"","OGD Vienna"])
        else:
            wfile.writerow([geo[0],geo[1], "tree", treeid, species, deutsch, circumference, height, diameter_crown, ttype, sorte, taxon, year,"Baum oder Strauch","OGD Vienna"])
            nobaum += 1
            added += 1
        
    rownum += 1

print "finished " + str(rownum) + " iterations"
print "left out " + str( (rownum - added) + nobaum) + " trees"
print "Leer oder Baumgruppe: " + str(baumgrleer)
print "noBaum: " + str(nobaum)
