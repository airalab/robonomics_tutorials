import Robonomics, { MessageProviderIpfs } from 'robonomics-js';
import { ROBONOMICS, VERSION } from '../config';

let robonomics = null;
export const initRobonomics = (ipfs, networkId) => {
  robonomics = new Robonomics({
    web3,
    account: {
      address: web3.eth.accounts[0]
    },
    ens: {
      address: ROBONOMICS[networkId].ens,
      suffix: ROBONOMICS[networkId].ensSuffix,
      version: VERSION
    },
    messageProvider: new MessageProviderIpfs(ipfs),
    lighthouse: ROBONOMICS[networkId].lighthouse
  });
  return robonomics;
};
const getRobonomics = () => {
  if (robonomics === null) {
    throw new Error('Robonomics not init');
  }
  return robonomics;
};

export default getRobonomics;
