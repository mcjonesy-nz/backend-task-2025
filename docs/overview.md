# Architecture 
Use python even though quite rusty with it

## Overview 
Client
  ↓
API Gateway
  ↓
Lambda 
Split into the various tasks that need to be done. 
- Validation
- Preprocessing
- Clustering
- Generate insights & sentiment 

## Logging
Would use cloudwatch to take the logs from the Lambda. 
Using structured logging to make searching easier.
Ensuring that we don't log raw sentence text

## IaC 
I would use Cloudformation because of familiarity with it. Feedback about it is thhat 
it can be a bit verbose but for a static infrastructure. 
Keep the infra code in the same repo as the lambda code. If you make a change for one 
thing blast radius is contained 
Have both UAT and Production env set up, try to mirror as much as possible between 
the two

## Scability 
Lambda's can scale as the traffic expands. Can bump up memory needs if the data size 
increases. Have config limits that reject if the data size is too big. 

# Testing 
- Had unit tests for each class.
- Use unittest over pytest 
- Run the unit tests on each PR and build.
- Once project is completed then can build integration tests for end to end. 

## Deployment 
- CI/CD pipeline in GitHub actions.
- Single action for entire deployment pipeline for PR's and then build
- PR's focus on just tests while merges to master run the whole pipeline
- Deploy to UAT first and then roll out to prod later 

## ML/AI 
- Start basic and then if time allows add more.
- Transformers seem to be recommended over spaCy, NLTK, can use local model for
this task
- Basic sentiment analysis and same for insights.

# Post Task
- Used VS Code with CoPilot and GPT-5 mini for a lot of the heavy lifiting.
- Asked it to generate the models, unit tests, and a lot of the implementation.
- Worked by giving it the context and overview of the task and the flow and then
working through each step with it.
- Toggled between different chat windows asking the same question and comparing
results.
- Or getting one model to generate the code and another to write the unit tests
- Using it like a pair programmer and getting it to explain why
- When it starting going rogue. Stop. Go back. Look at documentation, do some
Goolging (without AI overview)
- 
