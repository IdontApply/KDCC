FROM jupyter/base-notebook:python-3.7.6



#COPY requirements.txt .
RUN conda install -c conda-forge voila
RUN conda install geopandas

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY germany germany
COPY csv csv
COPY test.ipynb .


