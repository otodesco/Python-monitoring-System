#!/bin/bash

df -k / | tail -1 | awk '{print $5}'        # Pourcentage utilisation disque
df -k / | tail -1 | awk '{print $2/1000}'   # Total de Mo du disque
df -k / | tail -1 | awk '{print $3/1000}'   # Nombre de Mo de disque utilisé