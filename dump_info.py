#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This will erase the keys! (it will print them out before doing it though...)
#

import argparse
from openocd.flashProgrammer import flashProgrammer

MAIN_FLASH_ADDR = 0x8000000
FLASH_BASE = 0x8000000
KEY_FLASH_OFFSET = 0xffd4
SECTOR_SIZE = 0x400
KEY_BYTES = 30
CONTACT_SIZE = 88
CONTACT_SECTORS = [58, 59, 60, 61, 62, 63]

def hex_str(byte_list):
    byte_str = ''
    for byte in range(len(byte_list)):
        byte_str += '{:02X}'.format(byte_list[byte])
    return byte_str

def ascii_str(byte_list):
    byte_str = ''
    for byte in range(len(byte_list)):
        byte_str += chr(byte_list[byte])
    return byte_str

def print_contact_info(contact_bytes, name=True, radio_id=True, key=True, signature=True):
    uid = hex_str(contact_bytes[0:2])
    if uid == 'FFFF':
        return

    if name:
        print('name:' + ascii_str(contact_bytes[76:88]))
    
    if radio_id:
        print('radio id:' + hex_str(contact_bytes[0:2]))

    if key:
        print('public key:' + hex_str(contact_bytes[2:27]))
    
    if signature:
        print('signature:' + hex_str(contact_bytes[28:76]))
    print('')

parser = argparse.ArgumentParser()
parser.add_argument('--openocd_dir', action='store', default='/opt/gnuarmeclipse/openocd/0.10.0-201601101000-dev/', help='Open OCD dev directory')
parser.add_argument('--no_name', action='store_false', help='don\'t print names')
parser.add_argument('--no_key', action='store_false', help='don\'t print keys')
parser.add_argument('--no_radio', action='store_false', help='don\'t print keys')
parser.add_argument('--no_signature', action='store_false', help='don\'t print signatures')

args, unknown = parser.parse_known_args()

try:
    flasher = flashProgrammer(args.openocd_dir)

    if flasher.connected is True:

        # Read device unique ID
        print('contacts:')
        for sector in CONTACT_SECTORS:
            contact_bytes = flasher.readMem(FLASH_BASE + SECTOR_SIZE * sector, SECTOR_SIZE)
            
            for contact in range(SECTOR_SIZE/CONTACT_SIZE):
                start_byte = CONTACT_SIZE * (contact)
                end_byte = (start_byte + CONTACT_SIZE + 1)
                print_contact_info(
                    contact_bytes[start_byte:end_byte],
                    name=args.no_name,
                    key=args.no_key,
                    signature=args.no_signature)
except:
    raise

finally:
    # Make sure we kill the flasher process, otherwise openocd thread 
    # stays open in background
    if flasher:
        flasher.kill()   
