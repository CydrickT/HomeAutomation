# Introduction
This is an home automation project for the nightstand. It integrates Raspberry Pi Audio, Philips Hue and PC's Wake-On-Lan capabilities. It's designed to be extensible.

This is a project that I've done over the summer to teach myself about Python, electronic circuits and general system integration. I'm from a Software Engineering background, so there might be better ways to solve some electronic-related challenges.

Feel free to submit pull requests.

# Components
* 1x Raspberry Pi 3 model B or higher (Must have Wifi capabilities)
* 1x Project Box ([Example](https://www.amazon.ca/gp/product/B07D23BF7Y/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1))
* 2x Buttons. I've used [5v buttons with lights](https://www.amazon.ca/EG-Illuminated-Buttons-Machine-Raspberry/dp/B01N11BDX9/ref=sr_1_1_sspa?dchild=1&keywords=EG+Starts+5x+30mm+Arcade+LED+Lights&qid=1595167643&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExUk8wUTg0WElKSk42JmVuY3J5cHRlZElkPUEwNTUyMDUxMkk3RFdUN0lIOFNLRiZlbmNyeXB0ZWRBZElkPUEwMTExNDQ0VE80N0pUQTNZSDZTJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==) for this project. Circuit architecture & software configuration might differ if the buttons used are different.
* 2x 2.2k Ohm Resistor. ([Example](https://www.amazon.ca/gp/product/B07L851T3V/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1))
* 1x Small Breadboard. ([Example](https://www.amazon.ca/Breadboard-Solderless-Prototype-PCB-Board/dp/B07589R1Q3/ref=sr_1_8?dchild=1&keywords=breadboard&qid=1595167198&sr=8-8))
* 1x Breadboard Jumper Wire Kit with Male-To-Female and Male-To-Male wires. ([Example](https://www.amazon.ca/Elegoo-120pcs-Multicolored-Breadboard-arduino/dp/B01EV70C78/ref=pd_bxgy_img_2/140-6625145-0927353?_encoding=UTF8&pd_rd_i=B01EV70C78&pd_rd_r=f6e65db0-0893-4511-a383-565f57ca271e&pd_rd_w=YyDz9&pd_rd_wg=Dxsw3&pf_rd_p=5b9fb149-eaf1-46dd-9884-d34ba47b0e7b&pf_rd_r=N99AVNTH7K4D83TTTH9W&psc=1&refRID=N99AVNTH7K4D83TTTH9W))
* 1x Audio Extension Cable. ([Example](https://www.amazon.ca/Headphone-Extension-Compatible-Earphone-Microphone/dp/B06XCSFQ2N/ref=sr_1_10?dchild=1&keywords=audio+extension&qid=1595167379&sr=8-10))
* 2x Velcro strips to hold the Raspberry Pi and the breadboard stable in the project box ([Example](https://www.amazon.ca/BRAVESHINE-Heavy-Duty-Adhesive-Tape/dp/B07GRNYG18/ref=sr_1_3?dchild=1&keywords=velcro+strips&qid=1595172465&sr=8-3))
* Optional: 1x HDMI to VGA with Audio converter ([Example](https://www.amazon.ca/Rankie-Adapter-3-5mm-Audio-Black/dp/B00ZMV7RL2/ref=sr_1_3?crid=3OSR1A83XPWH5&dchild=1&keywords=hdmi+to+vga+with+audio&qid=1595166982&sprefix=hdmi+to+vga+with+%2Caps%2C147&sr=8-3))
* Optional: 1x Multimeter. ([Example](https://www.amazon.ca/AstroAI-Digital-Multimeter-2000Counts-Voltage/dp/B01ISAMUA6/ref=sr_1_2_sspa?dchild=1&keywords=multimeter&qid=1595167451&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFDNFY1SlM4TEFTVkImZW5jcnlwdGVkSWQ9QTA4NjA2MjE1NFQ4NURWU1RBSVcmZW5jcnlwdGVkQWRJZD1BMDU4MDI3MDFFUU9ESUpaODMwUkUmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl))
* Optional: 1x Raspberry Pi case / platform ([Example](https://www.amazon.ca/Transparent-Clear-Case-Raspberry-Model/dp/B07FCS8DRD/ref=sr_1_6?dchild=1&keywords=raspberry+pi+3+case&qid=1595172583&sr=8-6))
# Software Architecture
## Services
### ButtonInputService
### CommandInterpreterService
### LightManagerService
### MusicManagerService
### TerminalInputService
### WakeOnLanManagerService
# Circuit Architecture
# System Configuration
## Wake-On-Lan (WOL)
In order for WOL to work, the computer needs to be configured to do so. This might require extra steps depending on your motherboard and OS. Using my setup, I had to modify both my Windows settings and my BIOS

### Windows Configuration
In "Device Manager", select "Network Adapters" and double-click on your network adapter. In the tab "Power Management", make sure you've checked "Allow this device to wake the computer". If you have an Intel network card, click on the "Advanced" tab, select "Wake on Magic Packet" and select the value "Enabled". If you do not see this option, it might be necessary to download the latest Intel Network Adapters from [here](https://downloadcenter.intel.com/download/25016/Ethernet-Intel-Network-Adapter-Driver-for-Windows-10?product=82186).

In "Power & Sleep Settings", click on "Additional Power Settings". Then, in "Power Options", click on "Chose what the power buttons do". Then, in "System Settings", click on "Change Settings that are currently unavailable" and uncheck "Turn on fast startup (recommended)". 

### BIOS Configuration
Consult your motherboard guide on how to turn on WOL. For instance, for an Asus motherboard, you have to go in "Advanced > APM Configuration", set "ErP Ready" to "Disabled" and "Power On By PCI-E/PCI" to "Enabled".

## Philips Hue
In order to use the Philips Hue Bridge to connect to the lights, a username needs to be generated. This username looks like `1028d66426293e821ecfd9ef1a0731df`. In order to generate a new one go to `https://<bridge ip address>/debug/clip.html`. In "URL", enter `/api` and in "Message Body", enter `{"devicetype":"HomeAutomation#Instance"}` (The device type can be customzied as desired). Click on the blue physical button on the Philips Hue Bridge, then quickly click on "Post" in the webpage. The "Command Respose" should display the username.
