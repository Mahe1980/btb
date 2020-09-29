from datetime import datetime, timedelta
from src.core.service.ctl_service import CTLService
from src.core.service.extractor import Extractor
from src.settings import envs
import argparse
from src.settings import log_config
import logging
from multiprocessing import Pool
from functools import partial
import shutil
from pathlib import Path
import gzip
import json

# Setting up module from __file__ as the interpreter sets __name__ as __main__ when the source file is executed as
# main program
logger = logging.getLogger(name=__file__.replace(envs.PROJECT_ROOT, '').replace('/', '.')[0:-3])

TMP_DIR = "/mapr/atilius.sns.sky.com/tmp/btb/tmp/"
DELTA_DIR = "/mapr-north/data/btb/delta/"


def extract_move(scope, frequency, ctl_source):
    cutoff_ts = datetime.now() - timedelta(hours=2)

    output_file = "{}/{}/{}.json".format(TMP_DIR, frequency.lower(), "{}_{}_delta".
                                         format(ctl_source.source_name, cutoff_ts.strftime("%Y%m%d%H%M%S")))
    extractor = Extractor(ctl_source, cutoff_ts)
    extractor.run(output_file)

    path = Path(output_file)

    delta_output_path = "{}/{}.gz".format(DELTA_DIR, path.name)
    with open(output_file, 'rb') as f_in, gzip.open(delta_output_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    if path.is_file():
        path.unlink()

    value = json.loads(ctl_source.value)
    value["HWM1"] = cutoff_ts.strftime("%Y-%m-%d %H:%M:%S")
    value = json.dumps(value)

    db_update = CTLService(scope, frequency, ctl_source.source_name)
    db_update.update_field("value", value)

    logger.info("updated watermark for {} and gzipped/moved file '{}' from tmp to delta dir."
                .format(ctl_source.source_name, path.name))


def extract(scope, frequency):
    #  clear tmp directory before the extraction
    logger.info("Clearing tmp directory before the extraction.")
    tmp_dir = "{}/{}".format(TMP_DIR, frequency.lower())
    path = Path(tmp_dir)
    [p.unlink() for p in path.glob('*')]

    ctl_service = CTLService(scope, frequency)
    ctl_sources = ctl_service.get_sources()

    with Pool(processes=10) as pool:
        pool.map(partial(extract_move, scope, frequency,), ctl_sources)
    logger.info("Extraction completed.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('scope', help='scope e.g. BTB')
    parser.add_argument('frequency', help='frequency e.g. DAILY')

    args = parser.parse_args()
    extract(**vars(args))
