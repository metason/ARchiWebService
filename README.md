# ARchiWebService

Sample server code to provide Web Services for the [ARchi VR](https://archi.metason.net) App
using:

- [Flask](https://flask.palletsprojects.com)
- Python

The sample code references a fictitious company named "Verified Spaces Inc.".
Replace the fictitious `www.verifiedspaces.com` with your own domain.

## Samples

The sample code contains examples for:
- Service Extension
- Workflow Extension
- Curation Extension

The respond of these Web Services is a Action as JSON object.
See [Technical Documentation](https://service.metason.net/ar/docu/) of ARchi VR for more details.

## Installation

- Get a Web server up and running when not yet available
- Install [Flask](https://flask.palletsprojects.com)
- Download the sample code of this repository
- Make the `extension` folder accessible via your Web server
- Copy the `arext`directory to your flask environment
- Change all `www.verifiedspaces.com` references to your own domain in `extension/ext.json` and `arext/controllers.py`
- Reload Flask app (or setup autoloading)
- Check service availability by calling `https://_yourdomain_/arext/test`
- Define your planned extensions in the `ext.json` file
- Request the registration of your extension by sending an email to [support@metason.net](support@metason.net)) with the `ext.json` file attached
- Start coding your own Web services in `controllers.py` ...
