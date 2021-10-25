import requests
import pytest
import json


class Test:
    with open("UserAgent_list.json") as f:
        user_agent_params = json.load(f)

    @pytest.mark.parametrize("params", user_agent_params)
    def test_check_user_agent(self, params):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"User-Agent": params["User-Agent"]}
        response = requests.get(url, headers=data)
        assert response.status_code == 200, "Wrong response code"
        assert "platform" in response.json(), "There is no parameter 'platform' in response"
        assert "browser" in response.json(), "There is no parameter 'browser' in response"
        assert "device" in response.json(), "There is no parameter 'device' in response"
        assert response.json()["platform"] == params["Expected_values"]["platform"], f"User-agent with value {params['User-Agent']}" \
                                                                                     f"have returned wrong value of parameter platform"
        assert response.json()["browser"] == params["Expected_values"]["browser"], f"User-agent with value {params['User-Agent']} " \
                                                                                   f"have returned wrong value of parameter browser"
        assert response.json()["device"] == params["Expected_values"]["device"], f"User-agent with value {params['User-Agent']} " \
                                                                                 f"have returned wrong value of parameter device"
