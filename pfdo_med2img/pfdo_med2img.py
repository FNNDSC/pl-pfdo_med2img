#!/usr/bin/env python                                            
#
# pfdo_med2img ds ChRIS plugin app
#
# (c) 2016-2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import importlib.metadata

# Turn off all logging for modules in this libary.
import logging
logging.disable(logging.CRITICAL)

from chrisapp.base import ChrisApp
from pfdo_med2image import pfdo_med2image


Gstr_title = """

        __    _                           _  _____ _                 
       / _|  | |                         | |/ __  (_)                
 _ __ | |_ __| | ___   _ __ ___   ___  __| |`' / /'_ _ __ ___   __ _ 
| '_ \|  _/ _` |/ _ \ | '_ ` _ \ / _ \/ _` |  / / | | '_ ` _ \ / _` |
| |_) | || (_| | (_) || | | | | |  __/ (_| |./ /__| | | | | | | (_| |
| .__/|_| \__,_|\___/ |_| |_| |_|\___|\__,_|\_____/_|_| |_| |_|\__, |
| |               ______                                        __/ |
|_|              |______|                                      |___/ 

"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       pfdo_med2img.py 

    SYNOPSIS

        python pfdo_med2img.py                \\
            [-i|--inputFile <inputFile>]            \\
            [--filterExpression <someFilter>]       \\
            [--outputLeafDir <outputLeafDirFormat>] \\
            [-t|--outputFileType <outputFileType>]  \\
            [-s|--sliceToConvert <sliceToConvert>]  \\
            [-f|--frameToConvert <frameToConvert>]  \\
            [--showSlices]                          \\
            [--func <functionName>]                 \\
            [--reslice]                             \\
            [--threads <numThreads>]                \\
            [--test]                                \\
            [-x|--man]                              \\
            [-y|--synopsis]                         \\
            [--followLinks]                         \\
            [--json]                                \\
            <inputDir>                              \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python pfdo_med2img.py   \\
                                in    out

    DESCRIPTION

        `pl-pfdo_med2img` is a ChRIS plugin that can recursively 
        walk down a directory tree and perform a 'med2image'
        on files in each directory (optionally filtered by some simple
        expression). Results of each operation are saved in output tree
        that  preserves the input directory structure.

    ARGS

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

        [-f|--filterExpression <someFilter>]
        An optional string to filter the files of interest from the
        <inputDir> tree.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as
        'anon' or 'preview'.

        This is a formatting spec, so

            --outputLeafDir 'preview-%%s'

        where %%s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        SPECIAL CASES:
        For DICOM data, the <outputFileStem> can be set to the value of
        an internal DICOM tag. The tag is specified by preceding the tag
        name with a percent character '%%', so

            -o %%ProtocolName

        will use the DICOM 'ProtocolName' to name the output file. Note
        that special characters (like spaces) in the DICOM value are
        replaced by underscores '_'.

        Multiple tags can be specified, for example

            -o %%PatientName%%PatientID%%ProtocolName

        and the output filename will have each DICOM tag string as
        specified in order, connected with dashes.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

        [-s|--sliceToConvert <sliceToConvert>]
        In the case of volume files, the slice (z) index to convert. Ignored
        for 2D input data. If a '-1' is sent, then convert *all* the slices.
        If an 'm' is specified, only convert the middle slice in an input
        volume.

        [-f|--frameToConvert <sliceToConvert>]
        In the case of 4D volume files, the volume (V) containing the
        slice (z) index to convert. Ignored for 3D input data. If a '-1' is
        sent, then convert *all* the frames. If an 'm' is specified, only
        convert the middle frame in the 4D input stack.

        [--showSlices]
        If specified, render/show image slices as they are created.

        [--func <functionName>]
        Apply the specified transformation function before saving. Currently
        support functions:

            * invertIntensities
              Inverts the contrast intensity of the source image.

        [--reslice]
        For 3D data only. Assuming [i,j,k] coordinates, the default is to save
        along the 'k' direction. By passing a --reslice image data in the 'i' and
        'j' directions are also saved. Furthermore, the <outputDir> is subdivided into
        'slice' (k), 'row' (i), and 'col' (j) subdirectories.

        [--threads <numThreads>]
        If specified, break the innermost analysis loop into <numThreads>
        threads.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--json]
        If specified, output a JSON dump of final return.

        [--followLinks]
        If specified, follow symbolic links.

        -v|--verbosity <level>
        Set the app verbosity level.

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write

"""


class Pfdo_med2img(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'FNNDSC <dev@babyMRI.org>'
    SELFPATH                = '/usr/local/bin'
    SELFEXEC                = 'pfdo_med2img'
    EXECSHELL               = 'python'
    TITLE                   = 'A ChRIS plugin app to run the Python utility: pfdo_med2image'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to run the Python utility: pfdo_med2image'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = importlib.metadata.version(__package__)
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument("-i", "--inputFile",
                            help    = "input file",
                            dest    = 'inputFile',
                            type    = str,
                            optional= True,
                            default = '')
        self.add_argument("--filterExpression",
                            help    = "string file filter",
                            dest    = 'filter',
                            type    = str,
                            optional= True,
                            default = '')
        self.add_argument("--printElapsedTime",
                            help    = "print program run time",
                            dest    = 'printElapsedTime',
                            action  = 'store_true',
                            type    = bool,  
                            optional= True,   
                            default = False)
        self.add_argument("--threads",
                            help    = "number of threads for innermost loop processing",
                            dest    = 'threads',
                            type    = str,
                            optional= True,
                            default = "0")
        self.add_argument("--outputLeafDir",
                            help    = "formatting spec for output leaf directory",
                            dest    = 'outputLeafDir',
                            type    = str,
                            optional= True,
                            default = "")
        self.add_argument("--test",
                            help    = "test",
                            dest    = 'test',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument("-y", "--synopsis",
                            help    = "short synopsis",
                            dest    = 'synopsis',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument("--overwrite",
                            help    = "overwrite files if already existing",
                            dest    = 'overwrite',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument("--followLinks",
                            help    = "follow symbolic links",
                            dest    = 'followLinks',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
                            
        # med2image additional CLI flags
        self.add_argument("-o", "--outputFileStem",
                            help    = "output file",
                            default = "output.jpg",
                            type    = str,
                            optional= True,
                            dest    = 'outputFileStem')
        self.add_argument("-t", "--outputFileType",
                            help    = "output image type",
                            dest    = 'outputFileType',
                            type    = str,
                            optional= True,
                            default = '')
        self.add_argument("-s", "--sliceToConvert",
                            help="slice to convert (for 3D data)",
                            dest='sliceToConvert',
                            type    = str,
                            optional= True,
                            default='-1')
        self.add_argument("-f", "--frameToConvert",
                            help    = "frame to convert (for 4D data)",
                            dest    = 'frameToConvert',
                            type    = str,
                            optional= True,
                            default = '-1')
        self.add_argument('-r', '--reslice',
                            help    = "save images along i,j,k directions -- 3D input only",
                            dest    = 'reslice',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument('--showSlices',
                            help    = "show slices that are converted",
                            dest    = 'showSlices',
                            action  = 'store_true',
                            type    = bool,
                            optional= True,
                            default = False)
        self.add_argument('--func',
                            help    = "apply transformation function before saving",
                            dest    = 'func',
                            type    = str,
                            optional= True,
                            default = "")


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        if options.man or options.synopsis:
            self.show_man_page()

        options.inputDir = options.inputdir
        options.outputDir = options.outputdir

        pfdo_shell = pfdo_med2image(vars(options))

        d_pfdo_shell = pfdo_shell.run(timerStart = True)
        print(pfdo_shell)

        if options.printElapsedTime:
            pfdo_shell.dp.qprint(
                    "Elapsed time = %f seconds" %
                    d_pfdo_shell['runTime']
            )

        sys.exit(0)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)

# ENTRYPOINT
if __name__ == "__main__":
    app = Pfdo_med2img()
    app.launch()