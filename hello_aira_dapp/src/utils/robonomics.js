import Robonomics from 'robonomics-js'
import Provider from './provider'
import { IPFS_PUBSUB, ROBONOMICS, VERSION } from '../config'

let robonomics = null
const getRobonomics = () => {
  if (robonomics === null) {
    return new Promise((resolve, reject) => {
      web3.version.getNetwork((e, r) => {
        if (!ROBONOMICS.hasOwnProperty(Number(r))) {
          return reject(new Error('No support network'))
        }
        robonomics = new Robonomics({
          web3,
          account: {
            address: web3.eth.accounts[0]
          },
          ens: {
            address: ROBONOMICS[Number(r)].ens,
            suffix: ROBONOMICS[Number(r)].ensSuffix,
            version: VERSION
          },
          messageProvider: new Provider(io(IPFS_PUBSUB)),
          lighthouse: ROBONOMICS[Number(r)].lighthouse
        })
        resolve(robonomics)
      })
    })
  }
  return Promise.resolve(robonomics)
}

export default getRobonomics
