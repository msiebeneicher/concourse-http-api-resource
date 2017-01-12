import json
import subprocess

import pytest

from helpers import cmd


def test_out(httpbin):
    """Test out action with minimal input."""

    data = {
        'source': {
            'uri': httpbin + '/status/200',
        }
    }
    subprocess.check_output('/opt/resource/out', input=json.dumps(data).encode())

def test_out_failure(httpbin):
    """Test action failing if not OK http response."""

    data = {
        'source': {
            'uri': httpbin + '/status/404',
        }
    }
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output('/opt/resource/out', input=json.dumps(data).encode())

def test_auth(httpbin):
    """Test basic authentication."""

    data = {
        'source': {
            'uri':  'http://user:password@{0.host}:{0.port}/basic-auth/user/password'.format(httpbin),
        }
    }
    subprocess.check_output('/opt/resource/out', input=json.dumps(data).encode())

def test_json(httpbin):
    """Json should be passed as JSON content."""

    source = {
        'uri': httpbin + '/post',
        'method': 'POST',
        'json': {
            'test': 123,
        },
    }

    output = cmd('out', source)

    assert output['json']['test'] == 123

def test_data_urlencode(httpbin):
    """Test passing URL encoded data."""

    source = {
        'uri': httpbin + '/post',
        'method': 'POST',
        'form_data': {
            'field': {
                'test': 123,
            },
        },
    }

    output = cmd('out', source)

    assert output['form'] == {'field': '{"test": 123}'}

def test_check(httpbin):
    """Json should be passed as JSON content."""

    source = {
        'uri': httpbin + '/post',
        'method': 'POST',
        'json': {
            'test': 123,
        },
    }

    output = cmd('check', source, version={'ref': '123'})

    ref_0 = output[0]
    ref_1 = output[1]

    print(output)

    assert ref_0.get('ref') != '123'
    assert ref_1.get('ref') == '123'

def test_json_in(httpbin):
    """Json should be passed as JSON content."""

    source = {
        'uri': httpbin + '/post',
        'method': 'POST',
        'json': {
            'test': 987,
        },
    }

    output = cmd('in', source, args=['/tmp'])

    assert output['json']['test'] == 987
