#!/bin/bash

pytest;
err=$? ;
if (( $err != 5 )) ;
then
  exit $err;
fi
flake8 ;
