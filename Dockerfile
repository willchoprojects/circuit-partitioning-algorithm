FROM python:3.9-slim-buster

# Install Jupyter
RUN pip install --no-cache-dir jupyter

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy notebook files
# COPY *.ipynb ./

# Set working directory
WORKDIR /notebooks

# Start Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

