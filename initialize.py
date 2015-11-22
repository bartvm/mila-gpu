#!/usr/bin/python
# -*- coding: utf-8 -*-
from operator import itemgetter
from reserve import Host, Model, GPU, Room, User, db


def initialize():
    hosts = [
        # name, memory, room, storage
        ('barney0', 24, 'Server room', None),
        ('eos1', 16, '3245', 3600),
        ('eos2', 16, '3336', 3600),
        ('eos3', 16, '3256', 3600),
        ('eos4', 16, '3251', 3600),
        ('eos5', 16, '3248', 3600),
        ('eos6', 16, '3248', 3600),
        ('eos7', 16, '3256', 3600),
        ('eos11', 32, '3248', 3600),
        ('eos12', 32, '3248', 3600),
        ('eos13', 32, '3248', 3600),
        ('eos14', 32, '3248', 3600),
        ('eos15', 32, '3248', 3600),
        ('eos16', 64, '3332', 3600),
        ('eos17', 64, '3332', 3600),
        ('eos18', 64, '3332', 3600),
        ('eos19', 64, '3332', 3600),
        ('eos20', 64, '3336', 3600),
        ('eos21', 64, '3255', 3600),
        ('eos22', 64, '3256', 3600),
        ('leto01', 64, '3256', 3600),
        ('leto02', 32, '3332', 3600),
        ('leto03', 32, '3332', 3600),
        ('leto04', 32, '3262', 3600),
        ('leto05', 32, '3244', 3600),
        ('leto06', 32, '3244', 3600),
        ('leto07', 32, '3244', 3600),
        ('leto08', 32, '3244', 3600),
        ('leto11', 64, '3256', 3600),
        ('leto12', 64, '3256', 3600),
        ('leto13', 64, '3256', 3600),
        ('leto14', 64, '3256', 3600),
        ('leto15', 64, '3332', 3600),
        ('leto17', 64, '3244', 3600),
        ('leto18', 64, '3262', 3600),
        ('leto50', 64, '3256', 3600),
        ('leto52', 64, '3256', 3600),
        ('kepler1', 256, 'Server room', 3600),
        ('kepler2', 256, 'Server room', 3600),
        ('kepler3', 256, 'Server room', 3600),
        ('assam', 10, None, 390),
        ('chai', 10, '3336', 390),
        ('bart1', 12, '3336', 3600),
        ('bart2', 12, '3256', 3600),
        ('bart3', 12, '3336', 3600),
        ('bart4', 12, '3256', 3600),
        ('bart5', 12, '3256', 3600),
        ('bart6', 12, '3248', 3600),
        ('bart7', 12, None, 3600),
        ('bart10', 64, '3336', 3600),
        ('bart12', 64, '3248', 3600),
        ('bart13', 64, '3256', 3600),
        ('bart14', 64, '3336', 3600),
        ('bart15', 64, '3355', 3600),
        ('bart16', 64, '3357', 3600),
        ('mila00', 64, '3332', 5500),
        ('sencha', 8, '3355', 385),
        ('ceylon', 12, '3248', 416),
    ]
    models = [
        # name, memory, compute capability
        ('GT 610', 2, 2.1),
        ('GTX 470', 1.25, 2.0),
        ('GTX 480', 1.5, 2.0),
        ('GTX 580', 1.5, 2.0),
        ('GTX 660', 2, 3.0),
        ('GTX 680', 2, 2.0),
        ('GTX 750', 2, 5.0),
        ('K80 (half)', 12, 3.7),
        ('K6000', 12, 3.5),
        ('GTX Titan X', 12, 5.2),
        ('GTX Titan', 6, 3.5),
        ('GTX Titan Black', 6, 3.5)
    ]
    gpus = [
        # host, device, model
        ('barney0', 'gpu0', 'GTX 580'),
        ('barney0', 'gpu1', 'GTX 580'),
        ('barney0', 'gpu2', 'GTX 580'),
        ('barney0', 'gpu3', 'GTX 580'),
        ('eos1', 'gpu0', 'GTX Titan'),
        ('eos2', 'gpu0', 'GTX Titan Black'),
        ('eos3', 'gpu0', 'GTX Titan X'),
        ('eos4', 'gpu0', 'GTX Titan Black'),
        ('eos5', 'gpu0', 'GTX Titan Black'),
        ('eos6', 'gpu0', 'GTX Titan Black'),
        ('eos7', 'gpu0', 'GTX Titan Black'),
        ('eos11', 'gpu0', 'GTX Titan Black'),
        ('eos11', 'gpu1', 'GT 610'),
        ('eos12', 'gpu0', 'GTX Titan Black'),
        ('eos12', 'gpu1', 'GT 610'),
        ('eos13', 'gpu0', 'GTX Titan Black'),
        ('eos13', 'gpu1', 'GT 610'),
        ('eos14', 'gpu0', 'GTX Titan Black'),
        ('eos14', 'gpu1', 'GT 610'),
        ('eos15', 'gpu0', 'GTX Titan X'),
        ('eos15', 'gpu1', 'GT 610'),
        ('eos16', 'gpu0', 'GTX Titan X'),
        ('eos16', 'gpu1', 'GT 610'),
        ('eos17', 'gpu0', 'GTX Titan X'),
        ('eos17', 'gpu1', 'GT 610'),
        ('eos18', 'gpu0', 'GTX Titan X'),
        ('eos18', 'gpu1', 'GT 610'),
        ('eos19', 'gpu0', 'GTX Titan X'),
        ('eos19', 'gpu1', 'GT 610'),
        ('eos20', 'gpu0', 'K6000'),
        ('eos21', 'gpu0', 'K6000'),
        ('eos22', 'gpu0', 'K6000'),
        ('leto01', 'gpu0', 'GTX Titan X'),
        ('leto01', 'gpu1', 'GTX Titan X'),
        ('leto02', 'gpu0', 'GTX Titan X'),
        ('leto02', 'gpu1', 'GTX 750'),
        ('leto03', 'gpu0', 'GTX Titan X'),
        ('leto03', 'gpu1', 'GTX 750'),
        ('leto04', 'gpu0', 'GTX Titan X'),
        ('leto04', 'gpu1', 'GTX 750'),
        ('leto05', 'gpu0', 'GTX Titan X'),
        ('leto05', 'gpu1', 'GTX 750'),
        ('leto06', 'gpu0', 'GTX Titan X'),
        ('leto06', 'gpu1', 'GTX 750'),
        ('leto07', 'gpu0', 'GTX Titan X'),
        ('leto07', 'gpu1', 'GTX 750'),
        ('leto08', 'gpu0', 'GTX Titan X'),
        ('leto08', 'gpu1', 'GTX 750'),
        ('leto11', 'gpu0', 'GTX Titan X'),
        ('leto11', 'gpu1', 'GTX Titan X'),
        ('leto11', 'gpu2', 'GTX 750'),
        ('leto12', 'gpu0', 'GTX Titan X'),
        ('leto12', 'gpu1', 'GTX Titan X'),
        ('leto12', 'gpu2', 'GTX 750'),
        ('leto13', 'gpu0', 'GTX Titan X'),
        ('leto13', 'gpu1', 'GTX Titan X'),
        ('leto13', 'gpu2', 'GTX 750'),
        ('leto14', 'gpu0', 'GTX Titan X'),
        ('leto14', 'gpu1', 'GTX Titan X'),
        ('leto14', 'gpu2', 'GTX 750'),
        ('leto15', 'gpu0', 'GTX Titan X'),
        ('leto15', 'gpu1', 'GTX Titan X'),
        ('leto15', 'gpu2', 'GTX 750'),
        ('leto17', 'gpu0', 'GTX Titan X'),
        ('leto17', 'gpu1', 'GTX Titan X'),
        ('leto17', 'gpu2', 'GTX 750'),
        ('leto18', 'gpu0', 'GTX Titan X'),
        ('leto18', 'gpu1', 'GTX Titan X'),
        ('leto18', 'gpu2', 'GTX 750'),
        ('leto50', 'gpu0', 'GTX Titan X'),
        ('leto50', 'gpu1', 'GTX Titan X'),
        ('leto50', 'gpu2', 'GTX Titan X'),
        ('leto50', 'gpu3', 'GTX 750'),
        ('leto52', 'gpu0', 'GTX Titan X'),
        ('leto52', 'gpu1', 'GTX Titan X'),
        ('leto52', 'gpu2', 'GTX Titan X'),
        ('leto52', 'gpu3', 'GTX 750'),
        ('kepler1', 'gpu0', 'K80 (half)'),
        ('kepler1', 'gpu1', 'K80 (half)'),
        ('kepler1', 'gpu2', 'K80 (half)'),
        ('kepler1', 'gpu3', 'K80 (half)'),
        ('kepler1', 'gpu4', 'K80 (half)'),
        ('kepler1', 'gpu5', 'K80 (half)'),
        ('kepler1', 'gpu6', 'K80 (half)'),
        ('kepler1', 'gpu7', 'K80 (half)'),
        ('kepler2', 'gpu0', 'K80 (half)'),
        ('kepler2', 'gpu1', 'K80 (half)'),
        ('kepler2', 'gpu2', 'K80 (half)'),
        ('kepler2', 'gpu3', 'K80 (half)'),
        ('kepler2', 'gpu4', 'K80 (half)'),
        ('kepler2', 'gpu5', 'K80 (half)'),
        ('kepler2', 'gpu6', 'K80 (half)'),
        ('kepler2', 'gpu7', 'K80 (half)'),
        ('kepler3', 'gpu0', 'K80 (half)'),
        ('kepler3', 'gpu1', 'K80 (half)'),
        ('kepler3', 'gpu2', 'K80 (half)'),
        ('kepler3', 'gpu3', 'K80 (half)'),
        ('kepler3', 'gpu4', 'K80 (half)'),
        ('kepler3', 'gpu5', 'K80 (half)'),
        ('kepler3', 'gpu6', 'K80 (half)'),
        ('kepler3', 'gpu7', 'K80 (half)'),
        ('assam', 'gpu0', 'GTX 480'),
        ('assam', 'gpu1', 'GTX 480'),
        ('chai', 'gpu0', 'GTX 680'),
        ('chai', 'gpu2', 'GTX 660'),
        ('bart1', 'gpu0', 'GTX 580'),
        ('bart1', 'gpu1', 'GTX 580'),
        ('bart2', 'gpu0', 'GTX Titan'),
        ('bart2', 'gpu1', 'GTX Titan'),
        ('bart3', 'gpu0', 'GTX 580'),
        ('bart3', 'gpu1', 'GTX 580'),
        ('bart4', 'gpu0', 'GTX 580'),
        ('bart4', 'gpu2', 'GTX 580'),
        ('bart5', 'gpu0', 'GTX Titan Black'),
        ('bart5', 'gpu2', 'GTX Titan Black'),
        ('bart6', 'gpu0', 'GTX 480'),
        ('bart6', 'gpu2', 'GTX Titan Black'),
        ('bart7', 'gpu0', 'GTX Titan Black'),
        ('bart7', 'gpu2', 'GTX Titan Black'),
        ('bart10', 'gpu0', 'GTX Titan X'),
        ('bart10', 'gpu2', 'GTX Titan X'),
        ('bart12', 'gpu0', 'K6000'),
        ('bart12', 'gpu2', 'K6000'),
        ('bart13', 'gpu1', 'K6000'),
        ('bart13', 'gpu2', 'K6000'),
        ('bart14', 'gpu0', 'K6000'),
        ('bart14', 'gpu2', 'K6000'),
        ('bart15', 'gpu0', 'K6000'),
        ('bart15', 'gpu2', 'K6000'),
        ('bart16', 'gpu0', 'K6000'),
        ('bart16', 'gpu2', 'K6000'),
        ('mila00', 'gpu0/dev3', 'GTX Titan X'),
        ('mila00', 'gpu1/dev2', 'GTX Titan X'),
        ('mila00', 'gpu2/dev1', 'GTX Titan X'),
        ('mila00', 'gpu3/dev0', 'GTX Titan X'),
        ('sencha', 'gpu0', 'GTX 470'),
        ('ceylon', 'gpu0', 'GTX 580'),
        ('ceylon', 'gpu2', 'GTX 580')
    ]

    users = [
        ('vanmerb', 'Bart', u'van Merriënboer')
    ]

    unreservable = [('leto08', 'gpu1'), ('ceylon', 'gpu0'), ('ceylon', 'gpu2')]

    # Find the unique rooms
    rooms = filter(bool, set(map(itemgetter(2), hosts)))

    # Add everything to the database
    room_entries = {}
    for room in rooms:
        room_entry = Room()
        room_entry.name = room

        db.session.add(room_entry)
        room_entries[room] = room_entry

    host_entries = {}
    for host in hosts:
        name, memory, room, storage = host
        host_entry = Host()
        host_entry.name = name
        host_entry.memory = memory
        host_entry.room = room_entries.get(room)  # Some hosts don't have rooms
        host_entry.storage = storage

        db.session.add(host_entry)
        host_entries[name] = host_entry

    model_entries = {}
    for model in models:
        name, memory, arch = model
        model_entry = Model()
        model_entry.name = name
        model_entry.memory = memory
        model_entry.arch = arch

        db.session.add(model_entry)
        model_entries[name] = model_entry

    for gpu in gpus:
        host, device, model = gpu
        gpu_entry = GPU()
        gpu_entry.device = device
        gpu_entry.host = host_entries[host]
        gpu_entry.model = model_entries[model]
        gpu_entry.reservable = (host, device) not in unreservable

        db.session.add(gpu_entry)

    for user in users:
        username, given_name, surname = user
        user_entry = User()
        user_entry.username = username
        user_entry.given_name = given_name
        user_entry.surname = surname

        db.session.add(user_entry)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    initialize()
    db.session.commit()
