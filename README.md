# url-shortener
URL shortener for UVA project

## Quick Started

### Prerequisite

- **Install Docker engine and Docker compose**

  > The easiest way is to install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/), which includes Docker Compose along with Docker Engine and Docker CLI.

### Install

To install url-shortener service, follow the below steps:

1. **Clone the url-shortener repository**

   ```
   git clone https://github.com/Vishwamitra/url-shortner.git
   ```

2. **Deploy and run url-shortener service**

   ```bash
   bash url-shortener/url-shortener/run.sh
   ```

### Usage

See and interact with RESTful APIs on **http://127.0.0.1:5001/apidocs/**



## Development

### Docker environment variable configuration

If you want your url-shortener service run on different port, configure the environment variable in `url-shortener/url-shortener/.env` file. Also, you can modify the database password and the base URL in this file. The default configuration is shown as below.

```ini
DATABASE_NAME=postgres
DATABASE_USER=postgresadmin
DATABASE_PASSWORD=admin123
DATABASE_PORT=5432
API_PORT=5001
API_DEBUG=True
BASE_URL_FOR_SHORT_URL=https://snv.io
```