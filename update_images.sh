#!/bin/bash

echo "Montando las última versión de las imágenes..."
docker build -t ev_cp_m ./EV_CP_M
docker build -t ev_cp_e ./EV_CP_E