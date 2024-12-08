# Boilerplate to support Advent of Code hackery
import sys
import os

def lines(input):
    return [ls for l in input.split('\n') if (ls := l.strip())]

def sections(input):
    return [[l.strip() for l in s.strip().split('\n')]
            for s in input.split('\n\n')]

def words(input):
    return [l.strip().split() for l in lines(input)]

def digit_grid(lines):
    return [[int(c) for c in l.strip()] for l in lines]

def digits(input):
    return digit_grid(lines(input))

def char_grid(lines):
    return [[c for c in l.strip()] for l in lines]

def chars(input):
    return char_grid(lines(input))

