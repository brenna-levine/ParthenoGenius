# ParthenoGenius - Levine *et al.* in prep

## Summary:
ParthenoGenius is a python program that tests for evidence and mode of parthenogenesis. ParthenoGenius takes as an input file a csv containing the SNP or microsatellite genotypes of a mother and a single offspring (i.e., hypothesized to be a parthenogen). ParthenoGenius first identifies all loci at which the mother is homozygous. It then scans offspring genotypes at these loci for genotypes that differ from the maternal homozygous genotype. If the proportion of maternal homozygous loci at which the offspring exhibits a different genotype from the mother exceeds the default or user-defined sequencing error rate, the offspring is not called as a parthenogen, and it is concluded that offspring alleles that differ from the maternal alleles at maternal homozygous loci are paternal alleles. If this is the case, the program produces only two files: (1) a list of all loci at which the mother is homozygous and those loci at which the offspring genotype differs from the maternal homozgyous genotype, and (2) a summary file describing the number of loci at which the mother is homozygous, the proportion of maternal homozygous loci at which the offspring exhibits alleles that differ from the maternal genotype, and a statement that the offspring is unlikely to be a parthenogen. If the proportion of maternal homozygous loci at which the offspring exhibits alleles that differ from the maternal genotypes is less than or equal to the default or user-defined sequencing error rate, the offspring is called as a likely parthenogen, and it is concluded that alleles that differ from the maternal alleles at these loci are the result of sequencing error rather than paternal alleles. If this is the case, the above two files are generated, but the homozygosity summary file states that the offspring is a likely parthenogen. Further, the proportion of maternal homozygous loci at which offspring alleles differ from the maternal homozygous genotypes is taken as an updated estimate of the sequencing error rate.

If the offspring is called as a likely parthenogen, ParthenoGenius identifies all loci at which the mother is heterozygous and then scans offspring alleles at these loci for retained maternal heterozygosity to call a putative mode of parthenogenesis. If the proportion of maternal heterozygous loci at which the offspring has retained heterozygosity is less than or equal to the updated sequencing error rate, the mode of parthenogenesis is called as gametic duplication (i.e., the offspring has no or very little retained heterozygosity). If the proportion of maternal heterozygous loci at which the offspring has retained heterozygosity exceeds the updated sequencing error rate but is less than the default or user-defined heterozygosity proportion limit beyond which to call central fusion automixis, the mode of parthenogenesis is called as terminal fusion automixis (i.e., the offspring has retained heterozygosity it some, but not all, loci at which the mother is heterozygous). If the proportion of maternal heterozygous loci at which the offspring has retained heterozygosity is greater than or equal to the maximum heterozygosity proportion tolerated, the mode of parthenogenesis is called as central fusion automixis (i.e., the offspring has retained heterozygosity at nearly all or all of the maternal heterozygous loci).

## How to run ParthenoGenius:
ParthenoGenius is executed from the command line and requires that python3 is installed, as well as the package "pandas" (https://pandas.pydata.org). 

ParthenoGenius is executed by typing in the following command on the command line:

***python3  ParthenoGenius.py  infile  outfile***

The infile is the name of a csv file containing the locus names, and sample names for the mother and the offspring, and the genotypes at each locus. **Missing data is not tolerated** and could result in erroneous calls by the program. The infile is formatted similarly to a Structure file but does not contain any columns other than the sample names and the alleles. Each individual has two lines, with one allele on each line. It is sometimes easier to create your file as a text file. When viewed as a text file, an example infile would look like the following:

<img width="394" alt="Screen Shot 2022-07-21 at 4 08 54 PM" src="https://user-images.githubusercontent.com/63752115/180306183-d42ddac7-b3fe-447e-b401-62da7d5c64a4.png">

This file can easily be converted to a csv using the following command:
***cat file.txt | tr -s '[:blank:]' ',' > infile.csv***

You can easily create the input file for large genomic data sets from any program that produces a Structure file (e.g., PGDSpider, Stacks) by selecting Structure as your file type, deleting the second column (which would contain popflag data), and converting your text file to a csv.

The outfile is the a user-defined prefix to name your output files and can be anything that is descriptive to you.

There are two optional arguments that can be provided to ParthenoGenius. These are: --error and --max-het

--error is the estimated sequencing error rate for your data set. ***The default is 0.01***. This value will serve as a limit that determines whether the offspring is called as a parthenogen or a non-parthenogen.

--max_het is a limit representing the proportion of maternal heterozygous loci for which the offspring have retained heterozygosity beyond which to call central fusion automixis. ***The default value is 0.8.*** To illustrate, if this value is set to the default (0.8), the mode of parthenogenesis is called as central fusion automixis if the offspring have retained heterozygosity at 80% or more of the maternal heterozygous loci (i.e., the offspring is heterozygous at almost all of the mom's heterozygous loci). 

Choose these parameters carefully as they determine whether parthenogenesis is called and if so what mode of parthenogenesis is called.

To provide user-defined values for these parameters, use the following command:

***python3 ParthenoGenius.py --error value --max_het value infile outfile***

The following is an example in which the infile is called testdata.csv, the outfile will have the prefix testdata, and the default values of the optional parameters are used:

***python3 ParthenoGenius.py testdata.csv testdata***

The following is an example in which the infile is called testdata.csv, the outfile will have the prefix testdata, and the optional parameters are set to error = 0.05 and max_het = 0.95:

***python3 ParthenoGenius.py --error 0.05 --max_het 0.95 testdata.csv testdata***

## Test Data Provided:
There are multiple data sets that are provided with ParthenoGenius that can be used to test its functionality and experiment with parameter settings. These are:

1. TEST-DATA-SETS
2. CROC-PARTH-TESTS
3. ATROX-PARTH-TESTS
4. COBRA-PARTH-TESTS
5. ANACONDA-PARTH-TESTS

TEST-DATA-SETS/ contains 4 infiles that represent four data sets. These data sets include simulated data where the offspring is not a parthenogen (test_NONPARTH.csv), data where the offspring is a parthenogen produced via gametic duplication (test_GAM-DUP.csv), data where the offspring is a parthenogen produced via terminal fusion automixis (test_TERM-FUS.csv), and data where the offspring is a parthenogen produced via central fusion automixis (test_CEN-FUS.csv).

The remaining data sets include real published data representing cases of parthenogenesis and nonparthenogenesis. In CROC-PARTH-TESTS/, you will find data demonstrating that a crocodile offspring is a parthenogen produced via terminal fusion automixis (in prep by Booth *et al.*). In ATROX-PARTH-TESTS/, you will find data demonstrating that multiple rattlesnake offspring are not parthenogens (published in Levine *et al.* 2021). In COBRA-PARTH-TESTS/, you will find data demonstrating that 2 cobra offspring are parthenogens produced via terminal fusion automixis (published in Card *et al.* 2021). In ANACONDA-PARTH-TESTS/, you will find data demonstrating that 2 of 4 offspring are parthenogens produced via gametic duplication (published in Shibata *et al.* 2017).

## References for Published Data Sets:

Booth W, Levine BA, Corush JB, Davis MA, Dwyer Q, De Plecker R, Schuett GW. In prep. Discovery of parthenogenesis in an extant archosaur.

Card DC, Vonk FK, Smalbrugge S, Casewell NR, Wuster W, Castoe TA, Schuett GW, Booth W. 2021. Genome-wide data implicate terminal fusion automixis in king cobra facultative parthenogenesis. *Scientific Reports*, 11, 7271.

Levine BA, Schuett GW, Booth W. 2021. Exceptional long-term sperm storage by a female vertebrate. *PLoS One*, 16: e0252049.

Shibata H, Sakata S, Hirano Y, Nitasaka E, Sakabe A. 2017. Facultative parthenogenesis validated by DNA analyses in the green anaconda (*Eunectes murinus*). *PLoS One*, 12: e0189654.







