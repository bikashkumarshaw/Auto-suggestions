import time
import json
import requests
from urllib.parse import urljoin
import json
import hashlib

from basescript import BaseScript
from esutils import create_index

KB = 1024
MB = 1024 * KB
DATA_SIZE = 10 * MB
BULK_HEADER = {'Content-type': 'application/x-ndjson'}
REINDEX_EXCEPTION = "resource_already_exists_exception"

class ESLOADING(BaseScript):
    def __init__(self):
        super(ESLOADING, self).__init__()

    def define_args(self, parser):
        parser.add_argument("-i", "--index")
        parser.add_argument("--host", help="es server", required=True)
        parser.add_argument("-d", "--data", help="json encoded ES data")

    def ensure_index(self):
        try:
            r = create_index(self.args.host, self.args.index)
            if r.get('status', 0) == 400 and r.get('error', '').get('type') == REINDEX_EXCEPTION:
                self.log.info('Index %s exists already.' % self.args.index)
            elif r.get('acknowledged', False) == True:
                self.log.info('Created index %s' % self.args.index)
            else:
                raise Exception('Error during creating index %s: %s' %\
                    (self.args.index, r))
        except (SystemExit, KeyboardInterrupt): raise
        except Exception as e:
            self.log.exception('During index creation in ES for username=%s' %\
                self.args.index)
            time.sleep(1)
            raise

    def insert_in_bulk(self, items, rtype):
        '''
        This function inserts data to es in bulk
        '''

        U = urljoin(self.args.host, "/_bulk")
        body = []
        for (_id, item) in items:
            body.append(json.dumps(
                dict(index=dict(_index=self.args.index, _type=rtype, _id=_id))
            ))
            body.append(item)

        body = '\n'.join(body) + '\n'
        success = False
        try:
            import pdb;pdb.set_trace()
            r = requests.post(U, data=body, headers=BULK_HEADER)
            if r.status_code == 200:
                success = True
            r = r.json()
            self.log.info("inserted %d items of type = %s", len(items), rtype)
        except (SystemExit, KeyboardInterrupt): raise
        except:
            self.log.exception("during bulk index")

        if not success:
            self.log.error("failed to index records of type = %s, num = %d", rtype, len(items))

    def insert_data(self, fname, rtype, max_size=DATA_SIZE):
        '''
        This function pepares data that needs to be inserted to ES
        and calls insert in bull function to load the data of a
        certain size
        '''

        if not fname:
            return
        size, buf = 0, []
        for line in open(fname):
            size += len(line.strip())
            token, occur = line.strip().split("\t")
            item = {"token": token}
            token = item.get('token', '').encode('utf-8')
            _id = hashlib.md5(token).hexdigest()

            buf.append((_id, json.dumps(item)))
            if size > max_size:
                self.insert_in_bulk(buf, rtype)
                del(buf[:])
                size = 0

        if len(buf) > 0:
            self.insert_in_bulk(buf, rtype)

    def run(self):
        self.ensure_index()
        self.insert_data(self.args.data, "_doc")

if __name__ == '__main__':
    ESLOADING().run()
