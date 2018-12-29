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
        const socket = io(IPFS_PUBSUB)
        robonomics = new Robonomics({
          web3,
          provider: new Provider(socket),
          ens: ROBONOMICS[Number(r)].ens,
          ensSuffix: ROBONOMICS[Number(r)].ensSuffix,
          lighthouse: ROBONOMICS[Number(r)].lighthouse,
          version: VERSION
        })
        resolve(robonomics)
      })
    })
  }
  return Promise.resolve(robonomics)
}

export default getRobonomics
