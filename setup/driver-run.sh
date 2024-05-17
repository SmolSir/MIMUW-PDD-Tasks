python3 -m venv venv
. venv/bin/activate
jupyter notebook --no-browser --NotebookApp.allow_origin='https://colab.research.google.com' --NotebookApp.port_retries=0 --port 8888 --ServerApp.token=PDD
