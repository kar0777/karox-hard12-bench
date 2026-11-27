You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Transfer] Server and Connector optional fields should not be returned in response

https://docs.aws.amazon.com/boto3/latest/reference/services/transfer/client/describe_server.html
https://docs.aws.amazon.com/transfer/latest/APIReference/API_DescribedServer.html

In practice, it appears that optional values that are not set shouldn't be included in the responses.
Fields such as LoggingRole and others should be omitted from responses

https://github.com/getmoto/moto/blob/master/moto/transfer/types.py
