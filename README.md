# bfbc2-stats-lambda
AWS Lambda function to retrieve Battlefield: Bad Company 2 player statistics

## Archived as of 2022-03-13
Due to how long the login process takes and how long it takes to fetch, a Lambda is not really the tool for the job. Since the lambda would need to login during every execution, it would take 3-5 seconds to fetch stats.

Instead, an API that keeps a FESL client logged in and ready can be found at [fesl.cetteup.com](https://fesl.cetteup.com/docs). Said API can fetch a minimal set of stats attributes in around 300ms, since the login can be skipped. Pulling all available stats attributes will usually take around 2 seconds.
