import json
import pytest

from crawler import Crawler, EmptyKeywords, NoQueryTypeProvided


@pytest.fixture()
def request_ok():
    """
    Returns a valid input dict
    :return: valid input dict.
    """
    return dict(
        keywords=["openstack", "nova", "css"],
        proxies=["194.126.37.94:8080", "13.78.125.167:8080"],
        type="Repositories"
    )


@pytest.fixture()
def response_repos_ok():
    """
    Returns a correct repos list response.
    :return: correct repos list response.
    """
    return [{
        "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage",
        "extra": {
            "owner": "atuldjadhav",
            "language_stats": {
                "CSS": 52.0,
                "JavaScript": 47.2,
                "HTML": 0.8}}}]


@pytest.fixture()
def response_wikis_ok():
    """
    Returns a correct wikis list response.
    :return: correct wikis list response.
    """
    return [
        {"url": "https://github.com/vault-team/vault-website/wiki/Quick-instal"
                "lation-guide"},
        {"url": "https://github.com/iiwaziri/wiki_learn/wiki/Packstack"},
        {"url": "https://github.com/marcosaletta/Juno-CentOS7-Guide/wiki/2.-Co"
                "ntroller-and-Network-Node-Installation"},
        {"url": "https://github.com/MirantisDellCrowbar/crowbar/wiki/Release-n"
                "otes"},
        {"url": "https://github.com/dellcloudedge/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/rhafer/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/eryeru12/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/vinayakponangi/crowbar/wiki/Release-note"
                "s"},
        {"url": "https://github.com/jamestyj/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/opencit/opencit/wiki/Open-CIT-3.2.1-Produc"
                "t-Guide"}
    ]


@pytest.fixture()
def response_issues_ok():
    """
    Returns a correct issues list response.
    :return: correct issues list response.
    """
    return [
        {"url": "https://github.com/hellowj/blog/issues/37"},
        {"url": "https://github.com/sfPPP/openstack-note/issues/8"},
        {"url": "https://github.com/altai/nova-billing/issues/1"},
        {"url": "https://github.com/novnc/websockify/issues/180"},
        {"url": "https://github.com/aaronkurtz/gourmand/pull/35"},
        {"url": "https://github.com/zioc/contrail-devstack-plugin/issues/27"},
        {"url": "https://github.com/rcbops/rpc-openstack/pull/2257"},
        {"url": "https://github.com/sphinx-doc/sphinx/issues/3782"},
        {"url": "https://github.com/clearlydefined/service/issues/85"},
        {"url": "https://github.com/python/core-workflow/issues/6"}
    ]


def test_repos_ok(request_ok, response_repos_ok):
    """
    Test that the repository functionality work ok.
    :param request_ok: dictionary with a correct repos query.
    :param response_ok: list with a correct response
    """
    cr = Crawler()
    query_data = json.dumps(request_ok)
    expected_response = json.dumps(response_repos_ok)
    assert cr.query(query_data) == expected_response


def test_wikis_ok(request_ok, response_wikis_ok):
    """
    Test that the wikis functionality work ok.
    :param request_ok: dictionary with a correct wikis query.
    :param response_ok: list with a correct response
    """
    cr = Crawler()
    request_ok['type'] = "Wikis"
    query_data = json.dumps(request_ok)
    expected_response = json.dumps(response_wikis_ok)
    assert cr.query(query_data) == expected_response


def test_issues_ok(request_ok, response_issues_ok):
    """
    Test that the issues functionality work ok.
    :param request_ok: dictionary with a correct issues query.
    :param response_ok: list with a correct response
    """
    cr = Crawler()
    request_ok['type'] = "Issues"
    query_data = json.dumps(request_ok)
    expected_response = json.dumps(response_issues_ok)
    assert cr.query(query_data) == expected_response


def test_empty_keywords(request_ok):
    """
    Test that an EmptyKeywords exception is raised when empty keywords.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    request_ok['keywords'] = []
    query_data = json.dumps(request_ok)
    with pytest.raises(EmptyKeywords):
        cr.query(query_data)


def test_not_list_keywords(request_ok):
    """
    Test that a TypeError exception is raised when keywords is not a list.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    request_ok['keywords'] = 123
    query_data = json.dumps(request_ok)
    with pytest.raises(TypeError):
        cr.query(query_data)


def test_no_keywords(request_ok):
    """
    Test that a KeyError exception is raised when no keywords.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    del request_ok['keywords']
    query_data = json.dumps(request_ok)
    with pytest.raises(KeyError):
        cr.query(query_data)


def test_not_list_proxies(request_ok):
    """
    Test that a TypeError exception is raised when proxies is not a list.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    request_ok['proxies'] = 123
    query_data = json.dumps(request_ok)
    with pytest.raises(TypeError):
        cr.query(query_data)


def test_no_proxies(request_ok):
    """
    Test that a KeyError exception is raised when no proxies.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    del request_ok['proxies']
    query_data = json.dumps(request_ok)
    with pytest.raises(KeyError):
        cr.query(query_data)


def test_empty_type(request_ok):
    """
    Test that an NoQueryTypeProvided exception is raised when empty type.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    request_ok['type'] = ""
    query_data = json.dumps(request_ok)
    with pytest.raises(NoQueryTypeProvided):
        cr.query(query_data)


def test_incorrect_type(request_ok):
    """
    Test that an NoQueryTypeProvided exception is raised when incorrect type.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    request_ok['type'] = "blabla"
    query_data = json.dumps(request_ok)
    with pytest.raises(NoQueryTypeProvided):
        cr.query(query_data)


def test_not_string_type(request_ok):
    """
    Test that a TypeError exception is raised when proxies is not a string.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    request_ok['type'] = 123
    query_data = json.dumps(request_ok)
    with pytest.raises(TypeError):
        cr.query(query_data)


def test_no_type(request_ok):
    """
    Test that a KeyError exception is raised when no type.
    :param request_ok: dictionary with a correct repos query.
    """
    cr = Crawler()
    del request_ok['type']
    query_data = json.dumps(request_ok)
    with pytest.raises(KeyError):
        cr.query(query_data)
