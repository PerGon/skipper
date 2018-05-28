#!/usr/bin/env python
# -*- coding: utf-8
import mock
import pytest

from fiaas_skipper.deploy.deploy import Deployer, DeploymentConfig


class TestDeployer(object):
    @pytest.fixture
    def cluster(self):
        cluster = mock.NonCallableMagicMock(name="cluster")
        cluster.find_deployment_configs.return_value = (
            DeploymentConfig("test1", "test1", "stable"),
            DeploymentConfig("test2", "test2", "stable"),
        )
        return cluster

    @pytest.fixture
    def release_channel_factory(self):
        return mock.MagicMock(name="release_channel_factory")

    def test_deploys_only_to_configured_namespaces(self, cluster, release_channel_factory):
        deployer = Deployer(cluster, release_channel_factory, None)
        deployer._deploy = mock.MagicMock(name="_deploy")
        deployer.deploy(namespaces=("test1",))
        deployer._deploy.assert_called_once()

    def test_deploys_to_all_namespaces(self, cluster, release_channel_factory):
        deployer = Deployer(cluster, release_channel_factory, None)
        deployer._deploy = mock.MagicMock(name="_deploy")
        deployer.deploy()
        assert 2 == deployer._deploy.call_count