const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: true
    });
    const page = await browser.newPage();
    await page.goto('https://ytmp3.cc/en13/', {waitUntil: 'networkidle2'});
    await page.focus('input[name="video"]');
    await page.keyboard.type(process.argv[2])
    await page.click("#submit")
    try {
        await page.waitForSelector('#buttons', {visible: true})
    } catch (e) {
        console.log('error')
        await browser.close()
    }
    let href = await page.evaluate("document.querySelector('#buttons').firstElementChild.href")
    console.log(href)
    await browser.close()

})();