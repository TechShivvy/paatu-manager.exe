import os
from dotenv import load_dotenv

from cryptography.fernet import Fernet

import re
import atexit
import signal
import sys

import asyncio
import discord
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyPKCE

import pickle

import random

from cryptography.fernet import Fernet