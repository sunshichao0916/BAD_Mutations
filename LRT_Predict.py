#!/usr/bin/env python

#   Script to perform LRT from Chun and Fay (2009) to predict deleterious SNPs
#   in plants.
#   Requires a user name and password for the JGI phyotzome portal (Free)
#   Thomas Kono
#       March 4, 2015
#       Saint Paul, MN

#   Dependencies:
#       1) requests http://www.python-requests.org
#       2) argparse https://code.google.com/p/argparse/
#           (Not required for Python 3 and Python 2 >= 2.7)
#       3) Biopython http://biopython.org/
#       4) BLAST+ executables from NCBI


#   To handle passwords
import getpass
#   To cd
import os
#   to check arguments
import sys
#   for verbosity messages
import logging

#   Import the dependency checking script
from lrt_predict.General import check_modules
#   Import the verbosity script
from lrt_predict.General import set_verbosity
#   Import our argument parsing script
from lrt_predict.General import parse_args


#   Define a function for fetching
def fetch(arg, log):
    fetchdeps = check_modules.check_modules(fetch=True)
    if fetchdeps:
        check_modules.missing_mods(fetchdeps)
        exit(1)
    #   Next we check for the presence of the utilities we need to 
    #   do the fetching
    missing_reqs = check_modules.missing_executables(['bash', 'makeblastdb', 'gzip', 'sum'])
    if missing_reqs:
        log.error('Some required executables were not found on your system: ' + '\n'.join(missing_reqs) + '\nPlease install them to continue.')
        exit(1)
    #   Import the main fetching script
    #   We do it here, since we only want to import this if we are fetching
    import lrt_predict.Fetch.phytozome as phytozome
    import lrt_predict.Fetch.ensembl as ensembl
    #   Create a new Phytozome instance that will handle our work with
    #   the JGI Genomes Portal.
    log.info('Creating a new Phytozome instance to fetch data.')
    #   We give it username, password, base directory, whether or not we have to log in and 
    p = phytozome.Phytozome(arg['user'], arg['password'], arg['base'], arg['convert_only'], arg['verbose'])
    log.info('Creating a new Ensembl instance to fetch data.')
    ens = ensembl.EnsemblPlants(arg['base'], arg['convert_only'], arg['verbose'])
    if arg['convert_only']:
        log.info('Only converting files.')
        ens.convert()
        p.convert()
    elif arg['fetch_only']:
        log.info('Only downloading files.')
        log.info('Fetching from Ensembl Plants...')
        ens.get_ftp_urls()
        ens.download_files()
        log.info('Fetching from Phytozome...')
        p.get_xml_urls()
        p.fetch_cds()
    else:
        log.info('Downloading and converting Ensembl Plants files...')
        ens.get_ftp_urls()
        ens.download_files()
        log.info('Downloading and converting files.')
        p.get_xml_urls()
        p.fetch_cds()
        ens.convert()
        p.convert()
    return


#   Define a function for BLASTing
def blast(arg, log):
    blastdeps = check_modules.check_modules(predict=True)
    #   Check the module dependencies for the BLAST function
    if blastdeps:
        check_modules.missing_mods(blastdeps)
        exit(1)
    missing_reqs = check_modules.missing_executables(['bash', 'tblastx'])
    #   And then check the executable dependencies
    if missing_reqs:
        log.error('Some required executables were not found on your system: ' + '\n'.join(missing_reqs) + '\nPlease install them to continue.')
        exit(1)
    #   If all that checks out, import the BLAST class script
    from lrt_predict.Blast import blast_search
    log.info('Creating a new instance to BLAST.')
    b = blast_search.BlastSearch(arg['base'], arg['fasta'], arg['evalue'], arg['verbose'])
    b.blast_all()
    #   hom contains the filename that has the unaligned sequence in it.
    hom = b.get_hit_seqs()
    return hom


#   Main function
def main():
    #   The very first thing we do is do a base check to make sure that we can
    #   parse arguments
    dep = check_modules.check_modules()
    if dep:
        check_modules.missing_mods(dep)
        exit(1)
    #   Parse the arguments
    #   First, a check to see if any arguments were sent at all
    #   If not, then print the usage and exit
    if not sys.argv[1:]:
        parse_args.usage()
        exit(1)
    arguments = parse_args.parse_args()
    #   Pull out the verbosity switch right away
    verbose = set_verbosity.verbosity('LRT_Predict', arguments.verbose)
    arguments_valid, msg = parse_args.validate_args(arguments, verbose)
    #   If we got a return value that isn't False, then our arguments are good
    if arguments_valid:
        verbose.debug(arguments_valid['action'] + ' subcommand was invoked')
        #   Which command was invoked?
        if arguments_valid['action'] == 'fetch':
            fetch(arguments_valid, verbose)
        elif arguments_valid['action'] == 'predict':
            #   We will return the filename that contains the unaligned
            #   sequences, as we will use these as inputs for prank
            unaligned_seqs = blast(arguments_valid, verbose)
    else:
        verbose.error(msg)
    return


#   Do the work here
main()
