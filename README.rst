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

`pl-pfdo_med2img` is a ChRIS plugin that can recursively 
walk down a directory tree and perform a 'med2image'
on files in each directory. (optionally filtered by some simple
expression). Results of each operation are saved in output tree
that  preserves the input directory structure.


Synopsis
--------

.. code::

    python pfdo_med2img.py                  \
            [-i|--inputFile <inputFile>]            \
            [--filterExpression <someFilter>]       \
            [--outputLeafDir <outputLeafDirFormat>] \
            [-t|--outputFileType <outputFileType>]  \
            [-s|--sliceToConvert <sliceToConvert>]  \
            [-f|--frameToConvert <frameToConvert>]  \
            [--showSlices]                          \
            [--func <functionName>]                 \
            [--reslice]                             \
            [--threads <numThreads>]                \
            [--test]                                \
            [-x|--man]                              \
            [-y|--synopsis]                         \
            [--followLinks]                         \
            [--json]                                \
            <inputDir>                              \
            <outputDir> 


Arguments
---------

.. code::

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


Run
===

While ``pl-pfdo_med2img`` is meant to be run as a containerized docker image, typically within ChRIS, it is quite possible to run the dockerized plugin directly from the command line as well. The following instructions are meant to be a psuedo- ``jupyter-notebook`` inspired style where if you follow along and copy/paste into a terminal you should be able to run all the examples.

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

::

    git clone https://github.com/FNNDSC/SAG-anon-nii.git

Pull DICOM
^^^^^^^^^^

The input should be a DICOM file usually with extension .dcm

We provide a sample directory of .dcm images here. (https://github.com/FNNDSC/SAG-anon.git)

-   Clone this repository (SAG-anon) to your local computer.

::

    git clone https://github.com/FNNDSC/SAG-anon.git


Run using ``docker run``
^^^^^^^^^^^^^^^^^^^^^^^^^^

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

    docker run --rm             \
        -v ${DEVEL}/:/incoming                          \
        -v ${DEVEL}/results/:/outgoing                  \
        fnndsc/pl-pfdo_med2img pfdo_med2img.py          \
        --filterExpression nii                          \
        --threads 0                                     \
        --printElapsedTime                              \
        --verbosity 5                                   \

The above command uses the argument ``--filterExpression`` to filter the ``.nii`` (NIfTI) files from the ${DEVEL} directory.
It replicates the structure of the ``inputdir`` into the ``outputdir`` (in this case: ``results`` directory) then converts all those NIfTI files (in this case SAG-anon.nii) to png files within  
the outputdir.

The following is a similar example that converts all the ``DICOM`` files to png/jpg images in the desired outputdir.

**NOTE:** Make sure you clear the ``results`` directory before running the following command.

.. code:: bash

    docker run --rm             \
        -v ${DEVEL}/:/incoming                          \
        -v ${DEVEL}/results/:/outgoing                  \
        fnndsc/pl-pfdo_med2img pfdo_med2img.py          \
        --filterExpression dcm                          \
        --threads 0                                     \
        --printElapsedTime                              \
        --verbosity 5                                   \
