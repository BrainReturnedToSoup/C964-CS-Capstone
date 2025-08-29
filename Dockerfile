FROM continuumio/miniconda3

# get the env data for conda
COPY environment.yml .

# create the conda env
RUN conda env create -f environment.yml

# activate the env
SHELL ["conda","run", "-n", "capstone-env", "/bin/bash", "-c"]
ENV PATH /opt/conda/envs/capstone-env/bin:$PATH


# create a directory for the source, need to make explicit "back_end" because the python modules use such as the source of truth in imports
WORKDIR /src
ENV PYTHONPATH=/src

# copy the src into the container
COPY ./back_end /src/back_end

CMD ["python", "-m", "back_end.app"]