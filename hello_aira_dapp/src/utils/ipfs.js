import Promise from 'bluebird';
import { IPFS_CONFIG } from '../config';

let ipfs = null;
const getIpfs = () => {
  if (ipfs !== null) {
    return Promise.resolve(ipfs);
  }
  const init = (resolve, reject) => {
    ipfs = new Ipfs(IPFS_CONFIG);
    ipfs.once('ready', () =>
      ipfs.id((err, info) => {
        if (err) {
          return reject(err);
        }
        // eslint-disable-next-line no-console
        console.log('ipfs id ' + info.id);
        window.ipfs = ipfs;
        resolve(ipfs);
      })
    );
  };
  const check = (resolve, reject) => {
    init(resolve, reject);
  };
  if (document.readyState !== 'complete') {
    return new Promise((resolve, reject) => {
      window.addEventListener('load', () => {
        check(resolve, reject);
      });
    });
  } else {
    return new Promise((resolve, reject) => {
      check(resolve, reject);
    });
  }
};

export default getIpfs;
