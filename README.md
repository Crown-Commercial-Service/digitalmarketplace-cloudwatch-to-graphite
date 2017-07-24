Digital Marketplace Cloudwatch to Graphite
=========================

## Purpose

Ships Cloudwatch metrics to Hosted Graphite using https://github.com/crccheck/cloudwatch-to-graphite.

An example config file is also included (`config.yaml.example`) to help you define the correct structure for your metrics.

## Initial setup

#### Setup a virtualenv, activate it and install python dependencies with pip

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Generate config.yaml

The `config.yaml` file defines what metrics are to be shipped to graphite. It is generated from the `config.yaml.j2` Jinja template using:

```
plumbum config.yaml.j2 ec2 > config.yaml
```

## To run locally

Set the required environment variables

```
export HOSTED_GRAPHITE_API_KEY=your-key-here
export AWS_ACCESS_KEY_ID=your-access-key-id-here
export AWS_SECRET_ACCESS_KEY=your-secret-access-key-here
```

...and run

```
python app.py
```

## To deploy on PaaS

If you haven't done so already, go through the "Initial Setup" section above.

You will also need to create a manifest file using the example manifest (`manifest.yml.example`), filling in the necessary environment variables.
You can then deploy this to the PaaS by running:

```
cf push -f manifest.yml
```
