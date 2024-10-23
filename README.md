# signalk-victron-ble

A SignalK plugin that reads 123/Smart BMS data over USB.

Requires the 123/Smart BMS to USB cable

This is based off the code for integrating 123/Smart BMS with thingspeak
[smartbms-thingspeak](https://github.com/123electric/smartbms-thingspeak) and 
[signalk-victron-ble](https://github.com/stefanor/signalk-victron-ble)


## Development

- clone the plugin from Github
- `npm link` in the plugin directory
- `npm link signalk-123smartbms-usb` in your server directory

## License

Copyright 2024 Alexander Funcke <funcke@0z.se>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
