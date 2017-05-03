# bugle

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  [![](http://progressed.io/bar/33?title=v1%20progress)](https://github.com/maxwu/bugle)

Python lib to parse Robot Framework keyword libraries and Test Suites. 
It reads git repo information and generate an HTML table of statistics of Robot Framework Keywords and Test Cases defined in *.robot files.
For each item, the table will show the presence mark of branches. 

## Introduction

This project is initialed as a prototype as a robot files parser for git repositories.

 - [X] Merge counter type statistic from branches and refresh ratios
 - [ ] Regularize the code structure
 - [ ] Refactor statistic methods 
 - [ ] Chart generation as in [cistat](https://github.com/maxwu/cistat)
  

## Targets

>TBC

## Configuration

>requirements.txt done, config guide TBC

## References

With the bugle stat, the trend of automation test cases and keywords growth cloud be presented as below chart:

![counter chart](http://oei21r8n1.bkt.clouddn.com/bugle-cases-small.png)

However, the test result trends on module failure rate, coverage and test time/efforts are covered by [cistat](https://github.com/maxwu/cistat).





