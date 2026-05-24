#!/usr/bin/env python3
import asyncio
async def main():
    import nodriver as uc
    browser = await uc.start(headless=True, browser_args=['--no-sandbox','--disable-gpu'])
    page = await browser.get('https://github.com/gyoomei/mimolink')
    await page.sleep(4)
    await page.send(uc.cdp.emulation.set_device_metrics_override(width=1920,height=1080,device_scale_factor=1,mobile=False))
    await page.sleep(1)
    await page.save_screenshot('/home/ubuntu/mimolink/screenshots/07_github.png')
    print('✅ GitHub screenshot saved')
    browser.stop()
asyncio.run(main())
