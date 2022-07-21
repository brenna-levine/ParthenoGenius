#!/usr/bin/env python
# coding: utf-8

############## create argument parser #################
#import argparse library
import argparse

#create an argument parser object
parser=argparse.ArgumentParser(description='ParthenoGenius')

#add positional arguments to argument parser (i.e., the required information)
parser.add_argument('infile', help="csv file with maternal and offspring alleles - See README for format")
parser.add_argument('outfile', help="prefix for naming output files")
parser.add_argument('--error', help="sequencing error limit; default = 0.01; see README for explanation", nargs="?", const=1, default=0.01)
parser.add_argument('--max_het', help="maximum heterozygosity limit beyond which to call central fusion automixis; default = 0.8, see README for explanation", nargs="?", const=1, default=0.8)

#parse arguments
args=parser.parse_args()

###################### read data and define parameters #########################

#import pandas
import pandas

#read in command line argument of infile and assign contents to a variable
with open(args.infile) as data_file:
    structure_alleles = pandas.read_csv(data_file, index_col=0)

#name output files
outfile_homozyg = "%s.homozygous_loci.txt" % args.outfile
outfile_homozyg_sum = "%s.homozygosity_summary.txt" % args.outfile
outfile_heterozyg = "%s.heterozygous_loci.txt" % args.outfile
outfile_heterozyg_sum = "%s.heterozygosity_summary.txt" % args.outfile

#get date and time of run
from datetime import datetime
now = datetime.now()
now_str = now.strftime("%d/%m/%Y %H:%M:%S")

#count number of rows in dataframe
row_total = structure_alleles.shape[0]
#print(row_total)


#count number of columns (loci)
column_total = structure_alleles.shape[1]
#print(column_total)

################################# scan for maternal homozygous genotypes ###############################

#declare empty list to hold loci names for which mom is homozygous
mom_homozyg = [] 

#declare empty list to hold male alleles 
males = []

with open(outfile_homozyg, 'w') as fileobject: #with homozygous loci file open for writing

    #write statements to outfile to appear before loci are returned 
    fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: HOMOZYGOUS LOCI ########\n")
    fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
    fileobject.write(f"######## Data generated: {now_str} #########\n\n\n")
    fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tError = {args.error}\n\tMax_Het = {args.max_het}\n\n\n")
    fileobject.write(f"The following are the IDs for the loci at which the mom is homozygous.\n")
    fileobject.write(f"If an offspring allele differs from the maternal homozygous genotype, the discordant maternal allele and the offspring allele are printed below the locus.\n\n")
    fileobject.write(f"Please refer to the maternal homozygous loci summary output file for summary statistics.\n\n\n")
    
    for (columnName, columnData) in structure_alleles.iteritems():  #for column/value pair
   
        mom1 = columnData.values[0] #mom1 = mom allele 1
        mom2 = columnData.values[1] #mom2 = mom allele 2
    
        if mom1 == mom2: #if mom is homozygous - i.e., if the mom's two alleles at the locus are identical 
        
            fileobject.write(f"Locus: {columnName}\n\n") #write the locus name to the outfile
            mom_homozyg.append(columnName) #append the name of the locus to the mom_homozyg list
        
            if mom1 != columnData.values[2] or mom1 != columnData.values[3]: #if mom homozygous allele does not equal or or both offspring alleles  
               
                #write statements about maternal and offspring alleles to outfile
                fileobject.write(f"\tMom homozygous allele: {mom1}")
                fileobject.write(f"\n\tOffspring allele 1: {columnData.values[2]}")
                fileobject.write(f"\n\tOffspring allele 2: {columnData.values[3]}\n\n")
                
                males.append(columnData.values[2]) #append one of the male alleles to males list - doesn't matter which one because it is just for counting

#close fileobject
fileobject.close()

#define variable to hold estimated error rate for maternal heterozygosity scan
estim_error = (len(males)/len(mom_homozyg))

    
with open(outfile_homozyg_sum, 'w') as fileobject: #with homozygosity summary outfile open for writing
    #write summary statistics about the data to the outfile
    fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: HOMOZYGOUS LOCI SUMMARY ########\n")
    fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
    fileobject.write(f"######## Data generated: {now_str} #########\n\n\n") #write the date and time to the outfile
    fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tError = {args.error}\n\tMax_Het = {args.max_het}\n\n\n")
    fileobject.write("SUMMARY OF RESULTS: SCAN OF MATERNAL HOMOZYGOUS LOCI FOR DISCORDANT OFFSPRING GENOTYPES\n\n")
    fileobject.write(f"Total number of loci analyzed: {column_total}\n")
    fileobject.write(f"Number of loci for which mom is homozygous: {len(mom_homozyg)}\n")
    fileobject.write(f"Number of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles: {len(males)}\n")
    fileobject.write(f"Proportion of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles: {round(len(males)/len(mom_homozyg), 5)}\n")
    fileobject.write(f"Proportion of mom's homozygous loci for which offspring has identical homozygous genotypes to maternal homozygous genotypes: {round(1 - (len(males)/len(mom_homozyg)), 5)}\n\n\n")

    #Test for significance - if proportion on mom's homozygous loci for which at least one of male's alleles differ from maternal alleles is less
    #than or equal to default or user-defined sequencing error rate, call a likely parthenogen
    if (len(males)/len(mom_homozyg)) <= float(args.error):
        fileobject.write(f"THE OFFSPRING IS LIKELY A PARTHENOGEN.\n")
        fileobject.write(f"\n\tThe proportion of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles is less than the error rate.\n")
        fileobject.write(f"\tIncongruence between maternal genotypes and offspring genotypes at these loci is likely due to sequencing error rather than the presence of paternal alleles.")
    else:
        fileobject.write(f"THE OFFSPRING IS UNLIKELY TO BE A PARTHENOGEN.\n")
        fileobject.write(f"\n\tThe proportion of mom's homozygous loci for which at least one of offspring's alleles differs from maternal alleles exceeds the error rate.\n")
        fileobject.write(f"\tIncongruence between maternal homozygous genotypes and offspring genotypes at these loci are likely due to presence of paternal alleles.\n\n\n")
        fileobject.write(f"Note: Maternal heterozygosity analysis will not be conducted to test for mode of parthenogenesis.\n")
        fileobject.write(f"Note: Heterozygosity outfiles will not be created.")

#close fileobject
fileobject.close()

##################################### scan for maternal heterozygosity if evidence of parthenogenesis ##################################

if (len(males)/len(mom_homozyg)) <= float(args.error): #if evidence of parthenogenesis

    #declare empty list to hold loci names for which mom is heterozygous
    mom_het = [] 

    #reset males list to empty; this list will be populated by one male allele for each locus at which a male is homozygous for a maternal allele at a maternal heterozygous locus
    males = []

    with open(outfile_heterozyg, 'w') as fileobject: #with heterozygous loci outfile open for writing

        #write statements to outfile to appear before loci are returned 
        fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: HETEROZYGOUS LOCI #########\n")
        fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
        fileobject.write(f"######## Data generated: {now_str} #########\n\n\n") #write date and time to outfile
        fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tEstimated Error Rate from Previous Homozygosity Scan = {round(estim_error, 5)}\n\tMax_Het = {args.max_het}\n\n\n")
        fileobject.write(f"The following are the IDs for the loci at which the mom is heterozygous.\n") 
        fileobject.write(f"If the offspring is heterozygous for the mom's alleles, the mom's and offspring's alleles are printed below.\n\n")
        fileobject.write(f"Please refer to the maternal heterozygous loci summary output file for summary statistics.\n\n")
        
        for (columnName, columnData) in structure_alleles.iteritems():  #for column/value pair
   
            mom1 = columnData.values[0] #mom1 = mom allele 1
            mom2 = columnData.values[1] #mom2 = mom allele 2
    
            if mom1 != mom2: #if mom is heterozygous - i.e., if the mom's two alleles at the locus are not identical
        
                fileobject.write(f"Locus: {columnName}\n\n") #write the locus name to the outfile
                mom_het.append(columnName) #append the locus name to the mom_het list
        
                if mom1 == columnData.values[2] and mom2 == columnData.values[3]: #if mom allele 1 = offspring allele 1 and mom allele 2 = offspring allele 2  

                    #write data to the outfile
                    fileobject.write(f"\tMom allele 1: {mom1}") 
                    fileobject.write(f"\n\tMom allele 2: {mom2}") 
                    fileobject.write(f"\n\tOffspring allele 1: {columnData.values[2]}") 
                    fileobject.write(f"\n\tOffspring allele 2: {columnData.values[3]}\n\n")

                    males.append(columnData.values[3]) #append male allele to males list

                elif mom1 == columnData.values[3] and mom2 == columnData.values[2]: #if mom allele 1 = offspring allele 2 and mom allele 2 = offspring allele 1 

                    #write data to the outfile
                    fileobject.write(f"\tMom allele 1: {mom1}") 
                    fileobject.write(f"\n\tMom allele 2: {mom2}") 
                    fileobject.write(f"\n\tOffspring allele 1: {columnData.values[2]}") 
                    fileobject.write(f"\n\tOffspring allele 2: {columnData.values[3]}\n\n")

                    males.append(columnData.values[2]) #append male allele to males list


    #close the fileobject
    fileobject.close()

    with open(outfile_heterozyg_sum, 'w') as fileobject: #with the heterozygosity summary outfile open for writing
    
        #write statements to outfile
        fileobject.write(f"######## PARTHENOGENIUS - OUTPUT FILE: HETEROZYGOUS LOCI SUMMARY #########\n")
        fileobject.write(f"######## QUESTIONS? EMAIL BRENNA LEVINE - levine.brenna.a@gmail.com ########\n")
        fileobject.write(f"######## Data generated: {now_str} #########\n\n\n")
        fileobject.write(f"Parameters:\n\tInfile = {args.infile}\n\tOutfile = {args.outfile}\n\tEstimated Error Rate from Previous Homozygosity Scan = {round(estim_error, 5)}\n\tMax_Het = {args.max_het}\n\n\n")
        fileobject.write(f"SUMMARY: SCAN OF MATERNAL HETEROZYGOUS LOCI FOR OFFSPRING RETAINED HETEROZYGOSITY\n\n")
        fileobject.write(f"Total number of loci analyzed: {column_total}\n")
        fileobject.write(f"Number of loci for which mom is heterozygous: {len(mom_het)}\n") #print total number of loci
        fileobject.write(f"Number of mom's heterozygous loci for which offspring has retained heterozygosity: {len(males)}\n") #print number of loci for which all males have paternal alleles
        fileobject.write(f"Proportion of mom's heterozygous loci for which offspring has retained heterozygosity: {round(len(males)/len(mom_het), 5)}\n\n")

        #Test for significance - if proportion on mom's heterozygous loci for which male is heterozygous differ is less
        #than or equal to default or user-defined sequencing error rate, call a likely parthenogen
        if ((len(males)/len(mom_het))) > float(estim_error) and ((len(males)/len(mom_het))) < float(args.max_het):
            fileobject.write(f"This parthenogen was likely produced via:\tTERMINAL FUSION AUTOMIXIS\n\n")
            fileobject.write(f"\tThe proportion of mom's heterozygous loci for which offspring has retained heterozygosity is greater than the estimated error rate from the homozygosity scan.\n")
            fileobject.write(f"\tTherefore, offspring heterozygosity at these loci is not likely an artifact of sequencing error.")
        elif ((len(males)/len(mom_het))) <= float(estim_error):
            fileobject.write(f"This parthenogen was likely produced via:\tGAMETIC DUPLICATION\n\n")
            fileobject.write(f"\tThe proportion of mom's heterozygous loci for which offspring has retained heterozygosity is less than the estimated error rate from the homozygosity scan.\n")
            fileobject.write(f"\tTherefore, offspring heterozygosity at these loci is likely an artifact of sequencing error.")
        elif ((len(males)/len(mom_het))) > float(args.max_het):
            fileobject.write(f"This parthenogen was likely produced via:\tCENTRAL FUSION AUTOMIXIS\n\n")
            fileobject.write(f"\tThe mom and offspring have a similar number of heterozygous loci (i.e., limited reduction in offspring heterozygosity).\n")
     

    #close the fileobject
    fileobject.close()
   

