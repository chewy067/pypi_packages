import sys
import os
import random
import string
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import time
import datetime
import csv
import subprocess
from pysinewave import SineWave



##=================================
##  INSERT CODE HERE
##=================================

##<< beeping notifications ===================
def base_beep( frequency, duration, pause = 0.3 ):
    sinewave = SineWave( pitch = frequency )
    sinewave.play( )
    time.sleep( duration )
    sinewave.stop( )

    time.sleep( pause )


def error_beep( frequency, duration ):
    for i in range( 0, 7 ):
        # base_beep( 12, 0.15 )
        base_beep( frequency, duration )


def done_status_beep( first_freq, second_freq, duration ):
    for i in range( 0, 2 ):
        # base_beep( 5, 0.15 )
        base_beep( first_freq, duration )

    time.sleep( 0.1 )

    for i in range( 0, 2 ):
        # base_beep( 10, 0.15 )
        base_beep( second_freq, duration )


def success_beep( frequency, duration):
    for i in range( 0, 1 ):
        # base_beep( 10, 1 )
        base_beep( frequency, 1 )

    time.sleep( 0.1 )

    for i in range( 0, 2 ):
        # base_beep( 10, 0.15 )
        base_beep( frequency, duration )
##>> beeping notifications ===================


##<< start log tracking ===================
def random_string( char_length ): # define the function and pass the length as argument
    # Print the string in Lowercase
    string_result = ''.join(
         (
             random.choice(string.ascii_lowercase) for x in range( char_length )
         )
    ) # run loop until the define length
    return string_result


def remove_blank_lines( log_file ):
    output = ""
    with open( log_file ) as lines:
        for line in lines:
            if not line.isspace( ):
                output += line

    lines = open( log_file, 'w' )
    lines.write( output )
    lines.close( )


def open_file( filename ):
    if sys.platform == "win32":
        os.startfile( filename )
    else:
        if sys.platform == "darwin":
            opener = "open"
        else:
            opener = "xdg-open"
        subprocess.call( [opener, filename ] )


def get_file_size( file_path ):
    """Get the size of a file in bytes"""
    return os.path.getsize( file_path ) if os.path.isfile( file_path ) else 0



def log_setup( log_folder, log_file_name, is_log_update = 1, is_log_update_1 = 0, is_log_update_2 = 0 ):

    """
    log_folder : folder path of the log folder
    log_file_name : self_explanatory
    is_log_update : 0 if log updates not needed, 1 if log updates needed
    is_log_update_1 / 2 : 0 or 1 -- use only if there is another log with different format.
    """

    execute_key = datetime.datetime.now( ).strftime( "%Y%m%d-%H%M-%S" ) + "_" + str( random_string( 5 ) )
    pic = os.getlogin( )
    timestamp_0 = datetime.datetime.now( ).strftime( "%Y-%m-%d" )
    log_format = ".csv"


    ##FOR LOG FILE
    if is_log_update == 1:
        log_file = Path( log_folder, "python_logs " + timestamp_0 + log_format )

        ##create new log file if not exists
        if os.path.isfile( log_file ) == False:
            open( log_file, 'a+' )

            with open( log_file, 'a', encoding = 'utf-8' ) as csv_file:
                csv_writer = csv.writer( csv_file, delimiter = '|' )
                csv_writer.writerow( [
                     "pic_name"
                    ,"file_name"
                    ,"script_exec_key"
                    ,"level_name"
                    ,"timestamp"
                    ,"log_message"
                ] )


        ##open log file
        # os.startfile( log_file )
        open_file( log_file )
        time.sleep( 0.5 )


        ##setting log configuration
        logger1 = logging.getLogger( "" )
        logger1.setLevel( logging.DEBUG )
        logging1 = logging.FileHandler( log_file )
        logging1.setLevel( logging.DEBUG )
        formatter1 = logging.Formatter( pic + "|" + log_file_name + "|" + execute_key + "|" + "%(levelname)s|%(asctime)s|%(message)s"
                # column_format:
                #     pic_name
                #    ; file_name
                #    ; script_execution_unique_key
                #    ; level_name
                #    ; timestamp
                #    ; log_message
        )
        logging1.setFormatter( formatter1 )
        logger1.addHandler( logging1 )
        remove_blank_lines( log_file )

    elif is_log_update == 0:
        pass


def log_setup_v2(
         log_folder         : str
        , log_file_name     : str
        , max_size          : float   = 1024 * 1024
        , num_of_backups    : int     = 50
        , is_log_update     : int     = 1
        , is_debug          : bool    = True
        , is_log_update_1   : int     = 0
        , is_log_update_2   : int     = 0
    ):
    """
    Set up logging with rotation based on file size.

    Parameters:
    - log_folder        : Folder path of the log folder.
    - log_file_name     : Name of the log file.
    - max_size          : Size limit (in bytes) for the log file.
    - num_of_backups    : set limit on how many log files (aka backups) to be created. This is related to the setting in RotatingFileHandler where older backups will have the extensions updated with sequential number, e.g. '.csv.1', '.csv.2' etc.
    - is_log_update     : 0 if log updates not needed, 1 if log updates needed.
    - is_debug          : to toggle if there is a need for logging files to show debug type. Turning this off (i.e. setting to False) can help with conserving file size.
    """

    timestamp_0 = datetime.datetime.now( )
    execute_key = f"""{timestamp_0.strftime( "%Y%m%d-%H%M-%S" )}_{random_string( 5 )}"""
    pic         = os.getlogin( )
    timestamp_1 = timestamp_0.strftime( "%Y-%m-%d %H%M" )
    log_format  = "csv"

    # Define the base file name and path
    base_log_file = Path( log_folder, f"""python_logs_{timestamp_1}__{log_file_name}.{log_format}""" )

    # Create a new log file if it does not exist
    if not os.path.isfile( base_log_file ):
        with open( base_log_file, 'a+', encoding = 'utf-8' ) as csv_file:
            csv_writer = csv.writer( csv_file, delimiter = '|' )
            csv_writer.writerow(
                [
                     "pic_name"
                    , "file_name"
                    , "script_exec_key"
                    , "level_name"
                    , "timestamp"
                    , "log_message"
                ]
            )

    def setup_logging( log_file ):
        """Configure logging to use the given log file."""
        logger          = logging.getLogger( "" )
        logger.setLevel( logging.DEBUG )
        file_handler    = RotatingFileHandler( log_file, maxBytes = max_size, backupCount = num_of_backups )
        file_handler.setLevel( logging.DEBUG if is_debug else logging.INFO )
        formatter       = logging.Formatter( f"""{pic}|{log_file_name}|{execute_key}|%(levelname)s|%(asctime)s|%(message)s""" )
        file_handler.setFormatter( formatter )
        logger.addHandler( file_handler )
        remove_blank_lines( log_file )

    def remove_blank_lines( file_path ):
        """Remove blank lines from the log file."""
        with open( file_path, 'r', encoding = 'utf-8' ) as file:
            lines = file.readlines( )
        with open( file_path, 'w', encoding = 'utf-8' ) as file:
            file.writelines( line for line in lines if line.strip( ) )

    # Check file size and create new file if necessary

    # Open the log file and set up logging
    open_file( base_log_file )
    time.sleep( 0.5 )
    setup_logging( base_log_file )

    if is_log_update == 0:
        pass
##end log tracking >> ===================



##<<start log_comments ===================
def log_script_start( ):
    print_comment = "script started"
    logging.info( print_comment )
    print( print_comment )


def log_subscript_start( tagging, print_comment ):
    logging.info( "subscript started: " + tagging + ":-- " + print_comment )
    print( "subscript started: " + tagging + ":-- " + print_comment )


def log_subscript_finish( tagging, print_comment, with_beep = 0 ):
    logging.info( "subscript finished: " + tagging + ":-- " + print_comment )
    print( "subscript finished: " + tagging + ":-- " + print_comment )

    if with_beep == 1:
        done_status_beep( 5, 10, 0.15 )
    else:
        pass


def log_script_finish( with_beep = 1 ):
    print_comment = "script finished"
    logging.info( print_comment )

    if with_beep == 1:
        success_beep( 10, 0.15 )
    else:
        pass

    print( print_comment )


def log_exception( exception, with_beep = 1 ):
    if with_beep == 1:
        error_beep( 12, 0.15 )
    else:
        pass

    logging.debug( "error encountered: " + str( str( exception ).encode( "utf-8" ).decode( "utf-8" ) ) )
    print( "error encountered: " + str( str( exception ).encode( "utf-8" ).decode( "utf-8" ) ) )
##end log_comments >> ===================



##<<start log_refresh_update_comments ==========================
def update_log_status_1( is_log_update_1, is_succeed, tagging ):
    if is_log_update_1 == 1:
        if is_succeed == 1:
            logging.info( "update_log_status_1:" + tagging + ":-- " + "ok" )

        elif is_succeed == 0:
            logging.debug( "update_log_status_1:" + tagging + ":-- " + "failed" )

    elif is_log_update_1 == 0:
        pass


def update_log_status_2( is_log_update_2, is_succeed, tagging ):
    if is_log_update_2 == 1:
        if is_succeed == 1:
            logging.info( "update_log_status_2:" + tagging + ":-- " + "ok" )

        elif is_succeed == 0:
            logging.debug( "update_log_status_2:" + tagging + ":-- " + "failed" )

    elif is_log_update_2 == 0:
        pass
##end log_refresh_update_comments >> ==========================



##=================================
##  CODE ENDS HERE
##=================================
