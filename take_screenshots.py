#!/usr/bin/env python3
"""Take MiMoLink screenshots at 1920x1080."""
import asyncio, os

async def main():
    import nodriver as uc
    out = '/home/ubuntu/mimolink/screenshots'
    os.makedirs(out, exist_ok=True)
    
    browser = await uc.start(
        headless=True,
        browser_args=['--no-sandbox','--disable-gpu','--window-size=1920,1080']
    )
    page = await browser.get('file:///home/ubuntu/mimolink/index.html')
    await page.sleep(3)
    
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=1920, height=1080, device_scale_factor=1, mobile=False
    ))
    await page.sleep(1)
    
    # Shot 1: Builder dark theme
    await page.save_screenshot(f'{out}/01_builder.png')
    print('✅ Shot 1: Builder')
    
    # Shot 2: Switch to gradient theme
    await page.evaluate("selectTheme('gradient', document.querySelector('[data-theme=\"gradient\"]'))")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/02_gradient.png')
    print('✅ Shot 2: Gradient Theme')
    
    # Shot 3: Switch to sunset theme
    await page.evaluate("selectTheme('sunset', document.querySelector('[data-theme=\"sunset\"]'))")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/03_sunset.png')
    print('✅ Shot 3: Sunset Theme')
    
    # Shot 4: Light builder theme
    await page.evaluate("document.documentElement.setAttribute('data-theme','light')")
    await page.sleep(1)
    await page.evaluate("selectTheme('minimal', document.querySelector('[data-theme=\"minimal\"]'))")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/04_light.png')
    print('✅ Shot 4: Light Mode')
    
    # Shot 5: Mobile view of builder
    await page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
    await page.evaluate("selectTheme('gradient', document.querySelector('[data-theme=\"gradient\"]'))")
    await page.sleep(0.5)
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=375, height=812, device_scale_factor=2, mobile=True
    ))
    await page.sleep(1)
    await page.save_screenshot(f'{out}/05_mobile.png')
    print('✅ Shot 5: Mobile')
    
    # Shot 6: Generated page example (open preview in new tab)
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=1920, height=1080, device_scale_factor=1, mobile=False
    ))
    html = await page.evaluate("generateHTML()")
    page2 = await browser.get(f'data:text/html;charset=utf-8,{html}')
    await page.sleep(2)
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=390, height=844, device_scale_factor=2, mobile=True
    ))
    await page.sleep(1)
    await page.save_screenshot(f'{out}/06_generated.png')
    print('✅ Shot 6: Generated Page')
    
    browser.stop()
    
    for f in sorted(os.listdir(out)):
        size = os.path.getsize(f'{out}/{f}')
        print(f'  {f}: {size//1024}KB')

asyncio.run(main())
