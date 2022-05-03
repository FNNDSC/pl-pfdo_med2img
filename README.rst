pl-pfdo_med2img
================================

.. image:: https://badge.fury.io/py/pfdo_med2img.svg
    :target: https://badge.fury.io/py/pfdo_med2img

.. image:: https://travis-ci.org/FNNDSC/pfdo_med2img.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdo_med2img

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-pfdo_med2img

.. contents:: Table of Contents


Abstract
--------

``pl-pfdo_med2img`` is a ChRIS plugin about a ``pfdo_med2image`` module. Consult the ``pfdo_med2image`` `repo <https://github.com/FNNDSC/pfdo_med2image>`_ for additional information -- this plugin wrapper exposes the same CLI contract with the exception that the input and output directories are positional mandatory arguments in the plugin, but named and optional in the module.


Synopsis
--------

.. code::

    pfdo_med2img                                            \
            [-i|--inputFile <inputFile>]                    \
            [--inputFileSubStr <substr>]                    \
            [--fileFilter <someFilter1,someFilter2,...>]    \
            [--dirFilter <someFilter1,someFilter2,...>]     \
            [--outputLeafDir <outputLeafDirFormat>]         \
            [-t|--outputFileType <outputFileType>]          \
            [-s|--sliceToConvert <sliceToConvert>]          \
            [--convertOnlySingleDICOM]                      \
            [--preserveDICOMinputName]                      \
            [-f|--frameToConvert <frameToConvert>]          \
            [--showSlices]                                  \
            [--func <functionName>]                         \
            [--reslice]                                     \
            [--rotAngle <angle>]                            \
            [--rot <3vec>]                                  \
            [--threads <numThreads>]                        \
            [--test]                                        \
            [-x|--man]                                      \
            [-y|--synopsis]                                 \
            [--followLinks]                                 \
            [--json]                                        \
            <inputDir>                                      \
            <outputDir>


Arguments
---------

.. code:: html

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

        [--inputFileSubStr <substr>]
        As a convenience, the input file can be determined via a substring
        search of all the files in the <inputDir> using this flag. The first
        filename hit that contains the <substr> will be assigned the
        <inputFile>.

        This flag is useful is input names are long and cumbersome, but
        a short substring search would identify the file. For example, an
        input file of

           0043-1.3.12.2.1107.5.2.19.45152.2013030808110149471485951.dcm

        can be specified using ``--inputFileSubStr 0043-``

        [--fileFilter <someFilter1,someFilter2,...>]
        An optional comma-delimated string to filter out files of interest
        from the <inputDir> tree. Each token in the expression is applied in
        turn over the space of files in a directory location, and only files
        that contain this token string in their filename are preserved.

        [-d|--dirFilter <someFilter1,someFilter2,...>]
        An additional filter that will further limit any files to process to
        only those files that exist in leaf directory nodes that have some
        substring of each of the comma separated <someFilter> in their
        directory name.

        [--analyzeFileIndex <someIndex>]
        An optional string to control which file(s) in a specific directory
        to which the analysis is applied. The default is "-1" which implies
        *ALL* files in a given directory. Other valid <someIndex> are:
            'm':   only the "middle" file in the returned file list
            "f":   only the first file in the returned file list
            "l":   only the last file in the returned file list
            "<N>": the file at index N in the file list. If this index
                   is out of bounds, no analysis is performed.
            "-1" means all files.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as
        'anon' or 'preview'.

        This is a formatting spec, so

            --outputLeafDir 'preview-%s'

        where %s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        SPECIAL CASES:
        For DICOM data, the <outputFileStem> can be set to the value of
        an internal DICOM tag. The tag is specified by preceding the tag
        name with a percent character '%', so

            -o %ProtocolName

        will use the DICOM 'ProtocolName' to name the output file. Note
        that special characters (like spaces) in the DICOM value are
        replaced by underscores '_'.

        Multiple tags can be specified, for example

            -o %PatientName%PatientID%ProtocolName

        and the output filename will have each DICOM tag string as
        specified in order, connected with dashes.

        [--convertOnlySingleDICOM]
        If specified, will only convert the single DICOM specified by the
        '--inputFile' flag. This is useful for the case when an input
        directory has many DICOMS but you specifially only want to convert
        the named file. By default the script assumes that multiple DICOMS
        should be converted en mass otherwise.

        [--preserveDICOMinputName]
        If specified, use the input DICOM name as the base of the output
        filename.

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

        [--rot <3DbinVector>]
        A per dimension binary rotation vector. Useful to rotate individual
        dimensions by an angle specified with [--rotAngle <angle>]. Default
        is '110', i.e. rotate 'x' and 'y' but not 'z'. Note that for a
        non-reslice selection, only the 'z' (or third) element of the vector
        is used.

        [--rotAngle <angle>]
        Default 90 -- the rotation angle to apply to a given dimension of the
        <3DbinVector>.

        [--func <functionName>]
        Apply the specified transformation function before saving. Currently
        support functions:

            * invertIntensities
              Inverts the contrast intensity of the source image.

        [--reslice]
        For 3D data only. Assuming [x,y,z] coordinates, the default is to save
        along the 'z' direction. By passing a --reslice image data in the 'x'
        and 'y' directions are also saved. Furthermore, the <outputDir> is
        subdivided into 'slice' (z), 'row' (x), and 'col' (y) subdirectories.

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


Run
===

While ``pl-pfdo_med2img`` is meant to be run as a containerized docker image, typically within ChRIS, it is quite possible to run the dockerized plugin directly from the command line as well. The following instructions are meant to be a psuedo- ``jupyter-notebook`` inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

(For advanced, interested users, it is also possible to run the python program directory without containerization using a ``pip install .`` in the repo source directory. In such a case, adapt the follow-along instructions accordingly.)

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now we need to fetch medical image data (NIfTI and DICOM data)

How to pull medical image data
-------------------------------

These medical image data files are in 2 formats:
- NIfTI
- DICOM

The following steps show how to pull sample files for NIfTI or DICOM files.

Pull NIfTI
^^^^^^^^^^

The input should be a NIfTI volume with extension .nii.

We provide a sample volume here https://github.com/FNNDSC/SAG-anon-nii.git

- Clone this repository (SAG-anon-nii) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/SAG-anon-nii.git

Pull DICOM
^^^^^^^^^^

The input should be a DICOM file usually with extension .dcm

We provide a sample directory of .dcm images here. (https://github.com/FNNDSC/SAG-anon.git)

-   Clone this repository (SAG-anon) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/SAG-anon.git


Run using ``docker run``
-------------------------

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

- Make sure your current working directory is ``devel``. At this juncture it should contain ``SAG-anon`` as well as ``SAG-anon-nii``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

- Pull the ``fnndsc/pl-pfdo_med2img`` image using the following command.

.. code:: bash

    docker pull fnndsc/pl-pfdo_med2img


Examples
--------

Copy and modify the different commands below as needed:

.. code:: bash

    docker run --rm                                     \
        -v ${DEVEL}/:/incoming                          \
        -v ${DEVEL}/results/:/outgoing                  \
        fnndsc/pl-pfdo_med2img pfdo_med2img             \
        --fileFilter nii                                \
        --threads 0                                     \
        --printElapsedTime                              \
        --verbosity 5                                   \
        /incoming /outgoing

The above command uses the argument ``--filterExpression`` to filter any ``.nii`` (NIfTI) files from any nested location within the ``${DEVEL}`` directory. Then, for each filtered file in each nested directory, a conversion is performed and the results written to a corresponding nested location in the ``ouputdir`` (in this case the ``results`` directory).

The following is a similar example that converts all the ``DICOM`` files to png/jpg images in the desired outputdir.

**NOTE:** Make sure you clear the ``results`` directory before running the following command.

.. code:: bash

    docker run --rm                                     \
        -v ${DEVEL}/:/incoming                          \
        -v ${DEVEL}/results/:/outgoing                  \
        fnndsc/pl-pfdo_med2img pfdo_med2img             \
        --analyzeFileIndex f                            \
        --fileFilter dcm -t jpg                         \
        --threads 0 --reslice --verbosity 1             \
        --preserveDICOMinputName --printElapsedTime     \
        /incoming /outgoing

Debug
=====

To poke around the container innards,

.. code:: bash

    docker run --rm -it --userns=host --name med2img    \
        --entrypoint /bin/bash fnndsc/pl-pfdo_med2img

To debug with source code mapping into the container, do:

.. code:: bash

docker run --rm -it --userns=host --name med2img        \
    -v $PWD/pfdo_med2img/pfdo_med2img.py:/usr/local/lib/python3.9/site-packages/pfdo_med2img/pfdo_med2img.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw    \
    -w /outgoing                                        \
    fnndsc/pl-pfdo_med2img pfdo_med2img                 \
    --analyzeFileIndex f                                \
    --fileFilter dcm -t jpg                             \
    --threads 0 --reslice --verbosity 1                 \
    --preserveDICOMinputName --printElapsedTime         \
    /incoming /outgoing

_-30-_