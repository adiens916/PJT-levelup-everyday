## Available Scripts
### `create_env.sh`
Makes an environment variable for **backend(host) server URL** to use API.
- If you work on **localhost**, then you don't need this.
- However, if you build on **web server**, then you have to setup backend(host) URL by this script or on your own.
  ```bash
  # frontend/.env.production
  REACT_APP_BACKEND_HOST='https://your-backend-server.com'
  ```

### `npm test`

Launches the test runner in the interactive watch mode.

*Currently, there are tests only for API connection.*

### `npm start`

Runs the app in the development mode.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `npm run build`
Or, use **`npm run build:on-server`** \
if you build on a server with low memory such as **AWS EC2**.\
this will prevent build error caused by out of memory

## ETC
### settings changed from default
- basic import path (`tsconfig.json`) 
- test setup for network connection (`src/setupTests.ts`)
