# Pipeline for creating NB422-detected (ODI) catalog

The repository contains a Docker-based pipeline for preprocessing observational data. The pipeline creates a "master catalog" that combines sextractor catalogs from the input of NB422 (ODI) and other broadband images in COSMOS field. The pipeline is fully automatic except during certain tasks in the pipeline that require user input (e.g. IRAF `msccmatch`, `imexamine` and sextractor tasks).

Features:

* run environment is independent of local machine
* only re-run necessary steps after changing input data and parameters
* automatically analyze stdout from IRAF `iterstat` and `imexamine` tasks and use result for the following step
* suuport multiple host operating systems

The pipeline is not meant to be run as is but should be modified to suit specific data analysis routine.

## license
Licensed under the MIT license; see LICENSE

## Software used in the example

SAOImageDS9, Python/AstroPy, IRAF/PyRaf, IDL, SExtractor

## Prerequisites

* [Docker](https://www.docker.com/)
* IDL, Python3 (if running the IDL-based generate_kernel task is desired)

## Instructions

1. prepare mosaic images and name them as `NB422.fits`, `g.fits` etc under a folder (rms images `g.rms.fits`); Download coordinate file from *Gaia* server to the same folder and name it as `gaia.coo` 
2. make any necessary changes to adapt the code to your workflow
3. edit `docker-compose.yml` and change `/path/to/data_folder` to the actual location of the data folder on the host machine
4. (steps 4-6 apply only if you want to run the generate_kernel task) 
open a new terminal, run `export REQUEST_PORT=8088` and `export RESPONSE_PORT=8089` (or any other port that you choose) in both terminals
5. copy `server.py` and `generate_kernel.pro` to the data folder
6. run `python server.py`
7. Back in the repository, run `docker build -t odi_pipeline .` to build the image
8. After the image is built successfully, run `docker-compose run --service-ports pipeline` to create a container
9. inside the container, run `python3 -m py_programs.tasks.runner create_makefile`
10. go to `/mnt/data` folder and run `make master_catalog.csv`
    * caution: for Mac and Windows users, check `Addtional Notes`

## Brief explanation of data processing in the pipeline

1. calibrate astrometry using gaia.coo, use IRAF `msccmatch` task
2. copy the new wcs in the mosaic image headers to their rms images, use IRAF `wcscopy`
3. (steps 3-4 apply only to broadband images) 
reproject the broadband images to the same tangent point and pixel scale of `NB422.fits`, use IRAF `wregister`
    * caution: turn on *flux_conserve* when dealing with the mosaic images; no need for rms maps
4. match the reprojected rms map to the sky noise of the reprojected mosaic image, use IRAF `iterstat`
5. make flag map of NB image, use Python
6. measure the image PSFs, use IRAF `imexamine`
7. make moffat PSFs, use Python
8. generate kernels, that transform original (broadband) PSFs to NB PSF, use IDL `max_entropy`
9. convolve broadband images, make sure all images have the same PSF, use Python
10. run sextractor, make a master catalog
11. All done!

## Additional notes

* IDL is required for creating kernels `bb_to_nb.fits`. The command is run on the host machine to avoid the complexity of installing IDL and setting up the license. The host communicates with the dock container via a basic TCP connection.
* The pipeline has been thoroughly tested on a 64-bit Ubuntu host.
* `touch` command is used after some IRAF/PyRAF tasks because IRAF changes the modification time of input files in an unexpected way, which makes the timestamp-based make system unusable

### Operation system support
* For both Windows and Mac systems:
   * edit `docker-compose.yml`: change `environment: DISPLAY=host.docker.internal:0`.
   * edit `server.py` (line:29) and `py_programs/func/generate_kernel.py` (line:8): change `127.0.0.1` to `host.docker.internal`.
* Windows:
   * must [have WSL 2 installed](https://docs.microsoft.com/en-us/windows/wsl/install), have [WSL integration](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers) enabled, and have [WSLg support](https://github.com/microsoft/wslg) (generally means on Windows 11). If there is an issue with opening display, refer to [Wiki](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg).
* Mac:
   * must [have XQuartz installed](https://www.xquartz.org/)
   * Launch XQuartz. Under the XQuartz menu, select Preferences
   * Go to the security tab and ensure "Allow connections from network clients" is checked.
   * Run `xhost + ${hostname}` to allow connections to the macOS host
   * For Mac with M1 processors, run `export DOCKER_DEFAULT_PLATFORM=linux/amd64` before docker build
