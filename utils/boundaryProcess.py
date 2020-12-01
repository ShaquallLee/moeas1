#!/usr/bin/env python
# encoding: utf-8
# @author: lishaogang
# @file: boundaryProcess.py
# @time: 2020/10/29 0029 16:02
# @desc: 超越边界处理方法
import random

def bpm1(xi, lbound, rbound):
    if xi < lbound:
        xi = lbound - random.random() * (xi - lbound)
    if xi > rbound:
        xi = rbound + random.random() * (rbound - xi)
    return xi


def bpm2(xi, lbound, rbound):
    if xi < lbound:
        xi = lbound
    if xi > rbound:
        xi = rbound
    return xi

def bpm3(xi, lbound, rbound):
    if xi < lbound or xi > rbound:
        xi = lbound + random.random()*(rbound-lbound)
    return xi
