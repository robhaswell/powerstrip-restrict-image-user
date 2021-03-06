import unittest

import json as _json

import lib
import priu

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = priu.app.test_client()

    def test_integration_create_user_success(self):
        """
        The request is returned unmodified when the user is allowed.
        """
        priu.app.config['ALLOWED_USER'] = "good"
        path = "/v1.16/containers/create"
        json = r'{"Hostname":"","Domainname":"","User":"","Memory":0,"MemorySwap":0,"CpuShares":0,"Cpuset":"","AttachStdin":false,"AttachStdout":true,"AttachStderr":true,"PortSpecs":null,"ExposedPorts":{},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":[],"Cmd":null,"Image":"good/container","Volumes":{},"WorkingDir":"","Entrypoint":null,"NetworkDisabled":false,"MacAddress":"","OnBuild":null,"HostConfig":{"Binds":null,"ContainerIDFile":"","LxcConf":[],"Privileged":false,"PortBindings":{},"Links":null,"PublishAllPorts":false,"Dns":null,"DnsSearch":null,"ExtraHosts":null,"VolumesFrom":null,"Devices":[],"NetworkMode":"bridge","IpcMode":"","CapAdd":null,"CapDrop":null,"RestartPolicy":{"Name":"","MaximumRetryCount":0},"SecurityOpt":null}}'
        request_json = self._make_powerstrip_pre_hook_request("POST", path, json)
        expected_json = lib.pre_hook_response("POST", path, json)

        rv = self.app.post("/", data=request_json, headers={
            "content-type": "application/json"})

        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.data, expected_json)
        self.assertEquals(rv.headers['content-type'], "application/json")

    def test_integration_create_user_fail(self):
        """
        The status code is 403 when the user is bad.
        """
        priu.app.config['ALLOWED_USER'] = "good"
        path = "/v1.16/containers/create"
        json = r'{"Hostname":"","Domainname":"","User":"","Memory":0,"MemorySwap":0,"CpuShares":0,"Cpuset":"","AttachStdin":false,"AttachStdout":true,"AttachStderr":true,"PortSpecs":null,"ExposedPorts":{},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":[],"Cmd":null,"Image":"bad/container","Volumes":{},"WorkingDir":"","Entrypoint":null,"NetworkDisabled":false,"MacAddress":"","OnBuild":null,"HostConfig":{"Binds":null,"ContainerIDFile":"","LxcConf":[],"Privileged":false,"PortBindings":{},"Links":null,"PublishAllPorts":false,"Dns":null,"DnsSearch":null,"ExtraHosts":null,"VolumesFrom":null,"Devices":[],"NetworkMode":"bridge","IpcMode":"","CapAdd":null,"CapDrop":null,"RestartPolicy":{"Name":"","MaximumRetryCount":0},"SecurityOpt":null}}'
        request_json = self._make_powerstrip_pre_hook_request("POST", path, json)

        rv = self.app.post("/", data=request_json, headers={
            "content-type": "application/json"})

        self.assertEquals(rv.status_code, 403)

    def test_integration_create_official_success(self):
        """
        The request is returned unmodified when the official is allowed.
        """
        priu.app.config['ALLOWED_USER'] = "_"
        path = "/v1.16/containers/create"
        json = r'{"Hostname":"","Domainname":"","User":"","Memory":0,"MemorySwap":0,"CpuShares":0,"Cpuset":"","AttachStdin":false,"AttachStdout":true,"AttachStderr":true,"PortSpecs":null,"ExposedPorts":{},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":[],"Cmd":null,"Image":"container","Volumes":{},"WorkingDir":"","Entrypoint":null,"NetworkDisabled":false,"MacAddress":"","OnBuild":null,"HostConfig":{"Binds":null,"ContainerIDFile":"","LxcConf":[],"Privileged":false,"PortBindings":{},"Links":null,"PublishAllPorts":false,"Dns":null,"DnsSearch":null,"ExtraHosts":null,"VolumesFrom":null,"Devices":[],"NetworkMode":"bridge","IpcMode":"","CapAdd":null,"CapDrop":null,"RestartPolicy":{"Name":"","MaximumRetryCount":0},"SecurityOpt":null}}'
        request_json = self._make_powerstrip_pre_hook_request("POST", path, json)
        expected_json = lib.pre_hook_response("POST", path, json)

        rv = self.app.post("/", data=request_json, headers={
            "content-type": "application/json"})

        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.data, expected_json)
        self.assertEquals(rv.headers['content-type'], "application/json")

    def test_integration_create_office_fail(self):
        """
        The status code is 403 when the user and only official Docker images
        are allowed.
        """
        priu.app.config['ALLOWED_USER'] = "_"
        path = "/v1.16/containers/create"
        json = r'{"Hostname":"","Domainname":"","User":"","Memory":0,"MemorySwap":0,"CpuShares":0,"Cpuset":"","AttachStdin":false,"AttachStdout":true,"AttachStderr":true,"PortSpecs":null,"ExposedPorts":{},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":[],"Cmd":null,"Image":"bad/container","Volumes":{},"WorkingDir":"","Entrypoint":null,"NetworkDisabled":false,"MacAddress":"","OnBuild":null,"HostConfig":{"Binds":null,"ContainerIDFile":"","LxcConf":[],"Privileged":false,"PortBindings":{},"Links":null,"PublishAllPorts":false,"Dns":null,"DnsSearch":null,"ExtraHosts":null,"VolumesFrom":null,"Devices":[],"NetworkMode":"bridge","IpcMode":"","CapAdd":null,"CapDrop":null,"RestartPolicy":{"Name":"","MaximumRetryCount":0},"SecurityOpt":null}}'
        request_json = self._make_powerstrip_pre_hook_request("POST", path, json)

        rv = self.app.post("/", data=request_json, headers={
            "content-type": "application/json"})

        self.assertEquals(rv.status_code, 403)

    def _make_powerstrip_pre_hook_request(self, method, path, json):
        """
        Format a Powerstrip pre-hook request JSON blob.
        """
        return _json.dumps(dict(
            PowerstripProtocolVersion=1,
            Type="pre-hook",
            ClientRequest=dict(
                Method=method,
                Request=path,
                Body=json,
            )))

if __name__ == '__main__':
    unittest.main()
