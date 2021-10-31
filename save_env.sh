#!/bin/bash

conda env export --file environment.yml
conda list --export > requirements.txt