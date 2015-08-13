#!/bin/bash
ifconfig | grep inet | grep -v "127.0.0.1" | grep -v inet6
