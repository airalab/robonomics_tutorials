import { open } from 'rosbag'
import axios from 'axios'

export default (hash, options, cb) => (
  axios.get(`https://ipfs.io/ipfs/${hash}`, {
    responseType: 'blob'
  })
    .then(r => open(r.data))
    .then((bag) => {
      // console.log(bag)
      bag.readMessages(options, (result) => {
        cb(result.message)
      })
    })
)
