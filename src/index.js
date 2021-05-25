const GoogleHome = require("google-home-push");
const { PrayerTimes, Coordinates, CalculationMethod, PolarCircleResolution, Madhab } = require('adhan')
const { CronJob } = require('cron');
const CONFIG = require('./config');

const myHome = new GoogleHome("Kitchen speaker");

function getNextPrayer(targetDate) {
    const nextPrayer = new Date(targetDate)
    console.log('next Prayer at:', nextPrayer)
    const dateNow = new Date()
    const nextTimeOut = nextPrayer - dateNow;
    console.log('time to wait: ', nextTimeOut / 1000)
    return nextTimeOut;
}
 
function waitAndCallPrayer(nextTimeOut, myHome, athanLink) {
    setTimeout(() => {
        console.log('Start Calling To Prayer'); 
        myHome.push(athanLink);
    }, nextTimeOut)
}

function getPrayerTimes() {    
    const params = CalculationMethod.MuslimWorldLeague();
    params.madhab = Madhab.Shafi;
    params.polarCircleResolution = PolarCircleResolution.AqrabBalad;
    params.adjustments.fajr = 2;
    params.adjustments.maghrib = 3;
    
    const coordinates = new Coordinates(51.450298, 5.482038);
    const date = new Date();
    const prayerTimes = new PrayerTimes(coordinates, date, params); 
    return prayerTimes;
}

function initNextPrayer(myHome) {
    const prayerTimes = getPrayerTimes();

    const fajr = getNextPrayer(prayerTimes.fajr)
    if (fajr > 0) waitAndCallPrayer(fajr, myHome, CONFIG.ATHAN.FAJER)

    const dhuhr = getNextPrayer(prayerTimes.dhuhr)
    if (dhuhr > 0)  waitAndCallPrayer(dhuhr, myHome, CONFIG.ATHAN.DEFAULT)

    const asr = getNextPrayer(prayerTimes.asr)
    if (asr > 0)  waitAndCallPrayer(asr, myHome, CONFIG.ATHAN.ASR)

    const maghrib = getNextPrayer(prayerTimes.maghrib)
    if (maghrib > 0)  waitAndCallPrayer(maghrib, myHome, CONFIG.ATHAN.MAGHRIB)

    const isha = getNextPrayer(prayerTimes.isha)
    if (isha > 0)  waitAndCallPrayer(isha, myHome, CONFIG.ATHAN.ISHA)
}


const job = new CronJob('30 1 * * *', async () => {
    console.log('new day new prayer time'); 
    initNextPrayer(myHome);
});

job.start(); 
initNextPrayer(myHome);