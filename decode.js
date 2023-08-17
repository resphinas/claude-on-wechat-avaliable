
function traceid(){
    const Crypto = require("crypto-js");
    let n = Crypto && Crypto.getRandomValues ? ()=>Crypto.getRandomValues(new Uint8Array(1))[0] : ()=>16 * Math.random();
    return "10000000100040008000100000000000".replace(/[018]/g, e=>(e ^ (15 & n()) >> e / 4).toString(16))}
// console.log(traceid(0))

function spanid(){
    const Crypto = require("crypto-js");
    let n = Crypto && Crypto.getRandomValues ? ()=>Crypto.getRandomValues(new Uint8Array(1))[0] : ()=>16 * Math.random();
    return "10000000100040008000100000000000".replace(/[018]/g, e=>(e ^ (15 & n()) >> e / 4).toString(16)).substring(16)}
// console.log(spanid(0))

function Sentry_Trace(){
    return traceid()+"-"+spanid()+"-0"
}


console.log(Sentry_Trace())
