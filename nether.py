#!/usr/bin/env python

#Licence LGPL v2.1
#Creates copy of map db, leaving only specified(filtered) blocks.
#Can also be used for map backup, may-be even online backup.

import sqlite3
#import mt_block_parser

import re

def getIntegerAsBlock(i):
    x = unsignedToSigned(i % 4096, 2048)
    i = int((i - x) / 4096)
    y = unsignedToSigned(i % 4096, 2048)
    i = int((i - y) / 4096)
    z = unsignedToSigned(i % 4096, 2048)
    return x,y,z
def unsignedToSigned(i, max_positive):
    if i < max_positive:
        return i
    else:
        return i - 2*max_positive


source = r'/home/martin/.minetest/worlds/stampyworld/map.sqlite.big'
target = r'/home/martin/.minetest/worlds/stampyworld/map.sqlite'

#use compiled regular expression to filter blocks by block content. it is faster that checking "in array".
useful_block_evidence = re.compile(
    "default:cobble|"+
    "protector:protect|default:chest_locked|doors:door_steel|"+
    "default:chest|default:torch|default:stonebrick|default:glass|default:obsidian_glass|"+
    "default:ladder|default:rail|default:fence_wood|"+
    "bones:bones"
    )

sourceconn = sqlite3.connect(source)
targetconn = sqlite3.connect(target)
sourcecursor = sourceconn.cursor()
targetcursor = targetconn.cursor()
targetcursor.execute("CREATE TABLE IF NOT EXISTS `blocks` (`pos` INT NOT NULL PRIMARY KEY, `data` BLOB);")

for row in sourcecursor.execute("SELECT `pos`, `data` "+" FROM `blocks`;"):
    x,y,z=getIntegerAsBlock(row[0])
    if y > -320/16:
        targetcursor.execute("INSERT OR IGNORE INTO `blocks` VALUES (?, ?);", (row[0], row[1]))
            
targetconn.commit()

sourceconn.close()
targetconn.close()
