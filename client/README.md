# alive

> Alive Project

## Build Setup

#### Setting up Webpack server
``` bash
# install dependencies
npm install

# See dev.env.js configuration
touch config/dev.env.js

# See prod.env.js configuration
touch config/dev.env.js
```

#### Setting up SSL
``` bash
# generate SSL certificate
./gencert.sh
```

#### Deployment

``` bash
# serve with hot reload at localhost:8080 (unless specified otherwise)
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

## Configurations

### `dev.env.js`
``` Javascript
'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"API_URL"',
  API_KEY: '"OPENTOK_API_KEY"'
})
```

### `prod.env.js`
``` Javascript
'use strict'
module.exports = {
  NODE_ENV: '"production"',
  API_URL: '"API_URL"',
  API_KEY: '"OPENTOK_API_KEY"'
}
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
