FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive" TZ="America/New_York"

RUN dpkg --add-architecture i386
RUN apt update

RUN apt install -y iraf iraf-noao iraf-mscred
RUN apt install -y python3 python3-pip python3-astropy python3-pyraf saods9 sextractor
RUN apt install -y git wget sudo nano
RUN apt install -y libc6:i386 libncurses5:i386 libstdc++6:i386
RUN pip install jinja2
# RUN apt install zsh

RUN useradd astro --create-home --shell /bin/bash
RUN echo 'astro:pipeline_lya' | chpasswd

RUN wget https://ssb.stsci.edu/astroconda/linux-64/iraf.stsdas-3.18.3-1.tar.bz2 -q
RUN mkdir /tmp/stsdas_raw
RUN tar xf iraf.stsdas-3.18.3-1.tar.bz2 -C /tmp/stsdas_raw
RUN mv /tmp/stsdas_raw/iraf_extern/stsdas /usr/lib/iraf/extern
RUN rm -r /tmp/stsdas_raw

RUN wget https://ssb.stsci.edu/astroconda/linux-64/iraf.tables-3.18.3-1.tar.bz2 -q
RUN mkdir /tmp/tables_raw
RUN tar xf iraf.tables-3.18.3-1.tar.bz2 -C /tmp/tables_raw
RUN mv /tmp/tables_raw/iraf_extern/tables /usr/lib/iraf/extern
RUN rm -r /tmp/tables_raw

RUN usermod -aG sudo astro

USER astro
WORKDIR /home/astro

RUN echo 'stty xterm\n\
set     home            = "/home/astro/.iraf/"\n\
set     imdir           = "/home/astro/.iraf/imdir"\n\
set     cache           = "/home/astro/.iraf/cache"\n\
set     uparm           = "home$uparm/"\n\
set     userid          = "astro"\n'\ > ~/login.cl

# RUN sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" --unattended

RUN mkdir py_programs
COPY --chown=astro py_programs /home/astro/py_programs

CMD export USER=astro
ENV PYTHONPATH="/home/astro/"
