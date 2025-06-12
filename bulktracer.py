#!/usr/bin/env python3

import argparse
import datetime
import random
import re
from math import gcd
import gzip, json
from scamper import ScamperAddr, ScamperFile, ScamperCtrl, ScamperInst, ScamperDealias, ScamperDealiasProbedef, \
    ScamperTrace


class _VantagePoint:
    def __init__(self, name: str):
        self.name = name
        self.remote = None
        self.out = None
        self.inst = None
        self.coprime = 1
        self.runval = 1
        self.off = 0
        self.rounds = 0

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False


@staticmethod
def _arkname(name: str) -> str:
    match = re.match("^([a-z]{3}\\d*-[a-z]{2})\\.ark$", name)
    if match:
        return match.group(1)
    return name


@staticmethod
def _insteof(ctrl: ScamperCtrl, inst: ScamperInst, vps: list[_VantagePoint]):
    name = _arkname(inst.name)
    print(f"{datetime.datetime.now()} {name} finished")
    if name in vps:
        del vps[name]
    print(f"{len(vps)} VPs still working")


@staticmethod
def _doit(ctrl: ScamperCtrl, inst: ScamperInst, dst: str):
    ctrl.do_trace(dst, inst=inst, method='icmp-paris', ptr=False,
                  #                  wait_probe = datetime.timedelta(milliseconds=20), #50 pps
                  wait_timeout=datetime.timedelta(seconds=2))


@staticmethod
def _mode_dump(args: argparse.ArgumentParser):
    with gzip.open('random.json.gz', 'wt') as fout:
        for infile in args.files:
            if not infile.endswith('.warts'):
                continue
            print(infile)
            warts = ScamperFile(infile, filter_types=[ScamperTrace])
            for o in warts:
                # print('ooo')
                tr = {}
                vp = _arkname(o.list.monitor)
                tr['ark'] = vp
                if isinstance(o, ScamperTrace):
                    # print('yes')
                    if o.is_stop_completed():
                        tr['src'] = str(o.src)
                        tr['dst'] = str(o.dst)
                        hops = []

                        for i in range(o.hop_count):
                            if o.hop(i) is not None:
                                hopinfo = o.hop(i)
                                hops.append({'addr': str(hopinfo.src), 'name': hopinfo.name,
                                             'rtt': hopinfo.rtt.total_seconds() * 1000})

                        tr['hops'] = hops
                fout.write(json.dumps(tr) + '\n')
            warts.close()


def _mode_probe(args: argparse.ArgumentParser):
    batchsize = 50

    if args.targets is None:
        print("need targets file")
        return
    # if args.scampers is None:
    #     print("need scampers location")
    #     return

    # load the targets out of the input file
    targets = []
    with open(args.targets) as infile:
        for line in infile:
            try:
                targets.append(ScamperAddr(line.rstrip('\n')))
            except ValueError:
                pass

    # calculate a set if coprimes that will allow us to select each
    # item in the targets list in a per-VP randomized order.
    coprimes = []
    n = len(targets)
    for i in range(int(n / 2), n):
        x = gcd(i, n)
        if x == 1:
            coprimes.append(i)

    # ping from all of the available VPs.
    vps = {}
    # ctrl = ScamperCtrl(remote_dir=args.scampers, eofcb=_insteof, param=vps)
    ctrl = ScamperCtrl(mux='/run/ark-special/mux')
    ctrl.add_vps(ctrl.vps())
    tsstr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print('You are scheduling traceroutes towards', len(targets), 'from', len(vps), 'ark monitors!!')
    for target in targets:
        print('scheduling traceroute towards', target)
        for inst in ctrl.instances():
            name = _arkname(inst.name)
            if name == 'sjj-ba':
                inst.done()
                continue
            vp = _VantagePoint(name)
            vp.inst = inst
            vp.coprime = random.choice(coprimes)
            vp.runval = random.randrange(0, n)
            vp.out = ScamperFile(f"output/{name}.{tsstr}.bulktracer.warts", 'w')
            vps[name] = vp
            _doit(ctrl, vp.inst, target)

        print(f"{datetime.datetime.now()} starting with {len(vps)} VPs")
    ctrl.done()

    while not ctrl.is_done():
        obj = None
        try:
            obj = ctrl.poll(timeout=datetime.timedelta(seconds=15 * 60))
        except Exception as exc:
            print(exc)
        if obj is None:
            if not ctrl.is_done():
                print("f{datetime.datetime.now()} nothing rxd in time, exiting")
            break
        vp = vps[_arkname(obj.inst.name)]
        vp.out.write(obj)
        # if isinstance(obj, ScamperDealias):
        #     vp.rounds += 1
        #     print(f"{datetime.datetime.now()} {vp.name} round {vp.rounds}")
        #     _doit(ctrl, vp.inst, _getips(vp, targets, batchsize))


@staticmethod
def _main():
    parser = argparse.ArgumentParser(description='bulk pinger')
    parser.add_argument('files',
                        metavar='file',
                        nargs=argparse.REMAINDER,
                        help='collected data to process')
    parser.add_argument('--mode',
                        dest='mode',
                        choices=['dump', 'probe'],
                        required=True,
                        help='mode to use')
    parser.add_argument('--targets',
                        dest='targets',
                        default=None,
                        help='target file to probe, 1 address per line')
    # parser.add_argument('--scampers',
    #                     dest = 'scampers',
    #                     default = None,
    #                     help = 'directory to find scamper VPs')

    args = parser.parse_args()

    if args.mode == 'dump':
        _mode_dump(args)
    elif args.mode == 'probe':
        _mode_probe(args)


if __name__ == "__main__":
    _main()