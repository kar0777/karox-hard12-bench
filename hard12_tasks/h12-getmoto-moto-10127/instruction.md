You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[CloudFront] list_distributions doesn't properly return distribution_config

Attached test shows that the Cloudfront distribution_config fields aren't being returned as top level fields as mentioned in 
https://docs.aws.amazon.com/boto3/latest/reference/services/cloudfront/client/list_distributions.html

```
(.venv) jlim@603e5f5a8790 moto % pytest tests/test_cloudfront/test_cloudfront_distributions.py::test_list_distributions_config_fields -s 
=============================================================================================================================================================================================== test session starts ================================================================================================================================================================================================
platform darwin -- Python 3.11.4, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/iwt148/moto
configfile: pyproject.toml
plugins: cov-6.0.0, order-1.3.0, xdist-3.6.1
collected 1 item                                                                                                                                                                                                                                                                                                                                                                                                   

tests/test_cloudfront/test_cloudfront_distributions.py F

===================================================================================================================================================================================================== FAILURES =====================================================================================================================================================================================================
______________________________________________________________________________________________________________________________________________________________________________________ test_list_distributions_config_fields _______________________________________________________________________________________________________________________________________________________________________________________

    @mock_aws
    def test_list_distributions_config_fields():
        client = boto3.client("cloudfront", region_name="us-east-1")
    
        client.create_distribution(
            DistributionConfig=scaffold.example_distribution_config(ref="ref1")
        )
    
        item = client.list_distributions()["DistributionList"]["Items"][0]
>       assert item["Origins"]["Quantity"] == 1
E       KeyError: 'Origins'

tests/test_cloudfront/test_cloudfront_distributions.py:786: KeyError
============================================================================================================================================================================================= short test summary info ==============================================================================================================================================================================================
FAILED tests/test_cloudfront/test_cloudfront_distributions.py::test_list_distributions_config_fields - KeyError: 'Origins'
```
