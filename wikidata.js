const {chain}  = require('stream-chain');
const {parser} = require('stream-json');
const {pick}   = require('stream-json/filters/Pick');
const {streamArray} = require('stream-json/streamers/streamArray');

const fs   = require('fs');
// const zlib = require('zlib');

const pipeline = chain([
  fs.createReadStream('wikidata.json'),
  //zlib.createGunzip(),
  parser(),
  pick({filter: 'features'}),
  streamArray()
]);

let counter = 0;
pipeline.on('data', (data) => {
  console.log(data.items);
});

pipeline.on('end', () =>
  console.log(`The accounting department has ${counter} employees.`));