#!/bin/bash

free | grep Mem | awk '{print $2/1000}'