#!/usr/bin/env python

import os
import sys
import argparse
import yaml
import json
from fnmatch import fnmatch
import re
import logging
import logging.config
from kombu import Connection, Exchange, Queue
from subprocess import Popen, PIPE
from datetime import datetime

description = """Pattern-match incoming file and publish event to AMQP exchange"""

script_dir = os.path.abspath(os.path.dirname(__file__))

def load_config(config_file):
    logger = logging.getLogger(__name__)
    if os.path.exists(config_file):
        cf = os.path.abspath(config_file)
    elif os.path.isabs(config_file):
        cf = config_file
    else:
        cf = os.path.join(script_dir, config_file)
    cfg = yaml.load(open(cf))
    logger.debug("config={}".format(cfg))
    return cfg

def get_rule(rules):
    if not rules: return
    if not isinstance(rules, list):
        rules = [rules]
    for r in rules:
        yield r
    return
        
class RuleMatcher:
    def __init__(self, config):
        """Precompile match rules for better performance"""
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.cmds = {}
        for d, rules in config.iteritems():
            rgen = get_rule(rules)
            default_rule = True
            # A rule may be a str, dict
            # Apply shell filename matching, unless a rule has 're'=True
            matchers = []
            cmdlist = []
            for r in rgen:
                if type(r) is str:
                    matcher.append(lambda f: fnmatch(f, r))
                elif isinstance(r, dict):
                    self.save_cmd_in_rule(cmdlist, r)
                    if r.get("re", False):
                        if "exclude" in r:
                            compiled = re.compile(r["exclude"])
                            matchers.append(dict(exclude=lambda f: compiled.search(f)))
                            default_rule = True
                        if "include" in r:
                            compiled = re.compile(r["include"])
                            matchers.append(dict(include=lambda f: compiled.search(f)))
                            default_rule = False
                    else:
                        if "exclude" in r:
                            pattern = r["exclude"]
                            matchers.append(dict(exclude=lambda f: fnmatch(f, pattern)))
                            default_rule = True
                        if "include" in r:
                            pattern = r["include"]
                            matchers.append(dict(include=lambda f: fnmatch(f, pattern)))
                            default_rule = False
                else:
                    raise ValueError("Unexpected config rule: {}: {}".format(type(r), r))
            # Catch-all rule is always the opposite of the last explicit rule
            matchers.append(lambda f: default_rule)
            self.config[d] = matchers
            if cmdlist:
                self.cmds[d] = cmdlist
    def match(self, path, filename):
        assert path in self.config, \
            "Path {} does not match any config {}".format(path, self.config.keys())
        for i, matcher in enumerate(self.config[path]):
            if isinstance(matcher, dict):
                if "exclude" in matcher and matcher["exclude"](filename):
                    self.logger.debug("excl i={} False".format(i))
                    return False
                if "include" in matcher:
                    m = matcher["include"](filename)
                    self.logger.debug("incl i={} m={}: {}".format(i, m, m is not None))
                    if m is None: return False
                    if type(m) is bool: return m
                    assert hasattr(m, 'groupdict'), "Unexpected matcher returned value: {}".format(m)
                    return m.groupdict()
            else:
                self.logger.debug("i={} {}".format(i, matcher(filename)))
                return matcher(filename)
    def save_cmd_in_rule(self, cmdlist, rule):
        if "cmd" not in rule: return
        if not rule["cmd"]: return
        if isinstance(rule["cmd"], list):
            cmdlist += rule["cmd"]
        else:
            cmdlist.append(rule["cmd"])
    
def setup_logging(verbosity=0, env_key="LOG_CFG"):
    # Translate verbosity counter to loglevel
    verbset = (logging.WARNING, logging.INFO, logging.DEBUG)
    if 0 < verbosity < len(verbset):
        level = verbset[verbosity]
    else:
        if verbosity < 0:
            level = verbset[0]
        else:
            level = verbset[-1]
    path = os.getenv(env_key, "logging.yml")
    if not os.path.exists(path):
        if not os.path.isabs(path):
            path = os.path.join(script_dir, path)
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

def main(argv=None):
    if argv is None:
        argv = sys.argv
    defvals = {
        "body": "file://{dir}.{file}",
        "rk": "{dir}.{file}",
    }
    def check_dir(d):
        if not os.path.isdir(d): raise argparse.ArgumentTypeError("must be an existing directory")
        return d
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("incron_dir", type=check_dir, \
        help="specifies incoming directory")
    parser.add_argument("incron_file", \
        help="specifies incoming file")
    parser.add_argument("incron_event", \
        help="specifies incoming event")
    parser.add_argument("-a", "--amqp", metavar='JSON', \
        help="specifies AMQP configuration file")
    parser.add_argument("-c", "--config", default="fse2amqp.yml", metavar='YAML', \
        help="specifies filename pattern file")
    parser.add_argument("-e", "--env", \
        help="specifies script which sets environment variables")
    parser.add_argument("--body", 
        help="specifies message body format: {}".format(defvals["body"]))
    parser.add_argument("--rk", \
        help="specifies message routing key format: {}".format(defvals["rk"]))
    parser.add_argument("-v", dest="verbosity", action="count", \
        help="increases verbosity")
    parser.add_argument("--log-config", default="logging.yml", \
        help="specifies YAML logging configuration")
    parser.set_defaults(**defvals)
    args = parser.parse_args()
    if not os.path.isfile(os.path.join(args.incron_dir, args.incron_file)):
        raise parser.error("incron_file must be an existing file")
    setup_logging(args.verbosity)
    logger = logging.getLogger(__name__)

    if args.env:
        if not os.path.exists(args.env) and not os.path.isabs(args.env):
            args.env = os.path.join(script_dir, args.env)
        if not os.path.exists(args.env):
            parser.error("Non-existent environment script: {}".format(args.env))
        p = Popen(['bash', '-c', 'source {} && env'.format(args.env)], stdout=PIPE, stderr=PIPE)
        source_env = {tup[0].strip(): tup[1].strip() for tup in map(lambda s: s.strip().split('=', 1), p.stdout)}
    else:
        source_env = {}
    if args.amqp:
        try:
            if not os.path.exists(args.amqp) and not os.path.isabs(args.amqp):
                args.amqp = os.path.join(script_dir, args.amqp)
            amqp = json.loads(open(args.amqp).read())
            uri = 'amqp://{amqp_user}:{amqp_pass}@{amqp_host}:{amqp_port}/{amqp_vhost}'.format(**amqp)
        except Exception, err:
            parser.error("Failed to load AMQP configuration from {}: {}".format(args.amqp, err))

    config = load_config(args.config)
    # Precompile match expressions and perform minimal check
    rm = RuleMatcher(config)
    for d, rules in config.iteritems():
        rv1 = rm.match(d, "TestFile")
        rv2 = rm.match(d, ".TestFile")
        logger.debug("{}: Testfile={} .Testfile={}".format(rules, rv1, rv2))

    rulematcher = RuleMatcher(config)
    matched = rulematcher.match(args.incron_dir, args.incron_file)
    if not matched:
        logger.debug("Skip unmatched file: {} {}".format(args.incron_dir, args.incron_file))
        return 0
    # Initialize with environment variables then override with runtime
    dic = source_env.copy()
    dic.update(os.environ)
    if isinstance(matched, dict): dic.update(matched)
    dic.update({
        'path': os.path.join(args.incron_dir, args.incron_file),
        'dir': args.incron_dir,
        'file': args.incron_file,
        'event': args.incron_event,
        'script_dir': script_dir,
    })
    logger.info('Processing: {path} for {event}'.format(**dic))
    if args.amqp:
        try:
            logger.debug('Trying to establish AMQP connection: {}'.format(uri))
            
            # Connect to rabbitmq server
            with Connection(uri) as conn:
                conn.connect()
                logger.debug('Connection established: {}'.format(uri))
                exchange = Exchange(amqp['amqp_exchange'], type='topic', channel=conn.default_channel)
                exchange.declare()
                body = args.body.format(**dic)
                rk = args.rk.format(**dic)
                exchange.publish(body, rk)
                logger.info('Published %d af_modis messages' % count)
        except Exception, err:
            dic['err'] = err
            logging.exception('Failed to process: {path} for {event}: {err}'.format(**dic))
    now = datetime.utcnow()
    if args.incron_dir in rulematcher.cmds:
        for cmd in rulematcher.cmds[args.incron_dir]:
            try:
                cmd = now.strftime(cmd).format(**dic)
                logger.debug("execute {} ...".format(cmd))
                p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                if p.returncode != 0:
                    logger.error("exited with {} stdout={} stderr={}".format(p.returncode, stdout, stderr))
                else:
                    logger.debug("OK stdout={} stderr={}".format(stdout, stderr))
            except Exception, err:
                logger.warning("Popen error: {}: {}".format(cmd, err))
    return 0

if __name__ == "__main__":
    sys.exit(main())
